import paho.mqtt.client as mqtt
import time
import datetime
import random
task = []
po = []
k=0
av = 3
#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, msg):
    msgp = str(msg.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msgp))
    split = str(msg).split(" ")
    
    if(msg.topic.endswith == "task"):
        savetask(split, av)
        
    elif(msg.topic.endswith('confirm')):
        confirm(split, task)

    elif(msg.topic.endswith('stop')):
        print("")
        
    elif(msg.topic.endswith('avalible vehicles')):
        get_av(av)
        
    elif(msg.topic.endswith('current coordinates')):###doesn't do anything as long as the vehicles return istantly
        get_coordinates(task, split, po)###

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
            n2=random.randint(0, (len(names)-1))
            po.append(names[n1])
            names.remove(po[0+j])
            po.append(names[n2])
            names.remove(po[1+j])
            randloc1 = loc[0]+(random.randint(-9, 9)/10)
            randloc2 = loc[1]+(random.randint(-9, 9)/10)
            randloc1 = round(randloc1, 2)
            randloc2 = round(randloc2, 2)
            po.append("Policecar "+str(i))
            po.append(str(randloc1)+","+str(randloc2))
            polices = (str(po[0+j])+" "+str(randloc1)+","+str(randloc2)+" "+"isFree"+" "+"p"+str(i))
            j= j+4
            i=i+1
            print(polices)
            client.publish("/hshl/polices/coordinates", polices)
    print(po) 

def savetask(split, av):
    if (av  >= 1):
        global task
        global k
        task.append(split[0])#Task
        task.append(split[1])#Coordinates
        task.append(split[2])#ID
        conf = (str(task[0+k])+" "+str(task[1+k])+" "+str(task[2+k]))
        k = k+3
        print(conf)
        client.publish("/hshl/polices/", conf)
    else:
        print("No vehicles")

def confirm(split, task):
    global k
    global av
    x = task.index(split[0])
    send = (task[x+2]+" "+"inUse")
    client.publish("/hshl/polices/", send)
    av = av-1
    get_av(av)
    send = (task[x+2]+" "+"arrived")
    client.publish("/hshl/polices/", send)
    send = (task[x+2]+" "+"returned")
    client.publish("/hshl/polices/", send)
    task.remove(task[x])
    task.remove(task[x])
    task.remove(task[x])
    k = k-3
    av = av+1
    get_av(av)

def get_av(av):
    client.publish("/hshl/polices/", av)

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
        ccc = (str(cc[0])+","+str(cc[1]))
        client.publish("/hshl/polices/", ccc)
    else:
        a = "No vehilces send"
        client.publish("/hshl/polices/", a)
        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polices/')#Abonnieren des Topics (Hier die jeweiligen Topics einfügen die vorgegeben sind)
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



    
