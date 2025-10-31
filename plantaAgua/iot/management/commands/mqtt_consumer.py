import json, signal, sys
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
import paho.mqtt.client as mqtt
from usuarios.models import Planta
from iot.models import Sensor
from iot.services import registrar_medicion_y_evaluar

def parse_payload(raw: bytes):
    s = raw.decode("utf-8", errors="ignore").strip()
    if s.startswith("{") and s.endswith("}"):
        try:
            obj = json.loads(s)
            ts = obj.get("ts")
            if ts:
                try: ts = datetime.fromisoformat(ts.replace("Z","+00:00"))
                except: ts = None
            return {"valor": obj.get("value"), "unit": obj.get("unit"), "lote": obj.get("lote"), "ts": ts}
        except json.JSONDecodeError:
            return None
    try:
        return {"valor": float(s), "unit": None, "lote": None, "ts": None}
    except ValueError:
        return None

class Command(BaseCommand):
    help = "Suscribe a MQTT y guarda mediciones"

    def handle(self, *args, **opts):
        conf = getattr(settings, "MQTT", {})
        host, port = conf.get("HOST","localhost"), int(conf.get("PORT",1883))
        subs = conf.get("SUBSCRIPTIONS",[("planta/+/sensor/+",1)])
        user, pwd, tls = conf.get("USERNAME"), conf.get("PASSWORD"), conf.get("TLS", False)

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="django-consumer")
        if user and pwd: client.username_pw_set(user, pwd)
        if tls: client.tls_set()

        def on_connect(c, u, flags, rc, props):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS(f"[MQTT] Conectado {host}:{port}"))
                for t,qos in subs:
                    c.subscribe(t, qos=qos); self.stdout.write(self.style.HTTP_INFO(f"[MQTT] Subscrito: {t}"))
            else:
                self.stdout.write(self.style.ERROR(f"[MQTT] rc={rc}"))

        def on_message(c, u, msg):
            try:
                topic = msg.topic  # planta/SM01/sensor/tds
                parts = topic.split("/")
                if len(parts) < 4: return
                _, planta_codigo, _, sensor_tipo = parts[:4]
                parsed = parse_payload(msg.payload)
                if not parsed or parsed["valor"] is None:
                    self.stdout.write(self.style.WARNING(f"[MQTT] payload inválido {topic}"))
                    return
                try:
                    planta = Planta.objects.get(codigo=planta_codigo)
                except Planta.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"[MQTT] planta desconocida: {planta_codigo}"))
                    return
                sensor = Sensor.objects.filter(planta=planta, topico_mqtt=topic).first() or \
                         Sensor.objects.filter(planta=planta, tipo=sensor_tipo).first()
                if not sensor:
                    self.stdout.write(self.style.WARNING(f"[MQTT] sensor no encontrado: {topic}"))
                    return
                med = registrar_medicion_y_evaluar(
                    planta=planta, sensor=sensor, valor=parsed["valor"],
                    unidad=parsed["unit"] or sensor.unidad, lote_codigo=parsed["lote"], ts=parsed["ts"]
                )
                self.stdout.write(self.style.SUCCESS(
                    f"[OK] {sensor.tipo.upper()}={med.valor} {med.unidad} [{planta.codigo}] lote={parsed['lote'] or '-'}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[ERR] on_message: {e}"))

        client.on_connect = on_connect
        client.on_message = on_message

        def _exit(signum, frame):
            try: client.disconnect()
            finally: sys.exit(0)

        signal.signal(signal.SIGINT, _exit)
        signal.signal(signal.SIGTERM, _exit)

        client.connect(host, port, int(conf.get("KEEPALIVE",60)))
        client.loop_forever(retry_first_connection=True)
