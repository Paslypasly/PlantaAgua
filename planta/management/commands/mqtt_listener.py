# planta/management/commands/mqtt_listener.py
import json
import paho.mqtt.client as mqtt

from django.core.management.base import BaseCommand
from django.utils import timezone

from planta.models import Estanque, InventarioBidones

TOPIC = "planta/datos"

TANQUE_CRUDO = "tanque 1"
TANQUE_PURIFICADA = "TANQUE 2"


def estado_por_pct(nivel_pct: int) -> str:
    if nivel_pct >= 95:
        return "ALERTA_95"
    elif nivel_pct >= 85:
        return "AVISO_85"
    else:
        return "OK"


def estado_por_ph(ph: float) -> str:
    return "OK" if 6.5 <= ph <= 8.5 else "ALERTA"


class Command(BaseCommand):
    help = "MQTT: tanque1(nivel) + tanque2(pH) + inventario IR (10/20)"

    def add_arguments(self, parser):
        parser.add_argument("--host", default="172.30.64.42")
        parser.add_argument("--port", type=int, default=1883)

    def handle(self, *args, **opts):
        host = opts["host"]
        port = opts["port"]

        try:
            tanque1 = Estanque.objects.get(nombre=TANQUE_CRUDO)
            tanque2 = Estanque.objects.get(nombre=TANQUE_PURIFICADA)
        except Estanque.DoesNotExist as e:
            raise SystemExit(f"Falta crear estanque en BD con nombre exacto: {e}")

        inv, _ = InventarioBidones.objects.get_or_create(id=1)

        def on_connect(client, userdata, flags, rc):
            self.stdout.write(self.style.SUCCESS(f"MQTT conectado rc={rc}. Suscrito a {TOPIC}"))
            client.subscribe(TOPIC)

        def on_message(client, userdata, msg):
            nonlocal inv
            try:
                data = json.loads(msg.payload.decode("utf-8"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"JSON inválido: {e}"))
                return

            now = timezone.now()

            # --------- TANQUE 1 -> NIVEL ----------
            nivel_pct = data.get("nivel_pct", None)
            if nivel_pct is not None:
                pct = int(nivel_pct)
                pct = max(0, min(100, pct))
                nivel_agua_l = (float(tanque1.capacidad_litros) * pct) / 100.0 if tanque1.capacidad_litros else 0.0
                tanque1.nivel_agua = round(nivel_agua_l, 2)
                tanque1.estado = estado_por_pct(pct)
                tanque1.updated_at = now
                tanque1.save(update_fields=["nivel_agua", "estado", "updated_at"])

            # --------- TANQUE 2 -> pH ----------
            ph = data.get("ph", None)
            ph_raw = data.get("ph_raw", None)
            if ph is not None:
                tanque2.ph_actual = round(float(ph), 2)
                if ph_raw is not None:
                    tanque2.ph_raw = int(ph_raw)
                tanque2.estado = estado_por_ph(float(ph))
                tanque2.updated_at = now
                tanque2.save(update_fields=["ph_actual", "ph_raw", "estado", "updated_at"])

            # --------- INVENTARIO -> IR (bidones acumulados) ----------
            # ESP manda bidones acumulados (0,1,2,3...).
            bidones = data.get("bidones", None)
            if bidones is not None:
                inv = InventarioBidones.objects.get(id=1)  # refresca por si usuario cambió modo/tipo
                esp_now = int(bidones)

                prev = int(inv.ultimo_contador_esp or 0)
                delta = esp_now - prev

                if delta > 0:
                    # aplica delta según selección actual
                    modo = inv.modo_pendiente
                    typ = inv.tipo_pendiente

                    if modo == "NONE":
                        inv.ultima_accion = f"ESP +{delta} pero sin modo (NONE). (ESP {esp_now})"
                    else:
                        if typ == "L10":
                            if modo == "IN":
                                inv.stock_10 += delta
                                inv.ultima_accion = f"ESP +{delta} aplicado a IN/L10. (10={inv.stock_10}, 20={inv.stock_20})"
                            else:
                                inv.stock_10 = max(0, inv.stock_10 - delta)
                                inv.ultima_accion = f"ESP +{delta} aplicado a OUT/L10. (10={inv.stock_10}, 20={inv.stock_20})"
                        else:  # L20
                            if modo == "IN":
                                inv.stock_20 += delta
                                inv.ultima_accion = f"ESP +{delta} aplicado a IN/L20. (10={inv.stock_10}, 20={inv.stock_20})"
                            else:
                                inv.stock_20 = max(0, inv.stock_20 - delta)
                                inv.ultima_accion = f"ESP +{delta} aplicado a OUT/L20. (10={inv.stock_10}, 20={inv.stock_20})"

                    inv.ultimo_contador_esp = esp_now
                    inv.updated_at = now
                    inv.save(update_fields=["stock_10", "stock_20", "ultimo_contador_esp", "ultima_accion", "updated_at"])

                elif delta < 0:
                    # el ESP se reinició (contador volvió a 0). No tocamos stock.
                    inv.ultimo_contador_esp = esp_now
                    inv.ultima_accion = f"ESP reiniciado (prev={prev} -> now={esp_now}). No se ajusta stock."
                    inv.updated_at = now
                    inv.save(update_fields=["ultimo_contador_esp", "ultima_accion", "updated_at"])

            self.stdout.write(
                f"OK | {tanque1.nombre}: {tanque1.nivel_agua}L estado={tanque1.estado} | "
                f"{tanque2.nombre}: pH={tanque2.ph_actual} estado={tanque2.estado} | "
                f"INV: 10={InventarioBidones.objects.get(id=1).stock_10} 20={InventarioBidones.objects.get(id=1).stock_20} "
                f"modo={InventarioBidones.objects.get(id=1).modo_pendiente}/{InventarioBidones.objects.get(id=1).tipo_pendiente} "
                f"esp={InventarioBidones.objects.get(id=1).ultimo_contador_esp}"
            )

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        self.stdout.write(f"Conectando a MQTT {host}:{port} ...")
        client.connect(host, port, 60)
        client.loop_forever()
