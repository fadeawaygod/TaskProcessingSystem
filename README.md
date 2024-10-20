# High-Throughput Task Processing System

## Description
This project provides a high-throughput task processing system using asynchronous APIs to send and consume tasks from a message queue, ensuring scalability, performance and reliability.

## Project structure

**Task Processing System**
==========================

**Application Directory**
------------------------

* `app/`: This is the main application directory, containing all the code for the task processing system.
	+ **Core**: This directory contains the core functionality of the application.
		- `core/`: This directory contains the core application logic, including configuration, database, and exceptions.
			- **Database**: This directory contains the database-related code, including CRUD operations and models.
				- `database/`: This directory contains the database-related code.
					- **CRUD Operations**: This directory contains the CRUD (Create, Read, Update, Delete) operations for the database.
						- `crud/`: This directory contains the CRUD operations.
					- **Models**: This directory contains the database models.
						- `models/`: This directory contains the database models.
			- **Enumerations**: This directory contains enumerations used throughout the application.
				- `enum/`: This directory contains enumerations.
			- **Exceptions**: This directory contains custom exceptions used throughout the application.
				- `exceptions/`: This directory contains custom exceptions.
			- **Helper Functions**: This directory contains helper functions used throughout the application.
			- **Logging**: This directory contains logging-related code.
				- `logging/`: This directory contains logging-related code.
			- **Middleware**: This directory contains middleware-related code.
				- `middleware/`: This directory contains middleware-related code.
			- **Utilities**: This directory contains utility functions used throughout the application.
				- `utils/`: This directory contains utility functions.
	+ **API**: This directory contains API-related code.
		- `api/`: This directory contains API-related code.
			- **Version 1**: This directory contains the API version 1 code.
				- `v1/`: This directory contains the API version 1 code.
					- **Endpoints**: This directory contains the API endpoints.
						- `endpoints/`: This directory contains the API endpoints.
					- **Schema**: This directory contains the API schema.
						- `schema/`: This directory contains the API schema.
	+ **Worker**: This directory contains worker-related code.
		- `worker/`: This directory contains worker-related code.
			- **Task Handlers**: This directory contains task handlers.
				- `task_handler/`: This directory contains task handlers.

**Tests**
--------

* `tests/`: This directory contains unit tests for the application.

**Documentation**
-------------

* `app/doc/`: This directory contains documentation for the application.
	+ `diagram/`: This directory contains diagrams for the application.

## Diagram
- [db diagram](app/doc/diagram/db_table_diagram.md)
- [sequence diagram](app/doc/diagram/sequence_diagram.md)

# Run with Docker Compose
## Environment
- Ubuntu 20.04
- Docker 25.0.2

## Run Steps
1. cd into this folder.
2. run `docker build -t task-processing-system .`.
3. run `docker build -t task-processing-system-worker -f Dockerfile.worker .`.
4. run `docker-compose up -d`.
5. To stop, run `docker-compose down`.

# Debug with VS Code Locally
## Environment
- Ubuntu 20.04
- Python 3.8
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
    "name": "Python: API Server Worker Local DB",
    "type": "debugpy",
    "request": "launch",
    "program": "app/worker_main.py",
    "console": "integratedTerminal",
    "env": {
        "DO_INIT_DB": "true",
        "POSTGRES_HOST": "127.0.0.1",
        "POSTGRES_PORT": "5432",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "xxx",
        "POSTGRES_DB": "task-processing-system-dev",
        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": "6379",
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
