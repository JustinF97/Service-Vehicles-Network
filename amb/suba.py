import paho.mqtt.client as mqtt
import time
import datetime
import random
task = []
po = []
avv = 3
av=0
tr = []
#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    split = msg.split(" ")
    i=0
    a = message.topic.split("/")
    print(a)
    b = list(a[3])
    try:
        if(a[3] == 'returnvehicle'):
            vehicle_returned(split)
        elif(a[3] == 'arrived'):
                check(split)
        elif(b[0] == "a"):
            try:
                c = str(b[0]+b[1])
                c =(task.index(c))
            except:
                try:
                    if(str(split[1]) != "Vehicle_Avalible"):
                        if(len(split) == 3):
                            print("Checking...")
                            savetask(split, b, po)
                except:
                    print("")
    except:
        print("Unknown topic")

def make_police(avv):
    global po
    global av
    names = ["Luka_Blackwell","Zain_Walls","Emilia_Hayden","Benjamin_Bruce","Malcolm_Sellers","Henry_Blair","Mckenna_Neal","Cohen_David","DAVE","Perla_Dickson","Tyson_Harrison","Lorena_Lane","Marcel_Horn"]
    loc = [51.67, 8.34]
    i = 0
    j=0
    for x in range (0, avv):
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
            po.append("Ambulance "+str(i))
            po.append(str(randloc1)+","+str(randloc2))
            topic="/hshl/ambulances/"
            payload = (str(po[0+j])+" "+str(randloc1)+","+str(randloc2)+" "+"True"+" "+"a"+str(i+1))
            j= j+4
            i=i+1
            av = av+1            
            print(payload)
            client.publish(topic, payload)

def savetask(split, b, po):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global av
    global task
    global tr
    b = str(b[0]+b[1])
    if(av >= 1):
        task.append(split[0])#Reason
        task.append(split[1])#Coordinates
        task.append(split[2])#Dist
        task.append(b)#ID
        x = task.index(b)
        try:
            print("Task: ")
            print(task[x])
            print(task[x-3])
            print(task[x-2])
            print(task[x-1])
        except:
            print("Error - No Tasks")
        topic = ("/hshl/ambulances/"+b)
        payload = (b+" "+"True"+" "+currentDT.strftime("%Y-%m-%d %H:%M:%S"))
        client.publish(topic, str(payload))
        topic = ("/hshl/ambulances/sendve")
        payload = (b+" "+task[x-2]+" "+po[x])
        client.publish(topic, str(payload))
        print("Send confirmation")
        tr.append(str(b))
        tr.append("True")
        av = av-1
    else:
        print("No Vehicles avalible")
        topic = ("/hshl/ambulances/"+b)
        payload = (b+" "+"False"+" "+currentDT.strftime("%Y-%m-%d %H:%M:%S"))
        client.publish(topic, str(payload))
            
def vehicle_returned(split):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global tr
    try:
        y = tr.index(split[0])
        if((str(tr[y]) == str(split[0])) and (str(tr[y+1]) == "False")):
            try:
                b = split[1]
                b = list(b.split(",", 1))
                if(isinstance(float(b[0]), float) == True):
                    if(isinstance(float(b[1]), float) == True):
                        get_coordinates(split)
                        global task
                        global av
                        x = task.index(split[0])
                        topic = ("/hshl/ambulances/"+task[x])
                        payload = (str(task[x])+" "+"Vehicle_Avalible"+" "+"True"+" "+currentDT.strftime("%Y-%m-%d %H:%M:%S"))
                        client.publish(topic, str(payload))
                        print("Vehicle Returned")
                        print(task[x])
                        task.remove(task[x-3])
                        task.remove(task[x-3])
                        task.remove(task[x-3])
                        task.remove(task[x-3])
                        tr.remove(tr[y])
                        tr.remove(tr[y])
                        av = av+1
            except:
                ("Wrong Data")
    except:
        print("Error -")

def check(split):
    try:
        b = split[1]
        b = list(b.split(",", 1))
        if(isinstance(float(b[0]), float) == True):
            if(isinstance(float(b[1]), float) == True):
                global tr
                x = tr.index(str(split[0]))
                if((str(tr[x]) == str(split[0])) and (str(tr[x+1]) == "True")):
                    tr[x+1] = "False"
                    get_coordinates(split)
    except:
        print("Wrong Data")

def get_coordinates(split):
    topic = ("/hshl/ambulances/"+split[0])
    payload = (split[1])
    client.publish(topic, str(payload))
        
        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/ambulances/returnvehicle')
    client.subscribe('/hshl/ambulances/arrived')
    i = 1
    global av
    for x in range(0, avv):
        a = ("/hshl/ambulances/a"+str(i))
        print(a)
        client.subscribe(str(a))
        i = i+1
    print("subsribed")
    make_police(avv)

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können



    
