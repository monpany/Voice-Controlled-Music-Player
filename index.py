# Import necessary libraries
import os
import speech_recognition as sr
import pyttsx3
from pygame import mixer
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps  # Ensure this line is at the top of your script
import threading


# Text-to-speech function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Speech-to-text function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return ""


# Get list of songs in the Music folder
def load_songs(folder):
    return [song for song in os.listdir(folder) if song.endswith(".mp3")]


# Find the closest match for a song
def find_song(song_name, songs):
    for song in songs:
        if song_name in song.lower():
            return song
    return None