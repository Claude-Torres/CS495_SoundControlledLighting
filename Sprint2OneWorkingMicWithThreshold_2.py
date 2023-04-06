import pyaudio
import math
import struct
import RPi.GPIO as GPIO
import threading
from gpiozero import MCP3008
import numpy as np

def open_stream(chunk=1024, sample_rate=44100, num_channels=128, device_index=2):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                     channels=num_channels,
                     rate=sample_rate,
                     input=True,
                     frames_per_buffer=chunk,
                     input_device_index=device_index)
    return p, stream

def close_stream(p, stream):
    stream.stop_stream()
    stream.close()
    p.terminate()

def calculate_decibel(data, chunk):
    data_int = struct.unpack(f"{chunk // 2}h", data)
    rms = math.sqrt(sum([(x ** 2) for x in data_int]) / chunk)
    decibel = 20 * math.log10(rms)
    return decibel

def get_decibel(p, stream, chunk):
    data = stream.read(chunk, exception_on_overflow=False)
    data = data[:chunk]
    assert len(data) == chunk, f"Input data is {len(data)} bytes, expected {chunk} bytes"
    decibel = calculate_decibel(data[:chunk], chunk)
    return decibel

'''
##Mic -- TODO
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

for i in range(num_devices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    if device_info.get('maxInputChannels') > 0:
        print("Input Device id ", i, " - ", device_info.get('name'))
        print("Max input channels: ", device_info.get('maxInputChannels'))
        if device_info.get('name') == "mic1":
            print("\nMIC 1 here!\n")
        if device_info.get('name') == "mic2":
            print("\nMIC 2 here!\n")
        if device_info.get('name') == "mic3":
            print("\nMIC 3 here!\n")
'''

p1, stream1 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=11)
p2, stream2 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=12)
#p3, stream3 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=14)
#p4, stream4 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=3)

global manDecThresh
global decibel1
global ml
manDecThresh = 100
decibel1 = 1


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
            # curremntly a constant .5 decibal input
            if  decibel1 > manDecThresh:
                GPIO.output(light, GPIO.HIGH)
            elif manDecThresh >= decibel1:
                GPIO.output(light, GPIO.LOW)
        GPIO.output(light, GPIO.LOW)
            
    def stop(self):
        self.stopped = True

# thread to check potentiomerter status 
class Potenti(threading.Thread):
    def __init__(self):
        super(Potenti, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        global ml
        ml = False
        while True:
            # light LED's
            if potentiometer.value > 10:
                ml = False
                manDecThresh = potentiometer.value * 100
            else:
                ml = True
            #print(manDecThresh)
            
    def stop(self):
        self.stopped = True
        
# set up GPIO interface
#GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# label each part's pins
#light = 18
light = 24
potentiometer = MCP3008(0)

# set sig as input for gpio
#GPIO.setup(potentiometer, GPIO.IN)

# set light to on and output
GPIO.setup(light, GPIO.OUT)
GPIO.output(light, GPIO.HIGH)

# start 1 of each thread
potenti = Potenti()
potenti.start()

ledthread = LEDThread()
ledthread.start()

decVals = []

while True:
    
    decibel1 = get_decibel(p1, stream1, chunk=1024)
    decibel2 = get_decibel(p2, stream2, chunk=1024)
    decibel3 = 45
    decibel4 = 40

    if len(decVals) < 7000:
        decVals.append(decibel1)
        decVals.append(decibel2)
        decVals.append(decibel3)
        decVals.append(decibel4)
    elif ml:
        print("here")
        
        decVals = np.array(decVals)
        manDecThresh = np.median(decVals)
        print(f"\n\nmanDecThresh: {manDecThresh}\n\n")
        break
    
    print(f"Microphone 1: {decibel1}, Microphone 2: {decibel2}, Microphone 3: {decibel3}, Microphone 4: {decibel4}, manDecThresh: {manDecThresh}")

close_stream(p1, stream1)
close_stream(p2, stream2)
#close_stream(p3, stream3)
#close_stream(p4, stream4)


