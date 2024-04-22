import paho.mqtt.client as mqtt
import time
from queue import Queue
import random

# Define Broker Parameters
# Broker Address
broker = "localhost"
port = 1883
# Broker Credentials
username = "auzon"
password = "2203"

#Initialise Queue - This is thread safe!
q = Queue()

def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc, properties):
        # rc is the error value - 0 is a success
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(client, userdata, message):
        q.put(message)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)

    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def subscribe(client, topic):
    print(f"Subscribing to topic: {topic}")
    result = client.subscribe(topic)
    status = result[0]
    if status == 0:
        print(f"Successfully Subscribed")
    else:
        print(f"Subscription Failed")

def unsubscribe(client, topic):
    print(f"Unsubscribbing from topic")
    client.unsubscribe(topic)
    result = client.unsubscribe(topic)
    status = result[0]
    if status == 0:
        print(f"Successfully Unsubbed")
    else:
        print(f"Unsub Failed")

# def get_message(client_id):
#     def on_message(client, userdata, message):
#         q.put(message)
#         print("message received " ,str(message.payload.decode("utf-8")))
#         print("message topic=",message.topic)
    
#     client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
#     client.on_message = on_message
#     while not q.empty():
#         message = q.get()
#         if message is None:
#             continue
#         print("Message from queue:", str(message.payload.decode("utf-8")))
#         message = int(message.payload.decode("utf-8"))
#         print(m)
#     # return message

def run():
    client = connect_mqtt(client_id)
    client.loop_start()
    publish(client, topic, msg)
    subscribe(client, topic)
    time.sleep(4)
    unsubscribe(client, topic)
    client.loop_stop()

if __name__ == "__main__":
    topic = "test/topic"
    client_id = "client" + str(random.randint(0,10))
    print(client_id)
    msg = random.randint(0,10)
    print(msg)
    run()
    while not q.empty():
        message = q.get()
        if message is None:
            continue
        print("Message from queue:", str(message.payload.decode("utf-8")))
        m = int(message.payload.decode("utf-8"))
        print(m)