def recordaudio():   
    import pyrebase
    import sounddevice
    from scipy.io.wavfile import write
    #record audio
    fs = 44100
    second = 5
    print("recording")
    record_voice = sounddevice.rec(int(second * fs),samplerate=fs,channels = 2)
    sounddevice.wait()
    write("output.wav",fs,record_voice)
    print("stop recording")
    
    #store the audio in firebase
    firebaseConfig = {
        'apiKey': "AIzaSyD31Rl2Tyiev4ehQsz5PYwMERWXh5g35uw",
        'authDomain': "test1-b08fe.firebaseapp.com",
        'projectId': "test1-b08fe",
        'storageBucket': "test1-b08fe.appspot.com",
        "databaseURL": "test1-b08fe.appspot.com",
        'messagingSenderId': "675375075463",
        'appId': "1:675375075463:web:7a7526e17944b6a8746822",
        'measurementId': "G-ZKMJE2PT3C"
        }
    firebase=pyrebase.initialize_app(firebaseConfig)

    storage=firebase.storage()
    file="output.wav"
    security = input("enter the security code")
    name = "/audio.wav"
    cloudfilename=security+name
    storage.child(cloudfilename).put(file)

recordaudio()