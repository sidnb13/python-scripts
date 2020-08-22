from pytube import YouTube 
import os, shutil, datetime
from os import path

path_dest = '/Users/sidbaskaran/Desktop/yt-planes'
url = input('Enter video URL: ')
    
yt = YouTube(url)
print('Downloading',yt.title)
filename = yt.title.replace('/','_')

video = yt.streams.filter(adaptive=True).filter(file_extension='mp4').order_by('resolution').last()
audio = yt.streams.filter(only_audio=True).filter(file_extension='mp4').first()
video.download(filename='vid')
audio.download(filename='aud')

os.system('ffmpeg -i vid.mp4 -i aud.mp4 -c:v copy -c:a aac "{}.mp4"'.format(filename))
os.remove('aud.mp4')
os.remove('vid.mp4')
size = os.path.getsize('{}.mp4'.format(filename))/(10**6)
shutil.move('{}.mp4'.format(filename),path_dest)
print('Downloaded to \'{}\' | {} MB'.format(path_dest,size))
