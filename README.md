# DRF Concurrency
Simple Django app to play around with concurrent requests to DRF.

In the most simple setup, Django/DRF seems to have a problem when handling simultaneous requests that try to modify or create a resource where database constraints apply.
Suppose you have an endpoint that creates customers. They have an id which is the primary key, and a login name, which must be unique. DRF and Django validate the uniqueness out of the box and the Serializer will return a 400 status with an appropriate message when trying to create a resource with a conflicting login (`{"login":["customer with this login already exists."]}`).

Now suppose that two requests, that both try to create a resource with the same login, arrive at (virtually) the same moment. They are handled by two separate threads. DRF will first validate that the data is correct (i.e. there is no resource with the same login yet). Because this step runs at virtually the same moment, both validations succeed. Then the first thread will create the resource and return success. The second thread now also tries to create the resource, but the database layer will raise an IntegrityError because the login is no longer unique. This error is not caught by the serializer, but ends up in the view which turns it into a 500 Internal Server Error.

This example app demonstrates the above mechanism. There is a sleep implemented just before creating the resource, to broaden the window for the race condition. The test-script (`./test.sh`) will do two (almost) simultaneous POST-requests to create a resource with the same login. The first succeeds, the seconds fails with a 500. Then a third POST-request is done with the same login to demonstrate the expected API response.

## Running the example
```
git clone https://github.com/gertjanol/drfconcurrency.git
cd drfconcurrency
# Start container for database first to give it a chance to boot before starting Django
docker-compose up -d db
docker-compose up -d web
docker-compose logs -f
```

In another window:
```
./test.sh
```

## Tested
 * Add `'ATOMIC_REQUESTS': True` to the `DATABASES['default']`-section in the settings.
   * Doesn't seem to have any effect
   * And has the side effect of starting a transaction on **all** configured databases on each request when using multiple databases.
 * Wrapping `concur.views.CustomerViewset.create` with an `@transaction.atomic` decorator
   * Doesn't seem to have any effect
 * Set `'OPTIONS': {'isolation_level': ISOLATION_LEVEL_SERIALIZABLE},` (also tested other isolation levels) on the default database
   * Doesn't seem to have any effect

## Results

Test script:
```
$ ./test.sh
{"id":119,"login":"henk12109"}
<h1>Server Error (500)</h1>
{"login":["customer with this login already exists."]}
```

Server logs:
```
web_1  | [04/Jan/2019 03:49:40] "POST /api/customer/ HTTP/1.1" 201 30
web_1  | Internal Server Error: /api/customer/
web_1  | Traceback (most recent call last):
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 85, in _execute
web_1  |     return self.cursor.execute(sql, params)
web_1  | psycopg2.IntegrityError: duplicate key value violates unique constraint "concur_customer_login_key"
web_1  | DETAIL:  Key (login)=(henk21709) already exists.
web_1  |
web_1  |
web_1  | The above exception was the direct cause of the following exception:
web_1  |
web_1  | Traceback (most recent call last):
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/core/handlers/exception.py", line 34, in inner
web_1  |     response = get_response(request)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/core/handlers/base.py", line 126, in _get_response
web_1  |     response = self.process_exception_by_middleware(e, request)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/core/handlers/base.py", line 124, in _get_response
web_1  |     response = wrapped_callback(request, *callback_args, **callback_kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/views/decorators/csrf.py", line 54, in wrapped_view
web_1  |     return view_func(*args, **kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/viewsets.py", line 116, in view
web_1  |     return self.dispatch(request, *args, **kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/views.py", line 495, in dispatch
web_1  |     response = self.handle_exception(exc)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/views.py", line 455, in handle_exception
web_1  |     self.raise_uncaught_exception(exc)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/views.py", line 492, in dispatch
web_1  |     response = handler(request, *args, **kwargs)
web_1  |   File "/usr/local/lib/python3.7/contextlib.py", line 74, in inner
web_1  |     return func(*args, **kwds)
web_1  |   File "/srv/project/concur/views.py", line 16, in create
web_1  |     return super(CustomerViewset, self).create(request, *args, **kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/mixins.py", line 21, in create
web_1  |     self.perform_create(serializer)
web_1  |   File "/srv/project/concur/views.py", line 20, in perform_create
web_1  |     return serializer.save(**extra_kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/serializers.py", line 214, in save
web_1  |     self.instance = self.create(validated_data)
web_1  |   File "/usr/local/lib/python3.7/site-packages/rest_framework/serializers.py", line 940, in create
web_1  |     instance = ModelClass._default_manager.create(**validated_data)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/manager.py", line 82, in manager_method
web_1  |     return getattr(self.get_queryset(), name)(*args, **kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/query.py", line 413, in create
web_1  |     obj.save(force_insert=True, using=self.db)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 718, in save
web_1  |     force_update=force_update, update_fields=update_fields)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 748, in save_base
web_1  |     updated = self._save_table(raw, cls, force_insert, force_update, using, update_fields)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 831, in _save_table
web_1  |     result = self._do_insert(cls._base_manager, using, fields, update_pk, raw)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/base.py", line 869, in _do_insert
web_1  |     using=using, raw=raw)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/manager.py", line 82, in manager_method
web_1  |     return getattr(self.get_queryset(), name)(*args, **kwargs)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/query.py", line 1136, in _insert
web_1  |     return query.get_compiler(using=using).execute_sql(return_id)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1289, in execute_sql
web_1  |     cursor.execute(sql, params)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 68, in execute
web_1  |     return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 77, in _execute_with_wrappers
web_1  |     return executor(sql, params, many, context)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 85, in _execute
web_1  |     return self.cursor.execute(sql, params)
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
web_1  |     raise dj_exc_value.with_traceback(traceback) from exc_value
web_1  |   File "/usr/local/lib/python3.7/site-packages/django/db/backends/utils.py", line 85, in _execute
web_1  |     return self.cursor.execute(sql, params)
web_1  | django.db.utils.IntegrityError: duplicate key value violates unique constraint "concur_customer_login_key"
web_1  | DETAIL:  Key (login)=(henk21709) already exists.
web_1  |
web_1  | [04/Jan/2019 03:49:40] "POST /api/customer/ HTTP/1.1" 500 27
web_1  | Bad Request: /api/customer/
web_1  | [04/Jan/2019 03:49:40] "POST /api/customer/ HTTP/1.1" 400 54
```
