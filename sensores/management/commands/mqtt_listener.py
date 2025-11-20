# sensores/management/commands/mqtt_listener.py

import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from sensores.services import registrar_lectura

# Configuración básica del broker (luego la ajustamos si es necesario)
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPICOS = [
    "planta/sensores/nivel",
    "planta/sensores/contador",
    "planta/sensores/ph",
]


class Command(BaseCommand):
    """
    Comando de Django para escuchar mensajes MQTT y
    registrar lecturas en la base de datos.
    Se ejecuta con:
        python manage.py mqtt_listener
    """
    help = "Escucha mensajes MQTT y los guarda en la BD"

    def handle(self, *args, **options):
        def on_message(client, userdata, msg):
            try:
                payload_str = msg.payload.decode()
                print(f"[MQTT] Mensaje recibido en {msg.topic}: {payload_str}")
                payload = json.loads(payload_str)

                sensor_codigo = payload.get("sensor_codigo")
                valor = payload.get("valor")

                if sensor_codigo is None or valor is None:
                    print("[MQTT][ERROR] JSON sin sensor_codigo o valor")
                    return

                registrar_lectura(sensor_codigo, valor)
                print(f"[MQTT][OK] Lectura registrada: {sensor_codigo} = {valor}")

            except Exception as e:
                print(f"[MQTT][ERROR] No se pudo procesar mensaje: {e}")

        client = mqtt.Client()
        client.on_message = on_message

        self.stdout.write(self.style.SUCCESS(
            f"Conectando a broker MQTT en {BROKER_HOST}:{BROKER_PORT}..."
        ))
        client.connect(BROKER_HOST, BROKER_PORT, 60)

        for t in TOPICOS:
            client.subscribe(t)
            self.stdout.write(self.style.SUCCESS(f"Suscrito a tópico: {t}"))

        self.stdout.write(self.style.SUCCESS("Escuchando MQTT (Ctrl+C para detener)..."))
        client.loop_forever()
