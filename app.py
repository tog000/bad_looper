import soundcard as sc
import numpy as np
import time
import threading

sample_rate = 48000

# usb_speaker = sc.get_speaker('Unitek')
usb_speaker = sc.get_speaker('Built')
usb_mic = sc.get_microphone('Unitek')
print(usb_speaker)
print(usb_mic)

recording = False
playing = False
data = np.array([])

def keyboard_input():
  global recording
  global playing
  global data
  while True:
    input("Press to start recording")
    data = np.array([])
    recording = True
    input("Press to stop recording")
    recording = False

def record_thread():
  global recording
  global playing
  global data
  with usb_speaker.player(samplerate=sample_rate, blocksize=4800) as sp, \
        usb_mic.recorder(samplerate=sample_rate, blocksize=9600) as mic:
    while True:
      sample = mic.record(numframes=2400)
      if recording:
          data = np.append(data, sample[:,0])
      else:
        if len(data) > 0:
          print("Playing")
          sp.play(data)


thread1 = threading.Thread(target=keyboard_input)
thread1.start()

thread2 = threading.Thread(target=record_thread)
thread2.start()