import pyaudio
import math
import struct

def open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=2):
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
    decibel = calculate_decibel(data, chunk)
    return decibel

p1, stream1 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=2)
#p2, stream2 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=1)
#p3, stream3 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=2)
#p4, stream4 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=3)

while True:
    decibel1 = get_decibel(p1, stream1, chunk=1024)
    #decibel2 = get_decibel(p2, stream2, chunk=1024)
    #decibel3 = get_decibel(p3, stream3, chunk=1024)
    #decibel4 = get_decibel(p4, stream4, chunk=1024)
    print(f"Microphone 1: {decibel1}")
    #print(f"Microphone 1: {decibel1}, Microphone 2: {decibel2}, Microphone 3: {decibel3}, Microphone 4: {decibel4}")

close_stream(p1, stream1)
#close_stream(p2, stream2)
#close_stream(p3, stream3)
#close_stream(p4, stream4)
