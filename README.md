# DRF Concurrency
Simple Django app to play around with concurrent requests to DRF.

In the most simple setup, Django/DRF seems to have a problem when handling simultaneous requests that try to modify or create a resource where database constraints apply.
Suppose you have an endpoint that creates customers. They have an id which is the primary key, and a login name, which must be unique. DRF and Django validate the uniqueness out of the box and the Serializer will return a 400 status with an appropriate message when trying to create a resource with a conflicting login (`{"login":["customer with this login already exists."]}`).

Now suppose that two requests, that both try to create a resource with the same login, arrive at (virtually) the same moment. They are handled by two separate threads. DRF will first validate that the data is correct (i.e. there is no resource with the same login yet). Because this step runs at virtually the same moment, both validations succeed. Then the first thread will create the resource and return success. The second thread now also tries to create the resource, but the database layer will raise an IntegrityError because the login is no longer unique. This error is not caught by the serializer, but ends up in the view which turns it into a 500 Internal Server Error.

This example app demonstrates the above mechanism. There is a sleep implemented just before creating the resource, to broaden the window for the race condition. The test-script (`./test.sh`) will do two (almost) simultaneous POST-requests to create a resource with the same login. The first succeeds, the seconds fails witha 500. Then a third POST-request is done with the same login to demonstrate the expected API response.

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
 *  Wrapping `concur.views.CustomerViewset.create` with an `@transaction.atomic` decorator
   * Doesn't seem to have any effect
 * Set `'OPTIONS': {'isolation_level': ISOLATION_LEVEL_SERIALIZABLE},` (also tested other isolation levels) on the default database
   * Doesn't seem to have any effect
