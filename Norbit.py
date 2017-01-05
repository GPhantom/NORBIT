
from __future__ import print_function
from nanpy import (ArduinoApi, SerialManager)
from nanpy import Servo
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
import os
import sys
import json
import apiai

CLIENT_ACCESS_TOKEN = 'Your_api.ai_Agent_Token_Here'


def default():
    lcd.clear()
    lcd.message("  N.O.R.B.I.T")

    
lcd = Adafruit_CharLCD()
lcd.begin(16,1)
lcd.clear()
default()
x = Servo(3)





try:
    connection = SerialManager()
    a = ArduinoApi (connection = connection)

except:
    print ("Failed to connect to the arduino")
    lcd.message("     ERROR\nConnectionFailed") 


def say(msg):
    m = '"' + msg + '"'
    os.system('espeak -s 125 -v en+m3 -p 70 ' + m +  ' 2>/dev/null')

pir = 5
val = 0
a.pinMode(pir, a.INPUT)
print ("N.O.R.B.I.T")



def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    while True:
        
        print(u"> ", end=u"")
        user_message = raw_input()
            
        if user_message == "calibrate":
            calibrate()
            main()
        elif user_message == "exit":
            print ("exiting...")
            sleep(1)
            lcd.clear()
            exit()
        elif user_message == "sleep":
            print ("Sleeping...zzz")
            while True:
                try:
                    slp()
                except KeyboardInterrupt:
                    lcd.clear()
                    break
            print ("\n")    
            wakeup()

        
        request = ai.text_request()
        request.query = user_message

        response = json.loads(request.getresponse().read())

        result = response['result']
        action = result.get('action')
        actionIncomplete = result.get('actionIncomplete', False)

        print(u"< %s" % response['result']['fulfillment']['speech'])
        say(response['result']['fulfillment']['speech'])
        
        shout(response['result']['fulfillment']['speech'])
        
        sleep(0.5)
        

        if action is not None:
            if action == u"send_message":
                parameters = result['parameters']

                text = parameters.get('text')
                message_type = parameters.get('message_type')
                parent = parameters.get('parent')

                print (
                    'text: %s, message_type: %s, parent: %s' %
                    (
                        text if text else "null",
                        message_type if message_type else "null",
                        parent if parent else "null"
                    )
                )

                if not actionIncomplete:
                    print(u"...Sending Message...")
                    break



def motion():
    val = a.digitalRead(pir)
    
    if val == 1:
        return True
    else:
        return False



def slp():
    lcd.clear()
    
    shout("   zzzzzZZZZZ")
    m = motion()
    if m == True:
        wakeup()
    



def calibrate():
    lcd.clear()
    x.write(0)
    lcd.message("Position: Right")
    sleep(1)
    lcd.clear()
    x.write(90)
    lcd.message("Position: Center")
    sleep(1)
    lcd.clear()
    x.write(180)
    lcd.message("Position: Left")
    sleep(1)
    lcd.clear()
    x.write(90)
    shout(" [+]Calibrating\n      Done")
    sleep(1)
    lcd.clear()
    default()
    


def wakeupgesture():
    x.write(90)
    x.write(45)
    sleep(0.5)
    x.write(135)
    sleep(0.5)
    x.write(90)



def wakeup():
    wakeupgesture()
    lcd.clear()
    shout("Hey There!")
    lcd.clear()
    shout("Sorry, i was sleeping zzzz")
    lcd.clear()
    shout("What can i do for u?")
    sleep(2)
    default()
    main()



def T():
    terminal = str(raw_input("N.O.R.B.I.T >> "))    
    if terminal == "calibrate":
        calibrate()
        
    elif terminal == "exit":
        print ("exiting...")
        sleep(1)
        lcd.clear()
        exit()
    elif terminal == "sleep":
        print ("Sleeping...zzz")
        while True:
            try:
                slp()
            except KeyboardInterrupt:
                lcd.clear()
                break
        print ("\n")    
        wakeup()
                
            
    else:
        print ("Command not found!")
        T()
        


def shout(msg):
    lcd.clear()
    p = 0
    line = 1
    l = len(msg)
    for letter in str(msg):
        if p == 16:
            if line == 1:
                lcd.message("\n")
                p = 0
                line = 2
            elif line == 2:
              lcd.clear()
              p = 0
              line = 1
              continue
        
        lcd.message(letter)
        p = p + 1
        
        sleep(0.1)

        
def terminalshout(msg):
    for letter in str(msg):
        print (letter, end="")
        sleep(0.1)


main()


