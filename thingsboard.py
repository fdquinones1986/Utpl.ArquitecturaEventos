from paho.mqtt import client as mqtt_client
import time
import requests

# Datos de conexión a ThingsBoard
broker_address = "mqtt.thingsboard.cloud"
port = 1883
client_id = "utpl-device-client1"
username = "utpl"
password = "utpl1234"
topic = "v1/devices/me/telemetry"

# Datos de ubicacion
latitude = "-3.9867537155781045"
longitude = "-79.19940736599808"

#Obtener temperatura
def obtener_temperatura():
  url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m"
  
  respuesta = requests.get(url)
  datos = respuesta.json()
  #print(str(datos))
  temperatura = datos['current']['temperature_2m']
  return temperatura

# Función de conexión al broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Función para publicar mensajes
def on_publish(client, userdata, mid):
    print("message published")


def run():

    # Crear el cliente MQTT
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Autenticación
    client.username_pw_set(username, password)

    # Conexión al broker
    client.connect(broker_address, port)

    # Bucle principal
    while True:
        # Datos a enviar
        data = {'temperature': obtener_temperatura()}
        client.publish(topic, str(data))
        print("Sending data:", data)
        time.sleep(5)  # Ajusta el tiempo de espera según tus necesidades

    client.loop_forever()
if __name__ == '__main__':
    run()