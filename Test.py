import paho.mqtt.client as mqtt
import time
import datetime
import random
import threading

task = []

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    split = msg.split(" ")
    print(split)
    a = message.topic.split("/")
    if (a[3] == "vehiclesend"):
        randomtime(split)


def randomtime(split):
    global task
    task.append(split[0])
    x = task.index(split[0])
    try:
        if(str(task[x] == "p1")):
            t1 = (random.randint(5, 10))
            timer1 = threading.Timer(t1, callback1)
            timer1.start()  # after 60 seconds, 'callback' will be called
        elif(str(task[x] == "p2")):
            t2 = (random.randint(5, 10))
            timer2 = threading.Timer(t2, callback2)
            timer2.start()  # after 60 seconds, 'callback' will be called
        elif(str(task[x] == "p3")):
            t3 = (random.randint(5, 10))
            timer3 = threading.Timer(t3, callback3)
            timer3.start()  # after 60 seconds, 'callback' will be called
        else:
            print("No Valid ID")
    except:
        print("Error")

def callback1():
    global task
    topic = "/hshl/polices/returnvehicle"
    payload = "p1"
    client.publish(topic, str(payload))
    task.remove("p1")

def callback2():
    global task
    topic = "/hshl/polices/returnvehicle"
    payload = "p2"
    client.publish(topic, str(payload))
    task.remove("p2")

def callback3():
    global task
    topic = "/hshl/polices/returnvehicle"
    payload = "p3"
    client.publish(topic, str(payload))
    task.remove("p3")      

#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polices/')#Abonnieren des Topics (Hier die jeweiligen Topics einfügen die vorgegeben sind)
    client.subscribe('/hshl/polices/vehiclesend')


#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können
