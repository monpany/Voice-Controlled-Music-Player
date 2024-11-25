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

# Background listener for voice commands
def voice_command_listener():
    while True:
        handle_voice_command()


# Update song info in the GUI
def update_song_info(title, artist):
    song_title_label.config(text=title)
    artist_label.config(text=f"- {artist} -")


# Update playback status in the GUI
def update_status(new_status):
    status_label.config(text=f"Status: {new_status}")


# Update the volume
def update_volume(val):
    volume = int(val) / 100  # Scale value is from 0 to 100, convert to 0.0 to 1.0
    mixer.music.set_volume(volume)


# GUI Setup
root = tk.Tk()
root.title("Voice-Controlled Music Player")
root.geometry("400x600")
root.configure(bg="#f2f2f2")

music_folder = "Music"  # Path to your music folder
songs = load_songs(music_folder)  # Load all songs from the folder
current_song = None
current_song_index = -1  # Initialize to -1 to indicate no song is playing yet


# Gradient background
canvas = tk.Canvas(root, width=400, height=300,background="white")
canvas.pack(fill="both", expand=True)

small = tk.Canvas(canvas,width=390, height=290, background="black")
small.pack()
ya =tk.Canvas(canvas,width=370,height=270, background="purple")

# Song Info
song_title_label = tk.Label(root, text="Your Very Cool Song", font=("Arial", 16, "bold"), bg="#f2f2f2")
song_title_label.pack(pady=10)

artist_label = tk.Label(root, text="- Your Cool Band -", font=("Arial", 12), bg="#f2f2f2")
artist_label.pack()

# Playback Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=20)

pause_button = tk.Button(button_frame, text="Pause", width=8, command=pause_music)
pause_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop", width=8, command=stop_music)
stop_button.grid(row=0, column=1, padx=5)

continue_button = tk.Button(button_frame, text="Continue", width=8, command=continue_music)
continue_button.grid(row=0, column=2, padx=5)

next_button = tk.Button(button_frame, text="Next", width=8, command=play_next_song)
next_button.grid(row=0, column=3, padx=5)

# Progress Bar
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

# Volume Control Slider (Cable-like UI)
volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Volume", command=update_volume)
volume_slider.set(50)  # Default volume is 50%
volume_slider.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12), bg="#f2f2f2")
status_label.pack(pady=10)

# Start background voice listener
speak("Welcome to the voice-controlled music player.")
speak(f"I found {len(songs)} songs in your library.")
listener_thread = threading.Thread(target=voice_command_listener, daemon=True)
listener_thread.start()

# Mainloop
root.mainloop()