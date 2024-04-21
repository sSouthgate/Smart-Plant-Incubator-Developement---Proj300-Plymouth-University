import json
import paho.mqtt.client as mqtt
import time
from adc_sensor import AdcSensor

moisture = AdcSensor(2)

broker = "localhost"
port = 1883
topic = "incubator/moisture"

client_id = 'publish-1'
username = "auzon"
password = "2203"

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

def publish(client):

    msg_count = 1
    while True:
        time.sleep(1)
        #msg = f"messages: {msg_count} light: {light.adc_sensor}"
        msg = moisture.adc_sensor
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()