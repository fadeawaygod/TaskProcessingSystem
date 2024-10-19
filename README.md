# High-Throughput Task Processing System

## Description
This project provides a high-throughput task processing system using asynchronous APIs to send and consume tasks from a message queue, ensuring scalability, performance and reliability.

- [db diagram](app/doc/diagram/db_table_diagram.md)
- [sequence diagram](app/doc/diagram/sequence_diagram.md)

# Debug with VS Code Locally
## Environment
- Ubuntu 20.04
- Python 3.11
- PostgresSQL server at 127.0.0.1:5432
  - db name: `task-processing-system-dev`
- Redis server at 127.0.0.1:6379

## Debug Steps(api server)
1. cd into this folder.
2. run `pip install -r requirements.txt`.
3. set up `.vscode/launch.json`, the variables defined [here](app/core/config.py), check example below.
4. start debugging
5. check the swagger doc [here](http://0.0.0.0:8000/docs)

### example of api server configuration in launch.json of VS Code
```json
 {
            "name": "Python: API Server Local DB",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--port",
                "8000",
                "--host",
                "0.0.0.0"
            ],
            "env": {
                "DO_INIT_DB": "true",
                "POSTGRES_HOST": "127.0.0.1",
                "POSTGRES_PORT": "5432",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "xxx",
                "POSTGRES_DB": "task-processing-system-dev",
                "REDIS_HOST": "127.0.0.1",
                "REDIS_PORT": "6379",
                "EVENT_BUS_REDIS_HOST": "127.0.0.1",
                "EVENT_BUS_REDIS_PORT": "6379",
                "LONG_TIME_CACHE_REDIS_HOST": "127.0.0.1",
                "LONG_TIME_CACHE_REDIS_PORT": "6379",
                "LONG_TIME_IS_REDIS_CLUSTER": "false",
                "EVENT_BUS_IS_REDIS_CLUSTER": "false",
                "BACKEND_CORS_ORIGINS": "http://localhost:3000",
                "PORT": "8000",
                "LOGGER_LEVEL": "DEBUG",
                "API_ROOT_PATH": "",
            },
            "justMyCode": true,
        }
```
## Debug Steps(api server worker)
1. cd into this folder.
2. run `pip install -r requirements.txt`.
3. set up `.vscode/launch.json`, the variables defined [here](app/core/config.py), check example below.
4. start debugging

### example of api server worker configuration in launch.json of VS Code
```json
 {
            "name": "Python: API Server Local DB",
            "type": "debugpy",
            "request": "launch",
            "module": "python",
            "args": [
                "app.worker_main:app",
            ],
            "env": {
                "DO_INIT_DB": "true",
                "POSTGRES_HOST": "127.0.0.1",
                "POSTGRES_PORT": "5432",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "xxx",
                "POSTGRES_DB": "task-processing-system-dev",
                "REDIS_HOST": "127.0.0.1",
                "REDIS_PORT": "6379",
                "EVENT_BUS_REDIS_HOST": "127.0.0.1",
                "EVENT_BUS_REDIS_PORT": "6379",
                "LONG_TIME_CACHE_REDIS_HOST": "127.0.0.1",
                "LONG_TIME_CACHE_REDIS_PORT": "6379",
                "LONG_TIME_IS_REDIS_CLUSTER": "false",
                "EVENT_BUS_IS_REDIS_CLUSTER": "false",
                "BACKEND_CORS_ORIGINS": "http://localhost:3000",
                "PORT": "8000",
                "LOGGER_LEVEL": "DEBUG",
                "API_ROOT_PATH": "",
            },
            "justMyCode": true,
        }
```

# Notice

## DB Migrations
### create migration files
If you change the model files in `app/database/models`,

1. `pip install alembic`
2. cd into this folder.
3. set up env variables, the variables defined [here](app/core/config.py).
4. create a migration file by:
```
alembic revision --autogenerate -m "${revision_message}"
```
4. check the generated file in `migrations/versions`
### do db migration
1. set the env variable: `DO_INIT_DB` to true, and run the server.

# API Server Worker

## Build Docker Images
It can be compiled locally through the following syntax
```
docker build -t task-processing-system-worker -f Dockerfile.worker .
```

> Note: Please adjust Tag according to actual needs