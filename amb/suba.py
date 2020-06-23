import paho.mqtt.client as mqtt
import time
import datetime
import random
import json
task = []
po = []
coor = []
avv = 3
av=0
tr = []
#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    i=0
    global task
    a = message.topic.split("/")
    print(a)
    b = list(a[3])
    try:
        if(a[3] == 'returnvehicle'):
            split = msg.split(" ")
            print(split)
            vehicle_returned(split, po)
        elif(a[3] == 'arrived'):
            split = msg.split(" ")
            print(split)
            check(split, task, po)
        elif(b[0] == "a"):
            try:
                js = json.loads(message.payload)
                if (js["self"] == "true"):
                    g = 1
            except:
                print("Checking...")
                savetask(message.payload, b, po)
    except:
        print("Unknown topic")

def make_amb(avv):
    global po
    global av
    global coor
    names = ["Luka_Blackwell","Zain_Walls","Emilia_Hayden","Benjamin_Bruce","Malcolm_Sellers","Henry_Blair","Mckenna_Neal","Cohen_David","Perla_Dickson","Tyson_Harrison","Lorena_Lane","Marcel_Horn"]
    loc = [51.67, 8.34]
    i = 0
    j=0
    for x in range (0, avv):
        if (len(names) >= 2):
            for x in range(0, 2):
                n1=random.randint(0, (len(names)-1))
                po.append(names[n1])
                k = po.index(names[n1])
                names.remove(po[k])
            randloc1 = loc[0]+random.randint(-7, 9)+(random.randint(-9, 9)/10)
            randloc2 = loc[1]+random.randint(-7, 9)+(random.randint(-9, 9)/10)
            randloc1 = round(randloc1, 2)
            randloc2 = round(randloc2, 2)
            po.append("a"+str(i+1))
            po.append(str(randloc1)+","+str(randloc2))
            loc = [float(randloc1), float(randloc2)]
            coor.append(loc)
            coor.append(loc)
            coor.append("a"+str(i+1))
            topic="/hshl/ambulances/"
            currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
            data = {
                "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "driver_name": str(po[0+j]),
                "location": loc,
                "isFree" : True,
                "id": "a"+str(i+1),
                "topic": topic}
            print(str(po[j])+" "+str(po[j+1])+" "+str(po[j+2])+" "+str(po[j+3]))
            j= j+4
            i=i+1
            av = av+1     
            client.publish(topic, json.dumps(data))
            a = ("/hshl/ambulances/a"+str(i))
            print(a)
            client.subscribe(str(a))
        

def savetask(data, b, po):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global av
    global task
    global tr
    global coor
    b = str(b[0]+b[1])
    try:
        c = (task.index(b))
        print("Vehicle not avalible")
        topic = ("/hshl/ambulances/"+b)
        data = {
        "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
        "id": b,
        "isFree": False,
        "self": "true",
        "acc" : "False",
        "location": coor[coor.index(b)-1],
        "reasons": task[task.index(b)-3],
        "driver_name": po[po.index(b)-2],
        "topic": topic}
        client.publish(topic, json.dumps(data))
    except:
        if(av >= 1):
            js = json.loads(data)
            task.append(js["reasons"])#Reason
            a = js["location"]
            a = str(a[0])+","+str(a[1])
            task.append(a)#Coordinates
            task.append("Dist")#Dist
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
            data = {
                "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "id": b,
                "isFree": False,
                "self": "true",
                "acc" : "True",
                "location": coor[coor.index(b)-1],
                "reasons": task[task.index(b)-3],
                "driver_name": po[po.index(b)-2],
                "av": av,
                "topic": topic}
            client.publish(topic, json.dumps(data))
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
            data = {
                "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "id": b,
                "isFree": False,
                "self": "true",
                "acc" : "False",
                "location": coor[coor.index(b)-1],
                "reasons": task[task.index(b)-3],
                "driver_name": po[po.index(b)-2],
                "topic": topic}
            client.publish(topic, json.dumps(data))
            
def vehicle_returned(split, po):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global tr
    try:
        x = tr.index(split[0])
        if(str(tr[x+1]) == "False"):
            try:
                b = split[1]
                b = list(b.split(",", 1))
                if(isinstance(float(b[0]), float) == True):
                    if(isinstance(float(b[1]), float) == True):
                        global task
                        global av
                        global coor
                        coor[int(coor.index(tr[x]))-1] = [float(b[0]), float(b[1])]
                        topic = ("/hshl/ambulances/"+str(tr[x]))
                        data = {
                            "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                            "self": "true",
                            "location": coor[coor.index(str(tr[x]))-1],
                            "isFree" : True,
                            "reasons": task[task.index(str(tr[x]))-3],
                            "driver_name": po[po.index(str(tr[x]))-2],
                            "av": av,
                            "id": str(tr[x]),
                            "topic": topic}
                        client.publish(topic, json.dumps(data))
                        print("Vehicle Returned")
                        y = task.index(tr[x])
                        task.remove(task[y-3])
                        task.remove(task[y-3])
                        task.remove(task[y-3])
                        task.remove(task[y-3])
                        tr.remove(tr[x])
                        tr.remove(tr[x])
                        av = av+1
            except:
                ("Wrong Data")
    except:
        print("Error -")

def check(split, task, po):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    try:
        b = split[1]
        b = list(b.split(",", 1))
        if(isinstance(float(b[0]), float) == True):
            if(isinstance(float(b[1]), float) == True):
                global tr
                global coor
                x = tr.index(str(split[0]))
                if(str(tr[x+1]) == "True"):
                    coor[int(coor.index(tr[x]))-1] = [float(b[0]), float(b[1])]
                    topic = ("/hshl/ambulances/"+str(tr[x]))
                    data = {
                        "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                        "location": coor[coor.index(str(tr[x]))-1],
                        "id": str(tr[x]),
                        "self": "true",
                        "isFree": False,
                        "reasons": task[task.index(str(tr[x]))],
                        "driver_name": po[po.index(str(tr[x]))-2],
                        "topic": topic}
                    client.publish(topic, json.dumps(data))
                    tr[x+1] = "False"
    except:
        print("Wrong Data")
        
        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/ambulances/returnvehicle')
    client.subscribe('/hshl/ambulances/arrived')
    make_amb(avv)

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können



    
