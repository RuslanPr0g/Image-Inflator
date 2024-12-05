import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import struct
import os

WIDTH, HEIGHT = 1000, 1000

def open_image_and_convert():
    """Open an image, convert it to .trt format, and save it."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if not file_path:
        return
    
    try:
        image = Image.open(file_path)
        image = image.convert("RGBA")
        pixels = list(image.getdata())
        
        width, height = image.size
        compressed_data = compress_image(pixels, width, height)
        
        with open("converted_image.trt", "wb") as f:
            f.write(struct.pack("HH", width, height))
            f.write(compressed_data)
        
        messagebox.showinfo("Success", "Image converted and saved as 'converted_image.trt'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert image: {e}")

def open_and_display_image():
    """Read a .trt file, decompress it, and display the image."""
    try:
        with open("converted_image.trt", "rb") as f:
            width, height = struct.unpack("HH", f.read(4))
            compressed_data = f.read()
        
        pixels = decompress_image(compressed_data, width, height)
        
        image = Image.new("RGBA", (width, height))
        image.putdata([tuple(pixel) for row in pixels for pixel in row])
        
        update_image(image)
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'converted_image.trt' not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read and display image: {e}")

def compress_image(pixels, width, height):
    """Compress image data using RLE."""
    compressed_data = bytearray()
    for row in range(height):
        run_length = 1
        prev_pixel = pixels[row * width]
        
        for i in range(1, width):
            if pixels[row * width + i] == prev_pixel and run_length < 255:
                run_length += 1
            else:
                compressed_data.append(run_length)
                compressed_data.extend(prev_pixel)
                prev_pixel = pixels[row * width + i]
                run_length = 1
        
        compressed_data.append(run_length)
        compressed_data.extend(prev_pixel)
    
    return compressed_data

def decompress_image(compressed_data, width, height):
    """Decompress RLE-compressed image data."""
    pixels = []
    i = 0
    while i < len(compressed_data):
        run_length = compressed_data[i]
        rgba = compressed_data[i + 1:i + 5]
        pixels.extend([rgba] * run_length)
        i += 5
    
    return [pixels[i:i + width] for i in range(0, len(pixels), width)]

def update_image(image):
    """Update the displayed image in the Tkinter GUI."""
    global photo, label
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)

root = tk.Tk()
root.title("Custom TRT Image Viewer")

btn_convert = tk.Button(root, text="Convert Image to TRT Format", command=open_image_and_convert)
btn_convert.pack(pady=5)

btn_open = tk.Button(root, text="Open and Display Image", command=open_and_display_image)
btn_open.pack(pady=5)

initial_image = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 100))
photo = ImageTk.PhotoImage(initial_image)
label = tk.Label(root, image=photo)
label.pack(pady=80, padx=160)

root.mainloop()
