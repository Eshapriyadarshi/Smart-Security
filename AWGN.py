
import soundfile as sf
import numpy as np
import sys
import os
import re
 
def add_noise(noisedir,cleandir,snr):
    # noisy
    splitdir=re.split(r"\\",noisedir)
    wavdir="D:\\clean" # The path where all wav files are located
    for i in range(len(splitdir) - 1):
        wavdir = splitdir[i] + '/'
        noisydir=wavdir+"noisy/" # Noisy voice storage path
    os.mkdir(noisydir)
    # noise
    for noisewav in os.listdir(noisedir):
        noise, fs = sf.read(noisedir+'/'+noisewav)
        noisy_splitdir=noisydir+"add_"+noisewav[:-4]+"/"
        os.mkdir(noisy_splitdir)
    # clean
        for cleanwav in os.listdir(cleandir):
            clean, Fs = sf.read(cleandir+"/"+cleanwav)
            # add noise
            if fs == Fs and len(clean) <= len(noise):
                cleanenergy = np.sum(np.power(clean,2))
                noiseenergy = np.sum(np.power(noise,2))
                                 # Noise level coefficient
                noiseratio = np.sqrt((cleanenergy / noiseenergy) / (np.power(10, snr * 0.1)))
                ind = np.random.randint(1, len(noise)-len(clean)+1)
                                 # Random index noise signal with the same length as clean
                noisyAudio = clean + noise[ind:len(clean)+ind] * noiseratio
                # write wav
                noisywavname=noisy_splitdir+cleanwav[:-4]+"_"+noisewav[:-4]+"_snr"+str(snr)+".wav"
                sf.write(noisywavname, noisyAudio, 16000)
            else:
                print("fs of clean and noise is unequal or the length of clean is longer than noise's\n")
                sys.exit(-1)
 
noisedir="D:\\noise"
cleandir="D:\\clean"
snr=5
add_noise(noisedir,cleandir,snr)