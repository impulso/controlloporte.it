FROM python:3.13-alpine3.23

RUN apk add --no-cache nmap && adduser -D -H -u 10001 scanner

WORKDIR /app
COPY worker.py /app/worker.py

USER scanner
EXPOSE 8080

CMD ["python", "/app/worker.py"]
