FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY .. .
CMD ["gunicorn", "wiki.wsgi:application", "--bind", "0:8000"]
