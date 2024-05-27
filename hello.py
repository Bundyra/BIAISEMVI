import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav"), ("All Files", "*.*")]
    )
    if file_path:
        messagebox.showinfo("Open File", f"Opening File: {file_path}")

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

# Create the main window
root = tk.Tk()
root.title("AI PROJEKT")
root.geometry("1366x768")  # Set the window size to 1366x768
root.configure(bg="#3498db")  # Set the background color to blue

# Create a frame to hold the menu buttons and center it
menu_frame = tk.Frame(root, bg="#3498db")  # Set the background color of the frame to blue
menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
    button.pack(pady=10)
    button.bind("<Button-1>", lambda e, cmd=command: cmd())

# Start the main event loop
root.mainloop()
