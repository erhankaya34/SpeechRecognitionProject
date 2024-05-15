import tkinter as tk
from tkinter import PhotoImage, font, ttk
import speech_recognition as sr
from deep_translator import GoogleTranslator
import threading

def available_microphones():
    return sr.Microphone.list_microphone_names()

def set_microphone(index):
    global mic
    mic = sr.Microphone(device_index=index)

def listen_and_translate():
    recognizer = sr.Recognizer()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:  # Sürekli dinleme ve çeviri için döngü
            message_label.config(text="Listening...", fg="green")
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                message_label.config(text="Processing...", fg="blue")
                text = recognizer.recognize_google(audio, language='en-US')
                audio_text.delete('1.0', tk.END)
                audio_text.insert(tk.END, text)
                audio_text.tag_add("center", "1.0", "end")
                translation = GoogleTranslator(source='en', target='tr').translate(text)
                translated_text.delete('1.0', tk.END)
                translated_text.insert(tk.END, translation)
                translated_text.tag_add("center", "1.0", "end")
                message_label.config(text="Translation Complete", fg="black")
            except sr.UnknownValueError:
                message_label.config(text="Unintelligible speech", fg="red")
            except sr.RequestError as e:
                message_label.config(text=f"Service error: {str(e)}", fg="red")
            except sr.WaitTimeoutError:
                message_label.config(text="No speech detected, try again", fg="red")
            except Exception as e:
                message_label.config(text=f"Error: {str(e)}", fg="red")

def refresh_app():
    threading.Thread(target=listen_and_translate, daemon=True).start()

root = tk.Tk()
root.title("Bug Zone Transcriptor")
root.geometry("1080x260")
root.configure(bg="white")

# Define fonts
normal_font = font.Font(family='Helvetica', size=12, weight='normal')
bold_font = font.Font(family='Helvetica', size=12, weight='bold')

# Load images
logo_image = PhotoImage(file='Images/logo.png')
icon_image = PhotoImage(file='Images/icon2.png')

logo_label = tk.Label(root, image=logo_image, bg="white")
logo_label.pack(side=tk.LEFT, padx=10, pady=10)

icon_label = tk.Label(root, image=icon_image, bg="white")
icon_label.pack(side=tk.RIGHT, padx=10, pady=10)

message_label = tk.Label(root, text="", bg="white", fg="black")
message_label.pack(fill=tk.X, pady=10)

# Dropdown menu for microphone selection
mic_list = available_microphones()
mic_menu = ttk.Combobox(root, values=mic_list, width=50)
mic_menu.pack(pady=20)
mic_menu.current(0)  # Default to the first microphone
set_microphone(mic_menu.current())  # Initialize with default microphone
mic_menu.bind("<<ComboboxSelected>>", lambda event: set_microphone(mic_menu.current()))

# Text areas with updated fonts and visible, centered text
audio_text = tk.Text(root, height=4, width=50, bg="white", fg="black", borderwidth=0, highlightthickness=0, font=normal_font)
audio_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
audio_text.tag_configure("center", justify='center')

translated_text = tk.Text(root, height=4, width=50, bg="white", fg="black", borderwidth=0, highlightthickness=0, font=bold_font)
translated_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
translated_text.tag_configure("center", justify='center')

refresh_button = tk.Button(root, text="Refresh", command=refresh_app, bg="white", fg="black", padx=50, pady=50)  # Increased padding

refresh_app()  # This function call starts continuous listening when the application starts

root.mainloop()
