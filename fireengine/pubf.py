import paho.mqtt.client as mqtt
import time
import datetime

task = "Bob"
c1 = "32.51"
c2 = "28.31"
reason = "Dead"
sendtask = (str(task)+" "+str(c1)+","+str(c2)+" "+reason)
task1 = "Hans"
c11 = "213.52"
c21 = "53.234"
reason1 = "Still_Alive"
sendtask1 = (str(task1)+" "+str(c11)+","+str(c21)+" "+reason1)


#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/firefighters/')
    client.subscribe('/hshl/firefighters/f1')
    client.subscribe('/hshl/firefighters/f2')
    client.subscribe('/hshl/firefighters/f3')
    print(sendtask)
    topic = "/hshl/firefighters/f1"
    client.publish(topic, sendtask)
    print(sendtask1)
    topic1 = "/hshl/firefighters/f2"
    client.publish(topic1, sendtask1)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    split = msg.split(" ")
    i=0
    a = message.topic
    a = (a.split("/"))
    print(a)
    if(split[1] == "True"):
        print("True")#id and True or Flase
    elif(a[3] == "f1"):
        print("F1")
    elif(a[3] == "f2"):
        print("F2")
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

