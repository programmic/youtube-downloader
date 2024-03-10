# Import necessary libraries
import customtkinter as ctk
import win32clipboard as wcb
import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from PIL import Image, ImageTk
import ffmpeg
import subprocess
import urllib.request
from io import BytesIO
import math
import os
import shutil

# Function to extract numbers from a string
def extractNumber(s):
    return int(''.join(filter(str.isdigit, s)))

# Define the function for merging audio and video
def merge_audio_video(audio_input, video_input, output_path):
    print("arrived in merge function")

    audIn = ffmpeg.input(audio_input)
    vidIn = ffmpeg.input(video_input)
    out = ffmpeg.input(output_path)

    ffmpeg.output(audIn, vidIn, output_path).run()

# Function triggered when downloading from clipboard
def clipboardDownload():
    wcb.OpenClipboard()
    data = wcb.GetClipboardData()
    wcb.CloseClipboard()
    tmpLen = len(entryURL.get())
    entryURL.delete(0, tmpLen)
    entryURL.insert(0, data)
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
        else:
            stream = yt.streams.filter(res=resolution).first()

        statLabel.configure(text=f"{str(yt.title)}", text_color="white")

        # load thumbnail image
        image_label.configure(image=loadThumbnail(url))
        image_label.pack(padx=10, pady=10)

        print(resolution)
        if int(resolution[0:-1]) <= 720:
            statLabel.configure(text=f"Starting download: {str(yt.title)}", text_color="white", fg_color="transparent")
            output_path = os.path.join("downloads", f"{yt.title}.mp4")
            stream.download(output_path=output_path)
            statLabel.configure(text=f"Successfully downloaded: {str(yt.title)}", text_color="green", fg_color="transparent")
            progBar.set(1)
        else:

            for filename in os.listdir("env/downloads/temp"):
                filePath = os.path.join("env/downloads/temp", filename)
                if os.path.isfile(filePath):
                    os.remove(filePath)


            os.rmdir("env/downloads/temp")
            shutil.rmtree("env/downloads/temp", ignore_errors=True)
            print("cleared temp file")

            # Download audio and video separately and merge them
            strAudio = yt.streams.get_audio_only()
            strVideo = yt.streams.filter(resolution=resolution).order_by('bitrate').first()

            statLabel.configure(text=f"Starting download: {str(yt.title)}", text_color="white", fg_color="transparent")
            tmpAudioFile = strAudio.download(output_path="env/downloads/temp")
            tmpVideoFile = strVideo.download(output_path="env/downloads/temp")
            print("Downloaded files...")

            # Rename audio and video files
            os.rename(tmpAudioFile, os.path.join("env/downloads/temp/TMP.mp3",""))
            os.rename(tmpVideoFile, os.path.join("env/downloads/temp/TMP.mp4",""))

            statLabel.configure(text=f"Merging files for {yt.title}", text_color="white", fg_color="transparent")

            print("fetching files...")
            audio = "env/downloads/temp/TMP.mp3"
            video = "env/downloads/temp/TMP.mp3"
            print("fetched em")

            # Merge audio and video
            merge_audio_video(audio, video, "env/downloads/temp/TMP.mp4")
            print("Done merging")

            # Clear temporary files
            shutil.rmtree("env/downloads/temp")

            statLabel.configure(text=f"Completed merge of audio/video: {yt.title}", text_color="green", fg_color="transparent")

    except Exception as e:
        statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

# Function to download audio
def downloadAudio():
    image_label.pack_forget()
    url = entryURL.get()

    statLabel.pack(padx=10, pady=5)
    progBar.pack(padx=10, pady=5)
    progLabel.pack(padx=10, pady=5)

    try:
        yt = YouTube(url, on_progress_callback=onProgress)
        statLabel.configure(text=f"{str(yt.title)}", text_color="white")

        # Load thumbnail image
        image_label.configure(image=loadThumbnail(url))
        image_label.pack(padx=10, pady=10)

        # Download audio
        downloaded_file = yt.streams.filter(only_audio=True).first().download(output_path="downloads")
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.mp3'
        os.rename(downloaded_file, new_file)

        statLabel.configure(text=f"Successfully downloaded: {str(yt.title)}", text_color="green", fg_color="transparent")
        progBar.set(1)
    except Exception as e:
        statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

# Function to download audio from clipboard
def clipboardAudio():
    wcb.OpenClipboard()
    data = wcb.GetClipboardData()
    wcb.CloseClipboard()
    tmpLen = len(entryURL.get())
    entryURL.delete(0, tmpLen)
    entryURL.insert(0, data)
    downloadAudio()

