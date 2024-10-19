FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PRIVATE_PYPI_URL=http://172.31.69.231:80
ENV PRIVATE_PYPI_DOMAIN=172.31.69.231

ENV PYTHONPATH "${PYTHONPATH}:/"

RUN apt-get update
RUN apt-get install sox -y

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install --extra-index-url ${PRIVATE_PYPI_URL} --trusted-host ${PRIVATE_PYPI_DOMAIN} --no-cache-dir -r requirements.txt

COPY ./app /app
