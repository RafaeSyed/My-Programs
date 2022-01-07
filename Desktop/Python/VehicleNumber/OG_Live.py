#MAIN CODE OF ST
import pyaudio
import wave
import os
from PIL import Image


from matplotlib import pyplot as plt
from math import log
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import read
import numpy as np
import cv2

from time import sleep
import datetime
from subprocess import call

import sys

#RECORDING THE AUDIO AND STORING IT
#now=datetime.now()
#print("now =",now)
#dt_string= now.strftime("%d%m%Y %H:%M:%S")
#print("date and time =",dt_string)
#The following code comes from markjay4k as referenced below
form_1 = pyaudio.paInt16
chans=1
samp_rate = 16000
chunk = 4096
record_secs = 10   #record time
dev_index = 2
wav_output_filename = './test1.wav'


audio = pyaudio.PyAudio()

#setup audio input stream
stream=audio.open(format = form_1,rate=samp_rate,channels=chans, input_device_index = dev_index, input=True, frames_per_buffer=chunk)
print("recording")
frames=[]

for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data=stream.read(chunk,exception_on_overflow = False)
    frames.append(data)

print("finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

#creates wave file with audio read in
#Code is from the wave file audio tutorial as referenced below
wavefile=wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

#plays the audio file
os.system("aplay test1.wav")

#CONVERTS ANALOG TO DIGITAL AND CALCULATES DB VALUE
#amp2fcode

samprate, wavdata= read('./test1.wav')
chunks = np.array_split(wavdata,880 )
dbs = [((10* np.log10( np.sqrt(np.mean(abs(chunk**2))))))for chunk in chunks]
#dbs = [(20* np.log10( np.mean(abs(chunk))))for chunk in chunks]
print(dbs)
dbss=30
minii=min(dbs)
maxii=max(dbs)
for ii in  range(len(dbs)):
    dbs[ii]= ((dbs[ii]-minii)*50/3)+40
    
   # dbs[ii]= ((dbs[ii]-minii)*50/(maxii-minii))+40
    print(dbs[ii])
for ii in  range(len(dbs)):
    if dbs[ii] >= dbss:
        #TRIGGERS THE CAMERA AND STORING IT
        camera = cv2.VideoCapture(0)
        car_cascade = cv2.CascadeClassifier('./cars.xml')
        while True:
            ret, frames = camera.read()
            gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 1)
            for (x,y,w,h) in cars:
                cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.imshow('video2',frames)
            
            if cv2.waitKey(33) == 27:
                break
#cv2.destroyAllWindows()
        

#vid_cod = cv2.VideoWriter_fourcc(*'XVID')
#output = cv2.VideoWriter("videos/cam_video.mp4", vid_cod, 20.0, (640,480))

        
        #return_value, image = camera.read()
        #cv2.imwrite('/home/pi/Documents/example/opencv.png', image)
        
        while(camera.isOpened()):
            ret, frame = camera.read()
            if ret:
                font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
                #font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
                dt = str(datetime.datetime.now())
                frame = cv2.putText(frame, dt,
                            (10, 100),
                            font, 0.8,
                            (255, 255, 255),
                            4, cv2.LINE_8)
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1)
                
                if key == 'q' or key == 27:
                    break
            else:
                break

    vid.release()    
            
    
        
        
        
        #del(camera)
        #timestampMessage= dt_string
        #timestampCommand="/usr/bin/convert "+ "/home/pi/Documents/example/pi.jpg"+" -pointsize 32 -fill black -annotate +700+700 '" + timestampMessage + "' " + "/home/pi/Documents/pi.jpg"
        #saveFile=open('/home/pi/Documents/example/lala.txt','w')
        #saveFile.write(str(dbs[ii])+'\n')
        #saveFile.write(dt_string)
        #saveFile.close()
        #break
    image.open('/home/pi/Documents/example/opencv.png')
    
# PLOTTING THE SIGNAL
spf = wave.open("./test1.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, "Int16")
fs = spf.getframerate()

# If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)


Time = np.linspace(0, len(signal) / fs, num=len(signal))

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(Time, signal)
plt.ylim(0.0,100.0)
#plt.show()
plt.savefig("./plot.png")



sleep(10)
#im =Image.open(r"/home/pi/Documents/example/opencv.png")
#Image.show('/home/pi/Documents/example/opencv.png')


#REMOVING THE FILES FOR STORAGE PURPOSES
os.remove("./test1.wav")
os.remove("./opencv.png")
os.remove("./lala.txt")
os.remove("./plot.png")
os.remove("./plot.jpg")




