# created using: https://www.youtube.com/watch?v=0hEmxOEeVO0

import customtkinter as ctk
import win32clipboard as wcb
import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from PIL import Image, ImageTk
from moviepy.editor import *
import urllib.request
from io import BytesIO
import math as math
import os, shutil

def extractNumber(s):
    return int(''.join(filter(str.isdigit, s)))

def clipboardDownload():
     wcb.OpenClipboard()
     data = wcb.GetClipboardData()
     wcb.CloseClipboard()
     tmpLen = len(entryURL.get())
     entryURL.delete(0, tmpLen)
     entryURL.insert(0,data)
     downloadVideo()

def downloadVideo():
    image_label.pack_forget()
    url = entryURL.get()
    resolution = resVar.get()

    statLabel.pack(padx=10, pady=5)
    progBar.pack(padx=10, pady=5)
    progLabel.pack(padx=10, pady=5)

    try:
        yt = YouTube(url, on_progress_callback=onProgress, use_oauth=False, allow_oauth_cache=True)
        if resolution == "max":
            stream = yt.streams.filter(progressive=False).order_by("resolution").last()
            resolution = stream.resolution
            resVar.set(resolution)
        else:stream = yt.streams.filter(res=resolution).first()
          

        statLabel.configure(text=f"{str(yt.title)}", text_color="white")

        # load thumbnail image
        image_label.configure(image=loadThumbnail(url))
        image_label.pack(padx=10, pady=10)

        print(resolution)
        if int(resolution[0:-1]) <= 720:
            statLabel.configure(text=f"Starting download: {str(yt.title)}", text_color="white", fg_color="transparent")
            os.path.join("env/downloads/", f"{yt.title}.mp4")

            stream.download(output_path="env/downloads")

            statLabel.configure(text=f"Successfully downloaded: {str(yt.title)}", text_color="green", fg_color="transparent")
            progBar.set(1)
        else:
            for f in os.listdir("env/downloads/temp"):
                file_path = os.path.join("env/downloads/temp", f)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            # in this case, we need to download audio and video seperately and merge them in post
        
            strAudio = yt.streams.get_audio_only()
            strVideo = yt.streams.filter(resolution=resolution).order_by('bitrate').first()

            print(f'Bitrate: {yt.streams.get_audio_only().bitrate}')
            print(strVideo)

            statLabel.configure(text=f"Starting download: {str(yt.title)}", text_color="white", fg_color="transparent")
            os.path.join("env/downloads/temp/", f'{yt.title}TMP.mp4')

            tmpAudioFile = strAudio.download(output_path="env/downloads/temp")
            tmpVideoFile = strVideo.download(output_path="env/downloads/temp")
            os.rename(tmpAudioFile, "env/downloads/temp/TMP.mp3")
            os.rename(tmpVideoFile, "env/downloads/temp/TMP.mp4")

            audio = AudioFileClip('env/downloads/temp/TMP.mp3')
            video = VideoFileClip('env/downloads/temp/TMP.mp4')

            compoundClip = CompositeAudioClip([audio])
            video.audio = compoundClip
            video.write_videofile(f'env/downloads/temp/{yt.title}.mp4', threads=4, logger=None)
            os.replace(f"env/downloads/temp/{yt.title}.mp4", f"env/downloads/{yt.title}.mp4")

            for f in os.listdir("env/downloads/temp"): # clear temp file
                file_path = os.path.join("env/downloads/temp", f)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

    except Exception as e:
        statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def downloadAudio():
     image_label.pack_forget()
     url = entryURL.get()

     statLabel.pack(padx=10, pady=5)
     progBar.pack(padx=10, pady=5)
     progLabel.pack(padx=10, pady=5)

     try:
          yt = YouTube(url, on_progress_callback=onProgress)
          
          statLabel.configure(text=f"{str(yt.title)}", text_color="white")

          # load thumbnail image
          image_label.configure(image=loadThumbnail(url))
          image_label.pack(padx=10, pady=10)

          # download
          os.path.join("downloads", f"{yt.title}.mp3")
          downloaded_file = yt.streams.filter(only_audio=True).first().download(output_path="downloads", )
          base, ext = os.path.splitext(downloaded_file)
          new_file = base + '.mp3'
          os.rename(downloaded_file, new_file)
          # on download complete
          statLabel.configure(text=f"Successfully downloaded: {str(yt.title)}", text_color="green", fg_color="transparent")
          progBar.set(1)
     except Exception as e:
          statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def clipboardAudio():
     wcb.OpenClipboard()
     data = wcb.GetClipboardData()
     wcb.CloseClipboard()
     tmpLen = len(entryURL.get())
     entryURL.delete(0, tmpLen)
     entryURL.insert(0,data)
     downloadAudio()

