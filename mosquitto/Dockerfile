FROM eclipse-mosquitto

COPY mosquitto.conf /mosquitto/config/mosquitto.conf

EXPOSE 1883
EXPOSE 9001

ENTRYPOINT ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
