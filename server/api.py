import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import struct
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (you can restrict to certain domains if needed)

WIDTH, HEIGHT = 1000, 1000

@app.route('/convert', methods=['POST'])
def convert_image():
    """Convert an image to .trt format and send it as a downloadable file with a random name."""
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No image file provided"}), 400
    
    try:
        # Open and process the image
        image = Image.open(file)
        image = image.convert("RGBA")
        pixels = list(image.getdata())
        
        width, height = image.size
        compressed_data = compress_image(pixels, width, height)
        
        # Generate a random filename using uuid
        random_filename = f"{uuid.uuid4().hex}.trt"
        
        # Create the .trt file in memory (no saving on the server)
        trt_file = io.BytesIO()
        trt_file.write(struct.pack("HH", width, height))
        trt_file.write(compressed_data)
        trt_file.seek(0)  # Move the pointer to the start of the file
        
        # Send the file as a downloadable .trt with the random filename
        return send_file(
            trt_file,
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=random_filename
        )
    except Exception as e:
        return jsonify({"error": f"Failed to convert image: {str(e)}"}), 500

@app.route('/load-trt', methods=['POST'])
def load_trt_file():
    """Load a .trt file, decompress it, and return the image data as PNG."""
    file = request.files.get('trt_file')
    if not file:
        return jsonify({"error": "No TRT file provided"}), 400

    try:
        # Read the .trt file and extract data
        file_data = file.read()
        width, height = struct.unpack("HH", file_data[:4])
        compressed_data = file_data[4:]
        
        # Decompress the image data
        pixels = decompress_image(compressed_data, width, height)
        
        # Reconstruct the image
        image = Image.new("RGBA", (width, height))
        image.putdata([tuple(pixel) for row in pixels for pixel in row])
        
        # Save the image to a BytesIO buffer as PNG
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)  # Move to the beginning of the BytesIO buffer
        
        # Send the PNG image back to the client
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=False,
            download_name='image_from_trt.png'
        )
    except Exception as e:
        return jsonify({"error": f"Failed to process TRT file: {str(e)}"}), 500

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

if __name__ == '__main__':
    app.run(debug=True)
