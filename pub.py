import paho.mqtt.client as mqtt
import time
import datetime

task = "Bob"
c1 = "32"
c2 = "28"
reason = "Dead"
vid = "p1"
sendtask = (str(task)+" "+str(c1)+","+str(c2)+" "+reason+" "+vid)

#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polices/')
    client.subscribe('/hshl/polices/vehiclesend')
    client.subscribe('/hshl/polices/vehiclearrived')
    client.subscribe('/hshl/polices/av')
    client.subscribe('/hshl/polices/cc')
    client.subscribe('/hshl/polices/vehiclereturned')
    print(sendtask)
    topic = "/hshl/polices/p1"
    client.publish(topic, sendtask)

def ask_for_avalible_vehicles():
    topic = "/hshl/polices/get_av"
    client.publish(topic, topic)

def ask_for_current_coordinates():
    topic = "/hshl/polices/get_cc"
    client.publish(topic, topic)

def stop():
    topic = "/hshl/polices/stop"
    client.publish(topic, topic)

def avalible_vehilces(split):
    av = split[0]
    print(av)

def save_coordinates(split):
    sc = split[0]
    print(sc)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    split = msg.split(" ")
    i=0
    a = message.topic
    a = (a.split("/"))
    print(a)

    if(a[3] == 'av'):
        avalible_vehilces(split)

    elif(a[3] == 'cc'):
        save_coordinates(split)
        
    elif(a[3] == 'vehiclearrived'):
        print("Vehicle has arrived")
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

