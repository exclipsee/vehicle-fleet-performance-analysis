FROM python:3.11-slim

WORKDIR /app

# system deps (kept minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

ENV PYTHONUNBUFFERED=1

# expose typical ports
EXPOSE 8501 8502 8000

CMD ["bash", "-c", "echo 'Use docker-compose to run services' && sleep infinity"]
