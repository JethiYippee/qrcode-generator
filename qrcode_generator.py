import customtkinter as ctk
import qrcode
import os
import re
import subprocess
import io
import win32clipboard
from PIL import Image

# Initialize the main app window
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Blue accent color

app = ctk.CTk()
app.title("QR Code Generator")
app.geometry("500x430")

def sanitize_filename(name):
    """Remove invalid characters and limit filename length."""
    name = re.sub(r'[\/:*?"<>|]', '_', name)  # Replace invalid characters
    return name[:30]  # Limit filename length to 30 characters

def get_unique_filename(base_name, extension=".png"):
    """Ensure unique filename by appending (1), (2), etc."""
    counter = 1
    filename = f"{base_name}{extension}"

    while os.path.exists(filename):  # Check if file exists
        filename = f"{base_name}({counter}){extension}"  # Add number
        counter += 1

    return filename

# Function to generate and display QR code with unique filename
def generate_qr():
    global last_filename  # Store last saved filename for "Open" and "Copy"
    data = qr_entry.get()
    if not data:
        return
    
    filename = get_unique_filename(sanitize_filename(data) + "_qr")
    qr = qrcode.make(data)
    qr.save(filename)
    last_filename = filename  # Save filename for buttons

    if os.path.exists(filename):  # Ensure the file exists before loading
        qr_image = ctk.CTkImage(light_image=Image.open(filename), size=(200, 200))
        qr_label.configure(image=qr_image)
        qr_label.image = qr_image
        open_button.configure(state="normal")  # Enable "Open" button
        copy_button.configure(state="normal")  # Enable "Copy" button
        print(f"QR Code saved as {filename}")

# Function to open the generated QR code
def open_qr():
    if last_filename and os.path.exists(last_filename):
        subprocess.run(["start", last_filename], shell=True)  # Opens the image

# Function to copy the QR code image to clipboard
def copy_qr():
    if last_filename and os.path.exists(last_filename):
        image = Image.open(last_filename)
        output = io.BytesIO()
        image.convert("RGB").save(output, format="BMP")

        data = output.getvalue()[14:]  # Remove BMP header

        # Copy image to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        print("QR Code copied to clipboard successfully!")

# Create main layout
frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

qr_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter text or URL")
qr_entry.pack(pady=10)

qr_button = ctk.CTkButton(frame, text="Generate QR Code", command=generate_qr)
qr_button.pack(pady=5)

qr_label = ctk.CTkLabel(frame, text="")  # No placeholder text
qr_label.pack(pady=10)

open_button = ctk.CTkButton(frame, text="Open QR Code", command=open_qr, state="disabled")
open_button.pack(pady=5)

copy_button = ctk.CTkButton(frame, text="Copy QR Code", command=copy_qr, state="disabled")
copy_button.pack(pady=5)

# Run the application
app.mainloop()
