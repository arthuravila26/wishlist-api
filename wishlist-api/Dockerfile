FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY wishlist-api/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY wishlist-api/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
