import json
import paho.mqtt.client as mqtt
from shared.config import CONFIG

client = mqtt.Client()
connected = False

def connect():
    global connected
    try:
        client.connect(CONFIG["MQTT"]["BROKER"], CONFIG["MQTT"]["PORT"])
        connected = True
        print("[MQTT] Ligado ao broker.")
    except Exception as e:
        print(f"[MQTT] Erro ao ligar: {e}")
        connected = False

def send_mqtt_message(data):
    if not connected:
        connect()

    if connected:
        payload = json.dumps(data)
        try:
            client.publish(CONFIG["MQTT"]["TOPIC"], payload)
            print(f"[MQTT] Publicado: {payload}")
        except Exception as e:
            print(f"[MQTT] Erro ao enviar: {e}")
