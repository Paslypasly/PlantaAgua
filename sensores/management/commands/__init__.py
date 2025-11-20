# sensores/management/commands/mqtt_listener.py
import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from sensores.services import registrar_lectura


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPICOS = [
    "planta/sensores/nivel",
    "planta/sensores/contador",
    "planta/sensores/ph",
]


class Command(BaseCommand):
    help = "Escucha mensajes MQTT y los guarda en la BD"

    def handle(self, *args, **options):

        def on_message(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode())
                sensor_codigo = payload.get("sensor_codigo")
                valor = payload.get("valor")

                registrar_lectura(sensor_codigo, valor)
                print(f"[OK] Lectura registrada desde MQTT: {sensor_codigo} = {valor}")

            except Exception as e:
                print(f"[ERROR] No se pudo procesar mensaje MQTT: {e}")

        client = mqtt.Client()
        client.on_message = on_message

        client.connect(BROKER_HOST, BROKER_PORT, 60)

        for t in TOPICOS:
            client.subscribe(t)
            print(f"Suscrito a {t}")

        print("Escuchando MQTT...")
        client.loop_forever()
