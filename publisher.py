#!/usr/bin/python

import paho.mqtt.client as mqtt
import numpy as np
import time
#import hashlib
import subprocess
import json

broker_address = "localhost"

def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_address,1883,60)
client.loop_start()

time.sleep(0.05)
degrees = np.random.random_sample()
toa = np.random.random_sample()
humidity = np.random.random_sample()

sample = "sample"

data ={
    'sample': sample
    }

msg = json.dumps(data)

client.publish("devices/" + str(computeruuid), msg.encode('utf-8'), 1, 1)
client.disconnect(client)
