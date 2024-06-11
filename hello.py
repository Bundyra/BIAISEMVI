import tkinter as tk
from tkinter import filedialog, messagebox, Scale
import pygame
import pickle
import numpy as np
import librosa
from PIL import Image, ImageTk, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Zapis modelu, enkodera i skalera
with open('genre_classifier.pkl', 'rb') as f:
    model = pickle.load(f)
with open('label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

current_file_path = None

def open_file():
    global current_file_path
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav"), ("All Files", "*.*")]
        )
        if file_path:
            current_file_path = file_path
            messagebox.showinfo("Open File", f"Opening File: {file_path}")
            features = extract_features_from_audio(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

def play_file():
    try:
        if current_file_path:
            pygame.mixer.music.load(current_file_path)
            pygame.mixer.music.play()
            audio, sfreq = librosa.load(current_file_path)
            time = np.arange(0, len(audio))/sfreq
            plt.figure(num="Amplitude")
            plt.plot(time,audio)
            plt.xlabel("Time")
            plt.ylabel("Sound Amplitude")
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to play file: {e}")

def stop_file():
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop file: {e}")

def guess_genre():
    global current_file_path
    try:
        if current_file_path:
            features = extract_features_from_audio(current_file_path)
            while len(features) < 15:
                features.append(0)
            scaled_features = scaler.transform([features])
            predictions = model.predict_proba(scaled_features)[0]

            all_labels = le.classes_

            data, sr = librosa.load(current_file_path)
            X = librosa.stft(data)
            Xdb = librosa.amplitude_to_db(abs(X))
            g = plt.figure(figsize=(14, 6), num="Spectogram")
            librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
            plt.colorbar()

            f = plt.figure(figsize=(10, 6), num="Genre Recognition")
            plt.barh(all_labels, predictions * 100, color='skyblue')
            plt.xlabel('Probability (%)')
            plt.ylabel('Music Genre')
            plt.title('Genre Prediction')

            for index, value in enumerate(predictions * 100):
                plt.text(value, index, f'{value:.2f}%', va='center')

            plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to predict genre: {e}")



def extract_features_from_audio(file_path):
    y, sr = librosa.load(file_path, duration=30)
    features = []
    features.append(np.mean(librosa.feature.chroma_stft(y=y, sr=sr)))  # chroma_stft
    features.append(np.mean(librosa.feature.rms(y=y)))  # rms
    features.append(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))  # spectral_centroid
    features.append(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))  # spectral_bandwidth
    features.append(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))  # spectral_rolloff
    features.append(np.mean(librosa.feature.zero_crossing_rate(y)))  # zero_crossing_rate
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features.extend(np.mean(mfccs.T, axis=0))  # MFCCs
    return features

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def exit_app():
    root.quit()

def about_app():
    messagebox.showinfo("About", "Made by: Kamil Bundyra, Kamil Grabowski")

def create_rounded_button_image(width, height, radius, color, text, text_color, font):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=radius,
        fill=color
    )

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=text_color
    )

    return ImageTk.PhotoImage(image)

pygame.mixer.init()

# Create the main window
root = tk.Tk()
root.title("Music Genre Recognition")
root.geometry("800x768")
root.configure(bg="#3498db")

menu_frame = tk.Frame(root, bg="#3498db")
menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

button_width = 200
button_height = 60
button_radius = 30
button_color = (0, 0, 255)
button_text_color = (255, 255, 0)

font = ImageFont.truetype("arialbd.ttf", 20)

buttons = [
    ("Open", open_file),
    ("Play", play_file),
    ("Stop", stop_file),
    ("Guess", guess_genre),
    ("About", about_app),
    ("Exit", exit_app)
]

for text, command in buttons:
    image = create_rounded_button_image(button_width, button_height, button_radius, button_color, text, button_text_color, font)
    button = tk.Label(menu_frame, image=image, cursor="hand2", bg="#3498db")
    button.image = image
    button.pack(pady=10)
    button.bind("<Button-1>", lambda e, cmd=command: cmd())

volume_slider = Scale(root, from_=0, to=100, orient=tk.VERTICAL, command=set_volume, bg="#3498db", fg="yellow", font=("Arial", 12), length=500)
volume_slider.set(50)
volume_slider.place(relx=0.95, rely=0.5, anchor=tk.CENTER)

root.mainloop()