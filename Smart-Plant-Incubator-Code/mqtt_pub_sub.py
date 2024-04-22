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

#Initialise Queues - This is thread safe!
q = Queue()
water_q = Queue()
light_q = Queue()

# MQTT pub/sub related functions

def connect_mqtt(client_id):
    '''
    Define a *UNIQUE* client_id to connect to the broker.
        This functions will connect the client and all related actions towards that clients topic to the MQTT Broker
    '''
    def on_connect(client, userdata, flags, rc, properties):
        '''
        Defines what happens when a client connects to the broker
        Triggers through callback function on_connect from paho MQTT \n
        Prints conection result - Fail or Success
         '''
        # rc is the error value - 0 is a success
        if rc == 0:
            print("Connected to MQTT Broker! {0}".format(client_id))
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(client, userdata, message):
        '''
        Define what happens when the client receives a payload from subbed topics
        Triggers through callback function on_connect from paho MQTT \n
        Adds message to queue for later retrieval
        '''

        q.put(message)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
    
    def on_water_message(client, userdata, message):
        '''
        Define what happens when the client receives a payload from the water_th topic
        See on_message...
        Adds message to water_q for later retreival
        '''
        water_q.put(message)
        # print("message received " ,str(message.payload.decode("utf-8")))
        # print("message topic=",message.topic)
    
    def on_light_message(client, userdata, message):
        '''
        Define what happens when the client receives a payload from the light_th topic
        See on_message...
        Adds message to light_q for later retreival
        '''
        light_q.put(message)
        # print("message received " ,str(message.payload.decode("utf-8")))
        # print("message topic=",message.topic)

    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    
    # Check client ID to see if payload needs to be sent to a specific queue
    if client_id == "sub_water":
        client.on_message = on_water_message
    elif client_id == "sub_light":
        client.on_message == on_light_message
    else :
        client.on_message == on_message
    
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    '''
    Publish msg to given topic by given client
    '''
    result = client.publish(topic, msg)
    # result: [0, 1] (0 is success)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def subscribe(client, topic):
    '''Subscribe to given topic with given client
    '''
    print(f"Subscribing to topic: {topic}")
    result = client.subscribe(topic)
    status = result[0]
    if status == 0:
        print(f"Successfully Subscribed")
    else:
        print(f"Subscription Failed")

def unsubscribe(client, topic):
    '''
    Unsub from given topic with given client'''
    print(f"Unsubscribbing from topic")
    client.unsubscribe(topic)
    result = client.unsubscribe(topic)
    status = result[0]
    if status == 0:
        print(f"Successfully Unsubbed")
    else:
        print(f"Unsub Failed")

def get_payload(q):
    '''
    Get payload stored in given queue
    Will loop for each message
    '''
    while not q.empty():
        message = q.get()
        if message is None:
            continue
        print("queue:", str(message.payload.decode("utf-8")))
        msg = float(message.payload.decode("utf-8)"))
        return msg

def run():
    '''
    Typical function pattern
    For use when run as main when testing
    '''
    client = connect_mqtt(client_id)
    client.loop_start()
    publish(client, topic, msg)
    subscribe(client, topic)
    time.sleep(4)
    unsubscribe(client, topic)
    client.loop_stop()

if __name__ == "__main__":
    topic = "incubator/moisture/threshold"
    client_id = "sub_water"
    #"client" + str(random.randint(0,10))
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
    
    while not water_q.empty():
        message = water_q.get()
        if message is None:
            continue
        print("Message from queue:", str(message.payload.decode("utf-8")))
        m = float(message.payload.decode("utf-8"))
        print(m)
