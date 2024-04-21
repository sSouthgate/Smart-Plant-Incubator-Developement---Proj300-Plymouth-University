import paho.mqtt.client as mqtt
import time
import random
from adc_sensor import AdcSensor

# Define Broker Parameters
broker = "localhost"
port = 1883
#topic = "incubator/moisture"
client_id = 'publish-1'
username = "auzon"
password = "2203"

# Define Sensor
moisture = AdcSensor(2)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    #time.sleep(1)
    #msg = f"messages: {msg_count} light: {light.adc_sensor}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run(topic, msg):
    client = connect_mqtt()
    client.loop_start()
    publish(client, topic, msg)
    client.loop_stop()

if __name__ == "__main__":
    topic = "topic/test"
    msg = random.randint(0,10)
    run(topic, msg)
    