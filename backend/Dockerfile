FROM python:3.10.7

COPY ./src /app/src
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r  requirements.txt

EXPOSE 8000

ENV API_KEY=BigProfiles-API
ENV MONGODB_URL="mongodb://localhost:27017"

CMD ["gunicorn", "--log-level", "INFO", "-b", "0.0.0.0:8000", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]