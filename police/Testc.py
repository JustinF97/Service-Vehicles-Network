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
    a = message.topic.split("/")
    print(a)
    if (a[3] == "sendve"):
        try:
            b = split[1]
            b = list(b.split(",",1))
            c = split[2]
            c = list(c.split(",",1))
            if(isinstance(float(b[0]), float) == True):
                if(isinstance(float(c[1]), float) == True):
                    randomtime(split)
        except:
            print("Wrong data")


def randomtime(split):
    global task
    task.append(split[0])
    task.append(split[1])
    task.append(split[2])
    x = task.index(split[0])
    try:
        if(str(task[x] == "p1")):
            t1 = (random.randint(1, 10))
            timer1 = threading.Timer(t1, callback1)
            timer1.start()  # after 60 seconds, 'callback' will be called
        if(str(task[x] == "p2")):
            t2 = (random.randint(1, 10))
            timer2 = threading.Timer(t2, callback2)
            timer2.start()  # after 60 seconds, 'callback' will be called
        if(str(task[x] == "p3")):
            t3 = (random.randint(1, 10))
            timer3 = threading.Timer(t3, callback3)
            timer3.start()  # after 60 seconds, 'callback' will be called
        else:
            print("No Valid ID")
    except:
        print("Error -")

def callback1():
    global task
    try:
        x = task.index("p1")
        topic = "/hshl/polices/arrived"
        payload = ("p1"+" "+str(task[1+x]))
        client.publish(topic, str(payload))
        t11 = (random.randint(1, 10))
        timer11 = threading.Timer(t11, callback11)
        timer11.start()  # after 60 seconds, 'callback' will be called
    except:
        print("Error1")

def callback2():
    global task
    try:
        x = task.index("p2")
        topic = "/hshl/polices/arrived"
        payload = ("p2"+" "+str(task[1+x]))
        client.publish(topic, str(payload))
        t22 = (random.randint(1, 10))
        timer22 = threading.Timer(t22, callback22)
        timer22.start()  # after 60 seconds, 'callback' will be called
    except:
        print("Error2")

def callback3():
    global task
    try:
        x = task.index("p3")
        topic = "/hshl/polices/arrived"
        payload = ("p3"+" "+str(task[1+x]))
        client.publish(topic, str(payload))
        t33 = (random.randint(1, 10))
        timer33 = threading.Timer(t33, callback33)
        timer33.start()  # after 60 seconds, 'callback' will be called
    except:
        print("Error3")

#---------------------------------------
def callback11():
    global task
    try:
        x = task.index("p1")
        topic = "/hshl/polices/returnvehicle"
        payload = ("p1"+" "+str(task[x+2]))
        client.publish(topic, str(payload))
        task.remove(task[x])
        task.remove(task[x])
        task.remove(task[x])
    except:
        print("Error11")
        
def callback22():
    global task
    try:
        x = task.index("p2")
        topic = "/hshl/polices/returnvehicle"
        payload = ("p2"+" "+str(task[x+2]))
        client.publish(topic, str(payload))
        task.remove(task[x])
        task.remove(task[x])
        task.remove(task[x])
    except:
        print("Error22")

def callback33():
    global task
    try:
        x = task.index("p3")
        topic = "/hshl/polices/returnvehicle"
        payload = ("p3"+" "+str(task[x+2]))
        client.publish(topic, str(payload))
        task.remove(task[x])
        task.remove(task[x])
        task.remove(task[x])
    except:
        print("Error33")

#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polices/sendve')


#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können
