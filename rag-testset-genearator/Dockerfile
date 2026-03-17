FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/

RUN  pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["-c", "from main import create_test_set; create_test_set()"]