# Function to search resolutions
def searchRes():
    image_label.pack_forget()
    try:
        tmpRes, tmpRes2 = [], []
        url = entryURL.get()
        yt = YouTube(url)
        try:
            # Load thumbnail image
            image_label.configure(image=loadThumbnail(url))
            image_label.pack(padx=10, pady=10)
        except:
            pass
        for s in yt.streams:
            tmpRes2.append(s.resolution)

        # Remove all None values
        for r in tmpRes2:
            if r is not None:
                tmpRes.append(r)

        # Convert found resolutions into dictionary to remove doubles
        tmpRes = list(dict.fromkeys(tmpRes))

        # Sort resolutions
        tmpRes.sort(key=extractNumber, reverse=True)
        resolutions = tmpRes
        resBox.configure(values=resolutions)

    except Exception as e:
        statLabel.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")
        statLabel.pack(padx=10, pady=5)

# Function to load thumbnail
def loadThumbnail(url):
    yt = YouTube(url)
    img = Image.open(BytesIO(urllib.request.urlopen(yt.thumbnail_url).read()))
    tmpW, tmpH = img.width, img.height
    verh = tmpW / tmpH
    desH = 400

    img = img.resize((int(math.floor(desH * verh)), int(desH)))
    photo = ImageTk.PhotoImage(img)
    return photo

# Function to update progress
def onProgress(stream, chunk, bytes_remaining):
    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytes_remaining
    completion = bytesDownloaded / totalSize * 100

    # Update label
    progLabel.configure(text=str(int(completion)) + "%")
    progLabel.update()

    # Update progress bar
    progBar.set(float(completion / 100))

# Create root window
root = ctk.CTk()
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root.iconbitmap("icon.ico")
root.title("YouTube Downloader")
root.geometry("1000x800")
root.minsize(1000, 800)
root.maxsize(3000, 2400)

# Create frame to hold content
contentFrame = ctk.CTkFrame(root)
contentFrame.pack(fill=ctk.BOTH, expand=True, pady=15, padx=15)

# Create label / url input widget
entryURL = ctk.CTkEntry(contentFrame, width=400, height=40)
entryURL.insert(-1, 'https://www.youtube.com/watch?v=xhiFAxgr680')
entryURL.pack(padx=10, pady=5)

# Create frame for download buttons
dFrame = ctk.CTkFrame(contentFrame, width=400, height=40)
dFrame.pack(expand=False, padx=15, pady=(15, 2))

# Download button
downloadButton = ctk.CTkButton(dFrame, text="Download", command=downloadVideo)
downloadButton.grid(row=0, column=0, padx=(15, 2.5), pady=15)

# Download from clipboard button
cbButton = ctk.CTkButton(dFrame, text="Download from Clipboard", command=clipboardDownload)
cbButton.grid(row=0, column=1, padx=(2.5, 2.5), pady=15)

searchButton = ctk.CTkButton(dFrame, text="Get Resolutions", command=searchRes)
searchButton.grid(row=0, column=2, padx=(2.5, 15), pady=15)

# Centering elements
dFrame.grid_columnconfigure(0, weight=1)
dFrame.grid_columnconfigure(1, weight=1)
dFrame.grid_columnconfigure(2, weight=1)

# Create frame for audio download buttons
aFrame = ctk.CTkFrame(contentFrame, width=400, height=40)
aFrame.pack(expand=False, padx=15, pady=(2, 15))

# Audio download button
audioButton = ctk.CTkButton(aFrame, text="Download Audio", command=downloadAudio)
audioButton.grid(row=0, column=0, padx=(15, 2.5), pady=15)

# Download audio from clipboard button
cbButton = ctk.CTkButton(aFrame, text="Audio from Clipboard", command=clipboardAudio)
cbButton.grid(row=0, column=1, padx=(2.5, 2.5), pady=15)

# Centering elements
aFrame.grid_columnconfigure(0, weight=1)
aFrame.grid_columnconfigure(1, weight=1)

# Resolution selection
resolutions = ["max"]
resVar = ctk.StringVar()
resBox = ttk.Combobox(contentFrame, values=resolutions, textvariable=resVar, justify="center", )
resBox.pack(padx=10, pady=5)
resBox.set("max")

# Create thumbnail
image_label = ctk.CTkLabel(contentFrame, width=500, height=320, corner_radius=200, bg_color="transparent")

# Create progress label and bar
progLabel = ctk.CTkLabel(contentFrame, text="0%")
progLabel.pack(padx=10, pady=5)

progBar = ctk.CTkProgressBar(contentFrame, width=600)
progBar.set(0.0)

# Create status label
statLabel = ctk.CTkLabel(contentFrame, text="-")

# Start app
root.mainloop()
