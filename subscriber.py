#!/usr/bin/python
import psycopg2
from psycopg2 import connect, Error
#from config import config
import paho.mqtt.client as mqtt
import datetime
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("devices/#",0)

def on_message(client, userdata, msg):
    Date = datetime.datetime.utcnow()
    message= msg.payload.decode()
    try:
            #print the JSON Message with Data and Topic
            #print(str(Date) + ": " + msg.topic + " " + str(message))
            #concatenate the SQL string
            sql_string = "INSERT INTO sampl (json)\nVALUES ('{0}')".format(message)
            #execute the INSERT statement
            cur = conn.cursor()
            cur.execute(sql_string)
            #commit the changes to the database
            conn.commit()
            print("Finished writing to PostgreSQL")
    except (Exception, Error) as err:
            print("\npsycopg2 connect error:", err)
            print("Could not insert " + message + " into Postgresql DB")

#Set up a client for Postgresql DB
try:
    #read connection parameters
    #connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
        user="postgres",
        password="123456",
        host="127.0.0.1",
        port="5432",
        database="deneme"
    )
    #create a cursor
    cur = conn.cursor()
    #execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    #cur.execute()
    #display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
#Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()

#set last will message
#client.will_set('Postgresql_Paho-Client/lastwill','Last will message', 1, True)

client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect("localhost", 1883, 60)
        connOK = True
    except:
        connOK = False
    time.sleep(2)
#Blocking loop to the Mosquitto broker
client.loop_forever()
