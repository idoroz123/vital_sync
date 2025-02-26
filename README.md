# vital_sync app

A Health Tracker rest API built for a home assignment for Longevity AI

## Run with docker compose
Unzip folder
Go to the project directory
```bash
cd vital_sync
```
Start the app
```bash
docker compose up
```
For ease of running the app and not being production ready we're using the default database created by postgres


## Running Tests
 
In order to run the tests you need to create the test database

Run the following command (on the postgres container):

It should put you into a psql prompt

```bash
docker exec -it  <postgres_container_name> psql -U postgres -d postgres
```

In the postgres psql prompt we create the database:
```
postgres=# CREATE DATABASE postgres_test;
```
Exit the psql prompt


To run tests, run the following command
```bash

docker compose run -e "SERVER_ENV=Test" vital_sync_app python -m pytest

```
