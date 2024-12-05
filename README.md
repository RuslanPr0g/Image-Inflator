## Installation 🛠️

### Prerequisites 📥

- **Node.js** (for live server support)
- **Flask** (for the backend)
- **Python** (for running the server)
- **Pillow** (for image processing in the backend)

### Steps 👇

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/image-inflator.git
   ```

2. **Navigate to your project directory**:
   ```bash
   cd image-inflator
   ```

3. **Set up the Python backend**:
   - Install the necessary Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - `requirements.txt` should contain:
     ```
     Flask==2.3.2
     flask-cors==3.1.1
     Pillow==9.2.0
     ```

4. **Start the Flask server**:
   - Run the Flask server:
     ```bash
     python app.py
     ```

   This will start the server locally at `http://127.0.0.1:5000`.

5. **Set up Live Server for the frontend**:
   - If you’re using **VS Code**, install the **Live Server** extension.
   - Open `index.html` and click the **"Go Live"** button in the VS Code toolbar to launch the frontend in your browser.

   Now, the app will be live on your local browser and can interact with the Flask backend.

---

## Usage 🕶️

### The Live Server Madness 🚀

Let’s get that **crazy image blow-up action** going! 🔥👑 Follow these steps to convert and display your images:

1. **Upload an Image**:
   - Click the **"Choose File"** button to select an image file from your computer.
   - Click **"Convert Image"** to send the image to the backend for conversion into the `.trt` format.

2. **Download the Converted Image**:
   - After processing, the image will be downloaded as a `.trt` file.

3. **Load a `.trt` File**:
   - Upload a `.trt` file using the **"Load TRT File"** button.
   - The image will be decompressed and displayed in the browser.

Enjoy turning normal images into **mind-bogglingly huge** ones! 🤯