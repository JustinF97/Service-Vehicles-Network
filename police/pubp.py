import paho.mqtt.client as mqtt
import time
import datetime
import json





#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polices/')
    client.subscribe('/hshl/polices/p1')
    client.subscribe('/hshl/polices/p2')
    client.subscribe('/hshl/polices/p3')
    data = {
        "task": "Bob",
        "location": [float(32.51), float(28.31)],
        "reasons": "heart_attack",
        "topic": "hshl/polices/p1"}
    topic = "/hshl/polices/p1"
    client.publish(topic, json.dumps(data))
    data = {
        "task": "Hans",
        "location": [float(213.52), float(53.234)],
        "reasons": "accident",
        "topic": "hshl/polices/p2"}
    topic = "/hshl/polices/p2"
    client.publish(topic, json.dumps(data))
    data = {
        "task": "Bob",
        "location": [float(32.51), float(28.31)],
        "reasons": "heart_attack",
        "topic": "hshl/polices/p1"}
    topic = "/hshl/polices/p1"
    client.publish(topic, json.dumps(data))

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    i=0
    a = message.topic
    a = (a.split("/"))
    print(a)
    if(a[3] == "p1"):
        print("P1")
    elif(a[3] == "p2"):
        print("P2")
    else:
        print("Unknown topic")


#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können

