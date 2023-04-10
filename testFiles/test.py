import pyaudio

# Set parameters
CHUNK = 8192
FORMAT = pyaudio.paInt16
RATE = 44100
CHANNELS = 1

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the first microphone on card 3
stream1 = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK,
                 input_device_index=11)


# Open the only microphone on card 4
stream2 = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK,
                 input_device_index=12)


# Read and process audio data in a loop
while True:
    # Read audio data from the first microphone
    data1 = stream1.read(CHUNK, exception_on_overflow=False)
    print("data1: ")
    print(data1)

    # Read audio data from the second microphone
    data2 = stream2.read(CHUNK, exception_on_overflow=False)
    print("data2: ")
    print(data2)

    # Process audio data here...

# Stop the streams and terminate PyAudio
stream1.stop_stream()
stream1.close()
stream2.stop_stream()
stream2.close()
p.terminate()