import paho.mqtt.client as mqtt
import time
import datetime
import random
task = []
po = []
av = 3
#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    split = msg.split(" ")
    print(split)
    i=0
    a = message.topic.split("/")
    print(a)
    b = list(a[3])
    print(b)
    if(b[0] == "p"):
        savetask(split)

    elif(a[3] == 'stop'):
        print("")
        
    elif(a[3] == 'get_av'):
        get_av(av)
        
    elif(a[3] == 'get_cc'):###doesn't do anything as long as the vehicles return istantly
        get_coordinates(task, split, po)###

    elif(a[3] == 'returnvehicle'):
        vehicle_returned(split)

    else:
        print("Unknown topic")

def make_police(av):
    global po
    names = ["Luka_Blackwell","Zain_Walls","Emilia_Hayden","Benjamin_Bruce","Malcolm_Sellers","Henry_Blair","Mckenna_Neal","Cohen_David","DAVE","Perla_Dickson","Tyson_Harrison","Lorena_Lane","Marcel_Horn"]
    loc = [51.67, 8.34]
    i = 0
    j=0
    for x in range (0, av):
        if (len(names) >= 2):
            n1=random.randint(0, (len(names)-1))
            po.append(names[n1])
            names.remove(po[0+j])
            n2=random.randint(0, (len(names)-1))
            po.append(names[n2])
            names.remove(po[1+j])
            randloc1 = loc[0]+(random.randint(-9, 9)/10)
            randloc2 = loc[1]+(random.randint(-9, 9)/10)
            randloc1 = round(randloc1, 2)
            randloc2 = round(randloc2, 2)
            po.append("Policecar "+str(i))
            po.append(str(randloc1)+","+str(randloc2))
            topic="/hshl/polices/"
            payload = (str(po[0+j])+" "+str(randloc1)+","+str(randloc2)+" "+"isFree"+" "+"p"+str(i))
            j= j+4
            i=i+1
            print(payload)
            client.publish(topic, payload)
    print(po) 

def savetask(split):
    global av
    global task
    try:
        print(task.index(split[3]))
        print("Vehicle not avalible")
    except:
        if (av  >= 1):
            task.append(split[0])#Task
            task.append(split[1])#Coordinates
            task.append(split[2])#Reason
            task.append(split[3])#ID
            x = task.index(split[0])
            topic = "/hshl/polices/vehiclesend"
            payload = (task[x+3]+" "+"inUse")
            client.publish(topic, str(payload))
            av = av-1
            get_av(av)
        else:
            print("No vehicles")
            
def vehicle_returned(split):
    global task
    global av
    x = task.index(split[0])
    topic = "/hshl/polices/vehiclereturned"
    payload = (str(task[x])+" "+"isFree")
    client.publish(topic, str(payload))
    print(task)
    task.remove(task[x-3])
    task.remove(task[x-3])
    task.remove(task[x-3])
    task.remove(task[x-3])
    print(task)
    av = av+1
    get_av(av)
        


def get_av(av):
    topic = "/hshl/polices/av"
    a = (av)
    client.publish(topic, str(av))

def get_coordinates(task, split, po): #Task senden
    if len(task) >=1 :
        c = []
        cv = []
        cc = []
        x = task.index(split[0])
        c = task[1+x].split(",")
        c[0] = float(c[0])
        c[1] = float(c[1])
        cv = po[x+4].split("2")
        cv[0] = float(cv[0])
        cv[1] = float(cv[1])
        cc[0] = (c[0]+cv[0])/2
        cc[1] = (c[1]+cv[1])/2
        topic = "/hshl/polices/cc"
        payload = (str(cc[0])+","+str(cc[1]))
        client.publish(topic, str(payload))
    else:
        topic = "/hshl/polices/cc"
        payload = ("No_vehilces_send")
        client.publish(topic, str(payload))
        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polices/')#Abonnieren des Topics (Hier die jeweiligen Topics einfügen die vorgegeben sind)
    client.subscribe('/hshl/polices/get_av')
    client.subscribe('/hshl/polices/get_cc')
    client.subscribe('/hshl/polices/stop')
    client.subscribe('/hshl/polices/returnvehicle')
    i = 0
    global av
    for x in range(0, av):
        a = ("/hshl/polices/p"+str(i))
        print(a)
        client.subscribe(str(a))
        i = i+1
    print("subsribed")
    make_police(av)

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können



    
