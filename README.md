# drfconcurrency
Simple Django app to play around with concurrent requests to DRF

## Running the example
```
git clone https://github.com/gertjanol/drfconcurrency.git
cd drfconcurrency
# Start container for database first to give it a chance to boot before starting Django
docker-compose up -d db
docker-compose up -d web

./test.sh
```
