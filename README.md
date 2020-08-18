# arturo-stac-api ![arturo-stac-api](https://github.com/arturo-ai/arturo-stac-api/workflows/arturo-stac-api/badge.svg)
FastAPI/postgres implementation of the [STAC API specification](https://github.com/radiantearth/stac-api-spec).

## Project Structure
```
.
├── alembic             # Database migrations
│   └── versions        # Migration versions
├── stac_api            
│   ├── clients         # Database CRUD
│   ├── models          # Database and API data models
│   ├── resources       # API endpoints
│   └── utils           # FastAPI dependencies
└── tests
    ├── clients         # CRUD test cases
    ├── data            # Test data
    └── resources       # API test cases
```

## Local Development
Use docker-compose to deploy the application, migrate the database, and ingest some example data:
```bash
docker-compose build
docker-compose up
```

For local development it is often more convenient to run the application outside of docker-compose:
```bash
make docker-run
```


### Testing
The database container provided by the docker-compose stack must be running.  Run all tests:
```bash
make test
```

Run individual tests by running pytest within the docker container:
```bash
make docker-shell
$ pytest -v
```