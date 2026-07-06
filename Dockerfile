FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirments.txt .

RUN pip install --no-cache-dir -r requirments.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn","--bind","0.0.0.0:5000","--workers","z","app:app"]