FROM alpine:3.7
RUN apk add --no-cache python3
RUN python3 -m pip install --no-cache-dir ovh google-api-python-client
COPY . /app
ENTRYPOINT ["python3", "/app/main.py"]