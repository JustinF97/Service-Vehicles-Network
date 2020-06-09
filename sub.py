import paho.mqtt.client as mqtt
import time
import datetime
import json
import random


k = [0]
task = [["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"]]
vic1 = []
vic2 = []
vic3 = []
people = ["Luka Blackwell","Zain Walls","Emilia Hayden","Benjamin Bruce","Malcolm Sellers","Henry Blair","Mckenna Neal","Cohen David","DAVE","Perla Dickson","Tyson Harrison","Lorena Lane","Marcel Horn"]
vehicle_track = [[0],["Policeccar 1","Policecar 2","Policecar 3"], ["-","-","-"]]


#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, msg):
    msgp = str(msg.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msgp))
    
    if(msg.topic.endswith("task")):
        savetask(msg.payload)
        
    elif(msg.topic.endswith('confirm')):
        confirm(msg.payload, k)

    elif(msg.topic.endswith('stop')):
        
    elif(msg.topic.endswith('avalible vehicles')):
        get_av(vehicle_track)
        
    elif(msg.topic.endswith('current coordinates')):###doesn't do anything as long as the vehicles return istantly
        get_coordinates(task)###



def savetask(data):
    global k
    global task
    i=0
    for x in range(0, len(task[0])):
        if task[0][i] == "-":
            k = i
            js = json.loads(data)
            task[0][i] = js["task"]
            task[1][i] = js["vamount"]
            task[2][i] = js["coord1"]
            task[3][i] = js["coord2"]
            data = {
                "task": task[0][i],
                "coord1": task[2][i],
                "coord2": task[3][i],
                "vamount": task[1][i],
                "topic": "/hshl/polices/police 1"}
            client.publish("/hshl/polices/police 1", json.dumps(data))
            break
        i = i+1

def confirm(data, k):
    global task
    global vehicle_track
    sendvehicle(k)
    data = {
        "task":  task[0][k],
        "vehicles": task[4+k],
        "info": "Vehicles send to coordinates",
        "av": (len(vehicle_track[1])-vehicle_track[0][0]),
        "topic": "/hshl/polices/send"}
    client.publish("/hshl/polices/send", (json.dumps(data)))
    data = {
        "task":  task[0][k],
        "vehicles": task[4+k],
        "info": "Vehicles arived",
        "topic": "/hshl/polices/update"}
    client.publish("/hshl/polices/update", (json.dumps(data)))
    returnvehicle(k)#can instead be used when reciving a message

def sendvehicle(k):
    global task
    global vehicle_track
    global people
    global vic1
    global vic2
    global vic3
    i = 0
    if int(vehicle_track[0][0]) == int(len(vehicle_track[1])):#no vehicles 
        data = {
        "send":  "No vehicles",
        "topic": "/hshl/polices/nova"}
        client.publish("/hshl/polices/nova", json.dumps(data))
    elif int(task[1][k]) > int(len(vehicle_track[1]))-int(vehicle_track[0][0]):
        data = {
        "send":  "Not enough vehicles",
        "topic": "/hshl/polices/neva"}
        client.publish("/hshl/polices/neva", json.dumps(data))
    else:
        j=0
        for x in range(0, int(task[1][k])):
            for x in range(0, len(vehicle_track[1])):
                if task[4+k][j] == "-":
                    if  vehicle_track[1][i] != ("-") :
                        vehicle_track[2][i] = (vehicle_track[1][i])
                        vehicle_track[1][i] = ("-")
                        vehicle_track[0][0] = (vehicle_track[0][0] + 1)
                        task[4+k][j] = (vehicle_track[2][i])
                        if i == 0:
                            vic1.append(people[0])
                            people.remove(vic1[0])
                            vic1.append(people[0])
                            people.remove(vic1[1])
                        if i == 1:
                            vic2.append(people[0])
                            people.remove(vic2[0])
                            vic2.append(people[0])
                            people.remove(vic2[1])
                        if i == 2:
                            vic3.append(people[0])
                            people.remove(vic3[0])
                            vic3.append(people[0])
                            people.remove(vic3[1])
                i=i+1
            j=j+1

def returnvehicle(k):
    global task
    global vehicle_track
    global people
    global vic1
    global vic2
    global vic3
    i=0
    if vehicle_track[0][0] == 0:
        print("--")
        #All vehicles are allready home
    else:
        j=0
        for x in range(0, int(task[1][k])):
            for x in range(0, len(vehicle_track[2])):
                if task[4+k][j] == vehicle_track[2][i]:
                    vehicle_track[1][i] = vehicle_track[2][i]
                    vehicle_track[2][i] = "-"
                    vehicle_track[0][0] = (vehicle_track[0][0] - 1)
                    if i == 0:
                        people.append(vic1[0])
                        vic1.remove(vic1[0])
                        people.append(vic1[0])
                        vic1.remove(vic1[0])
                    elif i == 1:
                        people.append(vic2[0])
                        vic2.remove(vic2[0])
                        people.append(vic2[0])
                        vic2.remove(vic2[0])
                    elif i == 2:
                        people.append(vic3[0])
                        vic3.remove(vic3[0])
                        people.append(vic3[0])
                        vic3.remove(vic3[0])
                i=i+1
            j=j+1
        task[0][k] = "-"
        task[1][k] = "-"
        task[2][k] = "-"
        task[3][k] = "-"
        task[4][k] = "-"
        get_av(vehicle_track)

def get_av(vehicle_track):
    data = {
        "avalible_vehilces": (len(vehicle_track[1])-vehicle_track[0][0]),
        "topic": "/hshl/polices/avalible_vehilces"}
    client.publish("/hshl/polices/avalible_vehilces", (json.dumps(data)))
        

def get_coordinates(task):
    i=0
    for x in range(0, len(task[0])):
        if task[0][i] != "-":
                   rand1 = randint(0, 9)/10
                   rand2 = randint(0, 9)/10
                   data = {
                        "task": task[0][i],
                        "cco": [51+rand1, 8+rand2],
                        "topic": "/hshl/polices/coordinates"}
                   client.publish("/hshl/polices/coordinates", (json.dumps(data)))
        elif (task[0][0] == "-" and task[0][1] == "-" and task[0][2] == "-" ):
            data = {
                    "task": "No Tasks",
                    "cco": [51, 8],
                    "topic": "/hshl/polices/coordinates"}
            client.publish("/hshl/polices/coordinates", (json.dumps(data)))
            break
        i=i+1

#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe([('/hshl/polices/task', 2),
                      ('/hshl/polices/avalible vehicles', 2),
                      ('/hshl/polices/current coordinates', 2),
                      ('/hshl/polices/stop', 2),
                      ('/hshl/polices/confirm', 2)])#Abonnieren des Topics (Hier die jeweiligen Topics einfügen die vorgegeben sind)

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können
