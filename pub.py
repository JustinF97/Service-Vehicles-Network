import paho.mqtt.client as mqtt
import time
import datetime
import json

task = [""]
coordinates1 = [0]
coordinates2 = [0]
vehicleamount = [0]
task = input("Enter Task: ")
coordinates1 = input("Enter coordinates: ")
coordinates2 = input("Enter coordinates: ")
vehicleamount = input("Enter vehicle amount: ")
a = [0]
b = [0]
c = [0]
d = [0]
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe([('/hshl/polices/police 1', 2),
                      ('/hshl/polices/send', 2),
                      ('/hshl/polices/update', 2),
                      ('/hshl/polices/nova', 2),
                      ('/hshl/polices/neva', 2),
                      ('/hshl/polices/avalible_vehilces', 2),
                      ('/hshl/polices/coordinates', 2)
                      ]) 
    request_task (task, coordinates1, coordinates2, vehicleamount)
    
def ask_for_avalible_vehicles():
    data = {
        "topic": "hshl/police/avalible vehicles"}
    client.publish("/hshl/polices/avalible vehicles", json.dumps(data))

def ask_for_current_coordinates():
    data = {
        "topic": "hshl/police/current coordinates"}
    client.publish("/hshl/polices/current coordinates", json.dumps(data))

def request_task (task, coordinates1, coordinates2, vehicleamount):
    data = {
        "task": task,
        "coord1": coordinates1,
        "coord2": coordinates2,
        "vamount": vehicleamount,
        "topic": "hshl/police/task"}
    client.publish("/hshl/polices/task", json.dumps(data))

def register_police(data, coordinates1, coordinates2, vehicleamount, task, a, b, c, d):
    js = json.loads(data)
    a = js["task"]
    b = js["coord1"]
    c = js["coord2"]
    d = js["vamount"]
    if str(task) != str(a):
        stop()
    elif coordinates1 != b:
        stop()
    elif coordinates2 != c:
        stop()
    elif vehicleamount != d:
        stop()
    else:
        data = {
            "Confirm": "Confirm",
            "topic": "/hshl/polices/confirm"}
        client.publish("/hshl/polices/confirm", json.dumps(data))

def stop():
    data = {
            "STOP": "STOP",
            "topic": "/hshl/police/stop"}
    client.publish("/hshl/polices/stop", json.dumps(data))

def recive(data):
    js = json.loads(data)
    vehicles = js["vehicles"] #Vehicles that have been sent
    avalible_vehilces = js["avalible_vehilces"] #amount of avalible vehicles at base
    topic = js["topic"]

def avalible_vehilces(data):
    js = json.loads(data)
    av = js["avalible_vehilces"]

def save_coordinates(data):
    js = json.loads(data)
    coordinates = js["cco"]

def on_message(client, userdata, msg):
    msgp = str(msg.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msgp))
    if(msg.topic.endswith('police 1')):
        register_police(msg.payload, coordinates1, coordinates2, vehicleamount, task, a, b, c, d)
        
    if(msg.topic.endswith('send')):
        recive(msg.payload)

    if(msg.topic.endswith('nova')):
    if(msg.topic.endswith('neva')):
        
    if(msg.topic.endswith('avalible_vehilces')):
        avalible_vehilces(msg.payload)

    if(msg.topic.endswith('coordinates')):
        save_coordinates(msg.payload)
        
    if(msg.topic.endswith('update')):
        print("Vehicle has arrived")
        
#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können

