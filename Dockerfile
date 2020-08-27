FROM alpine:3.12

RUN mkdir -p /app /config
RUN apk --no-cache add \
    python3 \
    py3-psutil \
    py3-paho-mqtt

COPY serverinfo2mqtt.py /app/

WORKDIR /config

CMD ["python3", "/app/serverinfo2mqtt.py"]
