from AudioFile import AudioFile
import librosa as lb

signaldata,samplingrate = lb.load('E:/aditya/BE project Database/Database/Additional Dataset/Mendley/Raw/Fibrosis/BP23_Lung Fibrosis,Crep,P R L ,50,M-[AudioTrimmer.com] (2).wav')
af = AudioFile()
fileurl = af.save_audio_file(signaldata,samplingrate)
filename = af.get_filename_from_url(fileurl) 
print(filename)