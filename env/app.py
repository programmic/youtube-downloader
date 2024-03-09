# created using: https://www.youtube.com/watch?v=0hEmxOEeVO0

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import math as math
import os

def extractNumber(s):
    return int(''.join(filter(str.isdigit, s)))

def downloadVideo():
     image_label.pack_forget()
     url = entryURL.get()
     resolution = resVar.get()

     statLabel.pack(padx=10, pady=5)
     progBar.pack(padx=10, pady=5)
     progLabel.pack(padx=10, pady=5)

     try:
          yt = YouTube(url, on_progress_callback=onProgress)
          if resolution == "max":
               resolution = yt.streams.get_highest_resolution()
          stream = yt.streams.filter(res=resolution).first()
          
          statLabel.configure(text=f"{str(yt.title)}", text_color="white")

          # load thumbnail image
          img = Image.open(BytesIO(urllib.request.urlopen(yt.thumbnail_url).read()))
          tmpW, tmpH = img.width, img.height
          verh = tmpW / tmpH
          desH = 200

          img = img.resize((int(math.floor(desH * verh)), int(desH)))
          photo = ImageTk.PhotoImage(img)
          image = photo

          image_label.configure(image=photo)
          image_label.pack(padx=10, pady=10)

          statLabel.configure(text=f"Starting download: {str(yt.title)}", text_color="white")
          os.path.join("downloads", f"{yt.title}.mp4")
          stream.download(output_path="downloads", )

          statLabel.configure(text=f"Successfully downloaded: {str(yt.title)}", text_color="green")
          progBar.set(1)
     except Exception as e:
          statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def searchRes():
     image_label.pack_forget()
     try:
          tmpRes, tmpRes2 = [], []
          url = entryURL.get()
          yt = YouTube(url)
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

          try:
               # load thumbnail image
               img = Image.open(BytesIO(urllib.request.urlopen(yt.thumbnail_url).read()))
               tmpW, tmpH = img.width, img.height
               verh = tmpW / tmpH
               desH = 200

               img = img.resize((int(math.floor(desH * verh)), int(desH)))
               photo = ImageTk.PhotoImage(img)
               image = photo

               image_label.configure(image=photo)
               image_label.pack(padx=10, pady=10)
          except: pass
     except Exception as e:
          statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")
          statLabel.pack(padx=10, pady=5)

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

# window title
root.title("YouTube Downloader")

# restrict window scaling
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

# create frame to hold content
contentFrame = ctk.CTkFrame(root)
contentFrame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)

# create label / url input widget
entryURL = ctk.CTkEntry(contentFrame, width=400, height=40)
entryURL.pack(padx=10, pady=5)

# download button
downloadButton = ctk.CTkButton(contentFrame, text="Download", command=downloadVideo)
downloadButton.pack(padx=10, pady=5)

searchButton = ctk.CTkButton(contentFrame,text="Get Resolutions", command=searchRes)
searchButton.pack(padx=0, pady=0)

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

progBar = ctk.CTkProgressBar(contentFrame, width=400)
progBar.set(0.0)
#progBar.pack(padx=10, pady=15)

# create status label
statLabel = ctk.CTkLabel(contentFrame, text="-")
#statLabel.pack(padx=10, pady=5)

# start app
root.mainloop()