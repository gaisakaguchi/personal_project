# coding: utf-8
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

import RPi.GPIO as GPIO
import time
import datetime

LedPin = 15    # pin15 --- led
BtnPin = 12    # pin12 --- button

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2fgloc1h244yd-ats.iot.ap-northeast-1.amazonaws.com"
CLIENT_ID = "Raspi_sakaguchi"
PATH_TO_ROOT = "./cert/AmazonRootCA1.pem"
PATH_TO_CERT = "./cert/d4529a911a-certificate.pem.crt"
PATH_TO_KEY = "./cert/d4529a911af7cec5c4c3086071917764ed33dc0aab7f7a7d04a92d7062ee14db-private.pem.key"
TOPIC = "p4p/sakaguchi"
RANGE = 20

def publish():
    myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
    myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
    myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

    myAWSIoTMQTTClient.connect()
    print('Begin Publish')
    date = str(datetime.date.today())
    nowtime = datetime.datetime.now()
    get_time = str(nowtime.hour) + ':' + str(nowtime.minute) + ':' + str(nowtime.second)
    name = "山田 太郎"
    date_of_birth=str(datetime.date(1961,8,1))
    age = "60"
    room = "403"

    data = {
        'raspiId':CLIENT_ID,
        'date':date,
        'time':get_time,
        'patient':{
            "name":name,
            "date_of_birth":date_of_birth,
            "age":age,
            "room":room
        }
    }

    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(data), 1) 
    print("Published: '" + json.dumps(data) + "' to the topic: " + "'p4p/sakaguchi'")   
    print('Publish End')
    myAWSIoTMQTTClient.disconnect()

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to make led off

def loop():
    Status = 1
    while True:
        if GPIO.input(BtnPin) == GPIO.LOW: # Check whether the button is pressed.
            if Status == 1:
                print ('...led on')
                GPIO.output(LedPin, GPIO.LOW)  # led on
                publish()
                Status = 0                
            else:
                print ('led off...')
                GPIO.output(LedPin, GPIO.HIGH) # led off
                Status = 1
        time.sleep(0.5)

def destroy():
    GPIO.output(LedPin, GPIO.HIGH)     # led off
    GPIO.cleanup()                     # Release resource
    print('-- cleanup GPIO!! --')

if __name__ == '__main__':     # Program start from here 
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
    
