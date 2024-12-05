# **Image Inflator** 🚀📸

**Image Inflator** is the *ultimate* tool you didn’t realize you needed to make your images **huge**—and we mean **HUGE**! 😱👀 No more small, pixelated pics. This app blows up your images to ridiculous proportions using my custom *TRT* (Torture-Resize-Technic) format, just to mess with your mind and really, really annoy you! 🎯 Get ready for **absurd** sizes that’ll make your browser choke. Perfect for frustrating the user, if that’s your vibe. 💯🎉

---

## Features 🎨

- **Mind-Boggling Size:** Your images get scaled to **massive** proportions. Quality? Who cares when it’s this big? 🏋️‍♂️
- **Complete Support:** JPG, PNG, BMP, you name it—everything will be distorted to oblivion. ✅
- **Custom Scaling (for Maximum Irritation):** Choose your scale factor, but don’t blame us when the image is *way* too big to handle. 💥
- **Batch Chaos:** Want to break the web with a bunch of ginormous images? Go ahead, process a ton at once! 🔄
- **Totally Ridiculous Interface:** Get ready to work with an interface designed to maximize confusion and frustration. No more simple apps—this one’s here to mess with your sanity! 🤡

---

## Installation 🛠️

### Prerequisites 📥

- **JavaScript (JS):** Don’t worry, we’ve got some JS madness happening behind the scenes. ⚡
- **HTML/CSS:** Yes, we’re torturing your images with the power of web tech.
  
### Steps 👇

1. Clone this **epic** repo:
   ```bash
   git clone https://github.com/yourusername/image-inflator.git
   ```

2. Navigate to your project directory (you know the drill):
   ```bash
   cd image-inflator
   ```

3. Open the files in your browser, no dependencies needed—except your patience! 🎯

---

## Usage 🕶️

### The Live Server Madness 🚀

Yo, let’s get that **crazy image blow-up action** going! You ready for this? 🔥👑 Just serve that `index.html` on a live server and you’ll be good to go. Here’s how:

1. Install **Live Server** extension in your code editor (like VS Code). Don’t trip, it’s mad simple. 👨‍💻
   
2. Open up `index.html` and click that **"Go Live"** button in VS Code (or whatever editor you’re using). Watch your image *explode* to **ridiculous** sizes. 🤯

3. Sit back, relax, and enjoy the chaos as you turn any image into an **unmanageable giant**. 

---

## Supported Formats 🎬

- **Input:** JPG, PNG, BMP, TIFF—anything you want to make **too big**. 
- **Output:** JPG, PNG, BMP, TIFF—expect a file that may take **ages** to load. We’re serious about those sizes.

---

## Algorithm 🧠

The **Image Inflator** uses a custom compression algorithm to transform the image into an absurdly large format, which is then saved as a `.trt` file. Here's how it works:

### 1. **Image Compression to TRT Format**:

- **Step 1: Load the Image**: The image file is loaded using the HTML `<input>` element. Once the image is loaded, it is drawn on a canvas using the Canvas API.

- **Step 2: Get Image Data**: The `ImageData` object is created from the canvas. This object contains pixel data for the image (RGBA values).

- **Step 3: Run-Length Encoding (RLE)**:
  - The pixel data is compressed using a technique called **Run-Length Encoding** (RLE). This technique identifies sequences of identical pixels (runs) and stores them as a single value (the pixel and its count).
  - **Example**: If there are 10 consecutive pixels with the color red, the run would be compressed into `[10, red]` instead of storing 10 individual red pixels.

- **Step 4: Store Image Dimensions**: The width and height of the image are stored in the header of the `.trt` file to ensure that it can be decompressed and displayed correctly later.

- **Step 5: Save as .TRT**: The final `.trt` file is created by combining the header (image dimensions) and the compressed pixel data. This file is then ready for download.

### 2. **Decompressing the TRT File**:

- **Step 1: Load the TRT File**: The user can upload a `.trt` file through the interface.
  
- **Step 2: Read Header**: The width and height of the image are extracted from the first few bytes of the `.trt` file.

- **Step 3: Decompress Pixel Data**:
  - The run-length encoded pixel data is decoded back into individual pixel values.
  - The code iterates through the compressed data, expanding each run of pixels into the full set of pixels.
  
- **Step 4: Display the Image**: Once the pixel data is decompressed, an `ImageData` object is created and drawn to the canvas. The image is now displayed in the preview section of the page.

This simple but absurd approach to image manipulation will make images go from normal size to absurdly large—guaranteeing a chaotic user experience. 😜

---

## Contributing 🤝

Want to mess with this even more? Fork the repo and send in some extra ways to irritate users! 👯‍♂️

1. Fork the repo (because who doesn’t want to control chaos?) 🍴
2. Create a new branch (`git checkout -b torture-format-improvements`).
3. Commit your changes with a smile (`git commit -am 'Added more ways to break stuff'`).
4. Push your branch (`git push origin torture-format-improvements`).
5. Send the PR, if you dare. 🙌

---

## License 📝

This project is under the MIT License. But let’s be real, you’ll probably wish you didn’t use it. 🔓

---

## Shoutouts 🙌

- **Canvas API:** Used to make sure your images get **stretched** like crazy. 🎨
- **HTML5:** All the magic happens with pure web tech. Because why not make your life harder? 🧙‍♂️

---

Get ready to *blow up* your images—literally—using **Image Inflator**. Because why settle for normal when you can go **way too far**? 🎉💥