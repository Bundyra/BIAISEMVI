import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pygame
import os

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav"), ("All Files", "*.*")]
    )
    if file_path:
        file_name = os.path.basename(file_path)
        file_label.config(text=f"Now playing: {file_name}")
        load_audio_player_controls(file_path)

def load_audio_player_controls(file_path):
    def play_audio():
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        update_progress_bar()

    def stop_audio():
        pygame.mixer.music.stop()
        progress_bar.stop()
        progress_bar["value"] = 0

    def pause_audio():
        pygame.mixer.music.pause()

    def unpause_audio():
        pygame.mixer.music.unpause()
        update_progress_bar()

    def update_progress_bar():
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000
            progress_bar["value"] = current_pos
            root.after(1000, update_progress_bar)

    def set_volume(volume):
        # Convert volume to float
        volume_float = float(volume)
        # Round to nearest integer
        volume_int = round(volume_float)
        # Set volume for Pygame mixer
        pygame.mixer.music.set_volume(volume_int / 100)

    # Get the length of the song
    audio_length = pygame.mixer.Sound(file_path).get_length()


    # Clear existing widgets in the player controls frame
    for widget in player_controls_frame.winfo_children():
        widget.destroy()

    # Load and resize images for buttons
    icon_size = (40, 40)  # Set the desired icon size
    play_image = Image.open("play.png").resize(icon_size, Image.LANCZOS)
    play_photo = ImageTk.PhotoImage(play_image)
    pause_image = Image.open("pause.png").resize(icon_size, Image.LANCZOS)
    pause_photo = ImageTk.PhotoImage(pause_image)
    stop_image = Image.open("stop.png").resize(icon_size, Image.LANCZOS)
    stop_photo = ImageTk.PhotoImage(stop_image)
    unpause_image = Image.open("unpause.png").resize(icon_size, Image.LANCZOS)
    unpause_photo = ImageTk.PhotoImage(unpause_image)

    # Create buttons with images
    play_button = tk.Button(player_controls_frame, image=play_photo, command=play_audio, bg="#3498db", borderwidth=0)
    stop_button = tk.Button(player_controls_frame, image=stop_photo, command=stop_audio, bg="#3498db", borderwidth=0)
    pause_button = tk.Button(player_controls_frame, image=pause_photo, command=pause_audio, bg="#3498db", borderwidth=0)
    unpause_button = tk.Button(player_controls_frame, image=unpause_photo, command=unpause_audio, bg="#3498db", borderwidth=0)

    # Keep a reference to the image objects to prevent garbage collection
    play_button.image = play_photo
    stop_button.image = stop_photo
    pause_button.image = pause_photo
    unpause_button.image = unpause_photo

    # Pack buttons horizontally
    play_button.pack(side=tk.LEFT, padx=10)
    stop_button.pack(side=tk.LEFT, padx=10)
    pause_button.pack(side=tk.LEFT, padx=10)
    unpause_button.pack(side=tk.LEFT, padx=10)

    # Create and display the progress bar
    progress_bar = ttk.Progressbar(player_controls_frame, orient="horizontal", length=500, mode="determinate",
                                   style="TProgressbar")
    progress_bar.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
    progress_bar["maximum"] = audio_length

    # Get the background color of the menu frame
    menu_bg_color = menu_frame.cget("bg")

    # Create a scale for volume control
    volume_scale = tk.Scale(
        player_controls_frame,
        from_=0, to=100,
        orient=tk.HORIZONTAL,
        command=set_volume,
        bg=menu_bg_color,  # Background color same as menu
        troughcolor=menu_bg_color,  # Trough color same as menu
        length=200  # Longer length
    )
    volume_scale.set(50)  # Set initial volume to 50%
    volume_scale.pack(side=tk.BOTTOM, pady=10)

def test_file():
    messagebox.showinfo("Guess genre", "Guessing genre of the song.")

def exit_app():
    root.quit()

def about_app():
    messagebox.showinfo("About", "Made by: Kamil Bundyra, Kamil Grabowski")

def create_rounded_button_image(width, height, radius, color, text, text_color, font):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw rounded rectangle
    draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=radius,
        fill=color
    )

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Add text
    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=text_color
    )

    return ImageTk.PhotoImage(image)

# Initialize Pygame mixer
pygame.mixer.init()

# Create the main window
root = tk.Tk()
root.title("AI PROJEKT")
root.geometry("1366x768")  # Set the window size to 1366x768
root.configure(bg="#3498db")  # Set the background color to blue

# Style the progress bar
style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar",
                troughcolor='#3498db',  # Blue background
                background='#000000',  # Black progress
                thickness=5)  # Thinner progress bar

# Create a frame to hold the menu buttons and center it
menu_frame = tk.Frame(root, bg="#3498db")  # Set the background color of the frame to blue
menu_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  # Adjusted position to leave space for controls

# Button configurations
button_width = 200
button_height = 60
button_radius = 30
button_color = (0, 0, 255)  # Blue
button_text_color = (255, 255, 0)  # Yellow

# Define font
font = ImageFont.truetype("arialbd.ttf", 20)  # Using Arial Bold

# Create and place the menu buttons
buttons = [
    ("Open", open_file),
    ("Guess", test_file),
    ("Exit", exit_app),
    ("About", about_app)
]

for text, command in buttons:
    image = create_rounded_button_image(button_width, button_height, button_radius, button_color, text, button_text_color, font)
    button = tk.Label(menu_frame, image=image, cursor="hand2", bg="#3498db")  # Set the background color of the button to blue
    button.image = image  # Keep a reference to prevent garbage collection
    button.pack(side=tk.LEFT, padx=10, pady=10)
    button.bind("<Button-1>", lambda e, cmd=command: cmd())

# Create a label to display the file name
file_label = tk.Label(root, text="No file selected", bg="#3498db", fg="white", font=("Arial", 16))
file_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Create a frame to hold the player controls and place it below the file label
player_controls_frame = tk.Frame(root, bg="#3498db")
player_controls_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Create a progress bar to display the song progress
progress_bar = ttk.Progressbar(player_controls_frame, orient="horizontal", length=500, mode="determinate", style="TProgressbar")

# Start the main event loop
root.mainloop()