def searchRes():
     image_label.pack_forget()
     try:
          tmpRes, tmpRes2 = [], []
          url = entryURL.get()
          yt = YouTube(url)
          try:
               # load thumbnail image
               image_label.configure(image=loadThumbnail(url))
               image_label.pack(padx=10, pady=10)
          except: pass
          for s in yt.streams:
               tmpRes2.append(s.resolution)
          
          # remove all None values
          for r in tmpRes2:
               if (r != None):tmpRes.append(r)

          # convert found resolutions into dictionary to remove doubles
          tmpRes = list(dict.fromkeys(tmpRes))

          # sort resolutions
          tmpRes.sort(key=extractNumber, reverse=True)
          resolutions = tmpRes
          resBox.configure(values=resolutions)

     except Exception as e:
          statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")
          statLabel.pack(padx=10, pady=5)

def loadThumbnail(url):
     yt = YouTube(url)
     img = Image.open(BytesIO(urllib.request.urlopen(yt.thumbnail_url).read()))
     tmpW, tmpH = img.width, img.height
     verh = tmpW / tmpH
     desH = 400

     img = img.resize((int(math.floor(desH * verh)), int(desH)))
     photo = ImageTk.PhotoImage(img)
     return(photo)

def onProgress(stream, chunk, bytes_remaining):
     totalSize = stream.filesize
     bytesDownloaded = totalSize - bytes_remaining
     completion = bytesDownloaded/totalSize * 100 

     # update label
     progLabel.configure(text=str(int(completion)) + "%")
     progLabel.update()

     # update bar
     progBar.set(float(completion / 100))


########################################################################################################
########################################################################################################


# create root window
root = ctk.CTk()
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root.iconbitmap("icon.ico")

# window title
root.title("YouTube Downloader")

# restrict window scaling
root.geometry("1000x800")
root.minsize(1000,800)
root.maxsize(3000, 2400)

# create frame to hold content
contentFrame = ctk.CTkFrame(root)
contentFrame.pack(fill=ctk.BOTH, expand=True, pady=15, padx=15)

# create label / url input widget
entryURL = ctk.CTkEntry(contentFrame, width=400, height=40)
entryURL.insert(-1, 'https://www.youtube.com/watch?v=xhiFAxgr680')
entryURL.pack(padx=10, pady=5)

# create frame for download buttons
dFrame = ctk.CTkFrame(contentFrame, width=400, height=40)
dFrame.pack(expand=False, padx=15, pady=(15,2))

# download button
downloadButton = ctk.CTkButton(dFrame, text="Download", command=downloadVideo)
downloadButton.grid(row=0, column=0, padx=(15, 2.5), pady=15)

# download from clipboard button
cbButton = ctk.CTkButton(dFrame, text="Download from Clipboard", command=clipboardDownload)
cbButton.grid(row=0, column=1, padx=(2.5, 2.5), pady=15)

searchButton = ctk.CTkButton(dFrame,text="Get Resolutions", command=searchRes)
searchButton.grid(row=0, column=2, padx=(2.5,15), pady=15)

# Centering elements
dFrame.grid_columnconfigure(0, weight=1)
dFrame.grid_columnconfigure(1, weight=1)
dFrame.grid_columnconfigure(2, weight=1)

# create frame for audio download buttons
aFrame = ctk.CTkFrame(contentFrame, width=400, height=40)
aFrame.pack(expand=False, padx=15, pady=(2,15))

# download button
audioButton = ctk.CTkButton(aFrame, text="Download Audio", command=downloadAudio)
audioButton.grid(row=0, column=0, padx=(15, 2.5), pady=15)

# download from clipboard button
cbButton = ctk.CTkButton(aFrame, text="Audio from Clipboard", command=clipboardAudio)
cbButton.grid(row=0, column=1, padx=(2.5, 2.5), pady=15)

# Centering elements
aFrame.grid_columnconfigure(0, weight=1)
aFrame.grid_columnconfigure(1, weight=1)


# resolution selection
resolutions = ["max"]
resVar = ctk.StringVar()
resBox = ttk.Combobox(contentFrame, values=resolutions, textvariable=resVar, justify="center", )
resBox.pack(padx=10, pady=5)
resBox.set("max")

#create thumbnail
image_label = ctk.CTkLabel(contentFrame, width=500, height=320, corner_radius=200, bg_color="transparent")

# create progress label and bar
progLabel = ctk.CTkLabel(contentFrame, text="0%")
progLabel.pack(padx=10, pady=5)

progBar = ctk.CTkProgressBar(contentFrame, width=600)
progBar.set(0.0)
#progBar.pack(padx=10, pady=15)

# create status label
statLabel = ctk.CTkLabel(contentFrame, text="-")
#statLabel.pack(padx=10, pady=5)

# start app
root.mainloop()