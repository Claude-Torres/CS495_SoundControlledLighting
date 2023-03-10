import RPi.GPIO as GPIO
import threading

global manDecThresh
manDecThresh = 1

class LEDThread(threading.Thread):
    def __init__(self):
        super(LEDThread, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        
        while True:
            # light LED's

            if manDecThresh > .5:
                GPIO.output(light, GPIO.HIGH)
            elif manDecThresh <= .5:
                GPIO.output(light, GPIO.LOW)
        GPIO.output(light, GPIO.LOW)
            
    def stop(self):
        self.stopped = True

class Potenti(threading.Thread):
    def __init__(self):
        super(Potenti, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        
        while True:
            # light LED's
            manDecThresh = GPIO.input(potentiometer)
            
    def stop(self):
        self.stopped = True
        

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

power = 2
potentiometer = 12
light = 18

GPIO.setup(potentiometer, GPIO.IN)

GPIO.setup(light, GPIO.OUT)
GPIO.output(light, GPIO.HIGH)

potenti = Potenti()
potenti.start()

ledthread = LEDThread()
ledthread.start()


            
