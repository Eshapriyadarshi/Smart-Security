
import concurrent.futures
import sounddevice 
import pyrebase
import numpy as np
import scipy.signal
import timeit
import python_speech_features
import RPi.GPIO as GPIO

firebaseConfig = {
        'apiKey': "AIzaSyCbWArvVFJStGZ_ijIx68ATffVpbM7TTTI",
        'authDomain': "my-application-3d098.firebaseapp.com",
        'projectId': "my-application-3d098",
        'storageBucket': "my-application-3d098.appspot.com",
        "databaseURL": "https://my-application-3d098-default-rtdb.firebaseio.com",
        'messagingSenderId': "407511304872",
        'appId': "1:407511304872:web:3745d4015435cf48c3109d",
        'measurementId': "G-9K5E03NK12"
        }
firebase=pyrebase.initialize_app(firebaseConfig)

from tflite_runtime.interpreter import Interpreter

def gsmsms():
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    import json
    import requests
    from twilio.rest import Client

    sid = "ACc0fb57fa6433e387d673ff1b68cec152"
    auth_token = "4e9d26580a70d2f4b5d1a1d6a11c8b4c"

    client = Client(sid, auth_token)
    cred = credentials.Certificate("service.json")
    firebase_admin.initialize_app(cred)

    db  =firestore.client()

    result = db.collection('USERS').document("sharath").get()
    result = (result.to_dict())
    p1 = (result['phone1'])
    p2 = (result['phone2'])
    p3 = (result['phone3'])
    client.messages.create(body="Help! Help! Help!",from_="+19547152741",to="{}".format(p1))
def recordaudio():  
    import datetime 
    
    import sounddevice
    from scipy.io.wavfile import write

    security = "sharath"
    name = "/audio.wav"
    
    cloudfilename=security+name

    #record audio
    fs = 44100
    second = 10
    print("recording")
    record_voice = sounddevice.rec(int(second * fs),samplerate=fs,channels = 2)
    sounddevice.wait()
    write("output.wav",fs,record_voice)
    print("stop recording")
    
    #store the audio in firebase
    

    storage=firebase.storage()
    file="output.wav"
    storage.child(cloudfilename).put(file)
def gps():
    
    db = firebase.database()
    data={"1":"12.902436,77.565549","2":"12.902373,77.565147","3":"12.902303,77.564561",
    "4":"12.902264,77.564182","5":"12.902299,77.563500","6":"12.902483,77.562871","7":"12.902701,77.563095","8":"12.903018,77.563492",
    "9":"12.903712,77.564292","10":"12.904371,77.565029","11":"12.905307,77.566257"}
    db.child("sharath").set(data)
# Parameters
debug_time = 0
debug_acc = 1

word_threshold = 0.5
rec_duration = 0.5
window_stride = 0.5
sample_rate = 48000
resample_rate = 8000
num_channels = 1
num_mfcc = 16
model_path = 'wake_word_stop_lite.tflite'

# Sliding window
window = np.zeros(int(rec_duration * resample_rate) * 2)



# Load model (interpreter)
interpreter = Interpreter(model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)

# Decimate (filter and downsample)
def decimate(signal, old_fs, new_fs):
    
    # Check to make sure we're downsampling
    if new_fs > old_fs:
        print("Error: target sample rate higher than original")
        return signal, old_fs
    
    # We can only downsample by an integer factor
    dec_factor = old_fs / new_fs
    if not dec_factor.is_integer():
        print("Error: can only decimate by integer factor")
        return signal, old_fs

    # Do decimation
    resampled_signal = scipy.signal.decimate(signal, int(dec_factor))

    return resampled_signal, new_fs

# This gets called every 0.5 seconds
def sd_callback(rec, frames, time, status):

    

    # Start timing for testing
    start = timeit.default_timer()
    
    # Notify if errors
    if status:
        print('Error:', status)
    
    # Remove 2nd dimension from recording sample
    rec = np.squeeze(rec)
    
    # Resample
    rec, new_fs = decimate(rec, sample_rate, resample_rate)
    
    # Save recording onto sliding window
    window[:len(window)//2] = window[len(window)//2:]
    window[len(window)//2:] = rec

    # Compute features
    mfccs = python_speech_features.base.mfcc(window, 
                                        samplerate=new_fs,
                                        winlen=0.256,
                                        winstep=0.050,
                                        numcep=num_mfcc,
                                        nfilt=26,
                                        nfft=2048,
                                        preemph=0.0,
                                        ceplifter=0,
                                        appendEnergy=False,
                                        winfunc=np.hanning)
    mfccs = mfccs.transpose()

    # Make prediction from model
    in_tensor = np.float32(mfccs.reshape(1, mfccs.shape[0], mfccs.shape[1], 1))
    interpreter.set_tensor(input_details[0]['index'], in_tensor)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    val = output_data[0][0]
    if val > word_threshold:
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(recordaudio,1)
        f2 = executor.submit(gps,1)
        f3 = executor.submit(gsmsms,1)
          
    if debug_acc:
        print(val)
    
    if debug_time:
        print(timeit.default_timer() - start)

# Start streaming from microphone
with sd.InputStream(channels=num_channels,
                    samplerate=sample_rate,
                    blocksize=int(sample_rate * rec_duration),
                    callback=sd_callback):
    while True:
        pass
