FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PYTHONPATH "${PYTHONPATH}:/"

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
