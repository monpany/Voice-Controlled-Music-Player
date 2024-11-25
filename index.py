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
# Function play music
def play_music(file_path=None):
    global current_song
    if file_path:
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        current_song = file_path
        update_status("Playing")
        update_song_info(os.path.basename(file_path).replace(".mp3", ""), "Unknown Artist")
    elif current_song:
        mixer.music.play()
        update_status("Playing")
    else:
        speak("No song selected.")

# Function stop music
def stop_music():
    if mixer.get_init():
        mixer.music.stop()
        update_status("Stopped")

# Function pause music
def pause_music():
    if mixer.get_init():
        mixer.music.pause()
        update_status("Paused")

# Function continue music
def continue_music():
    if mixer.get_init():
        mixer.music.unpause()  # Resume playback from the paused position
        update_status("Playing (continued)")
    else:
        speak("No song to continue.")

# Function next song
def play_next_song():
    global current_song_index, current_song
    if songs:
        current_song_index = (current_song_index + 1) % len(songs)  # Move to the next song; loop to the start if at the end
        next_song = songs[current_song_index]
        file_path = os.path.join(music_folder, next_song)
        current_song = file_path
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        update_status("Playing")
        update_song_info(os.path.basename(next_song).replace(".mp3", ""), "Unknown Artist")
    else:
        speak("No songs in the library.")



def handle_voice_command():
    command = listen()
    if "play" in command:
        speak("Please say the name of the song.")
        song_name = listen()
        matched_song = find_song(song_name, songs)
        if matched_song:
            file_path = os.path.join(music_folder, matched_song)
            play_music(file_path)
        else:
            speak("Song not found.")
    elif "stop" in command:
        stop_music()
    elif "pause" in command:
        pause_music()
    elif "next" in command:
        play_next_song()  # Restarts the song
    elif "continue" in command:
        continue_music()  # Continues from the paused position
    elif "exit" in command:
        speak("Goodbye!")
        root.destroy()
