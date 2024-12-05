const convertButton = document.getElementById('convertButton');
const trtInput = document.getElementById('trtInput');
const imageInput = document.getElementById('imageInput');
const downloadLink = document.getElementById('downloadLink');
const canvas = document.getElementById('imageCanvas');
const ctx = canvas.getContext('2d');

let imageData = null;

convertButton.addEventListener('click', () => {
    const file = imageInput.files[0];
    if (!file) {
        alert('Please upload an image first.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            imageData = ctx.getImageData(0, 0, img.width, img.height);

            const compressedData = compressImage(imageData.data, img.width, img.height);
            const trtData = createTRTFormat(img.width, img.height, compressedData);

            const blob = new Blob([trtData], { type: 'application/octet-stream' });

            const filename = generateRandomFilename() + '.trt';
            const url = URL.createObjectURL(blob);

            downloadLink.href = url;
            downloadLink.download = filename;
            downloadLink.style.display = 'inline-block';

            alert('Image converted to TRT format! You can download it now.');
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
});

trtInput.addEventListener('change', () => {
    const file = trtInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        const trtData = new Uint8Array(event.target.result);
        const { width, height, compressedData } = parseTRTFormat(trtData);

        const pixels = decompressImage(compressedData, width, height);
        const newImageData = new ImageData(new Uint8ClampedArray(pixels), width, height);

        canvas.width = width;
        canvas.height = height;
        ctx.putImageData(newImageData, 0, 0);
    };
    reader.readAsArrayBuffer(file);
});

function compressImage(data, width, height) {
    const compressed = [];
    let index = 0;

    for (let row = 0; row < height; row++) {
        let runLength = 1;
        const prevPixel = [data[index], data[index + 1], data[index + 2], data[index + 3]];

        for (let col = 1; col < width; col++) {
            index += 4;
            const pixel = [data[index], data[index + 1], data[index + 2], data[index + 3]];
            if (pixelsAreEqual(pixel, prevPixel) && runLength < 255) {
                runLength++;
            } else {
                compressed.push(runLength);
                compressed.push(...prevPixel);
                runLength = 1;
            }
        }
    }

    return compressed;
}

function decompressImage(compressedData, width, height) {
    const pixels = [];
    let i = 0;
    const totalPixels = width * height;

    while (i < compressedData.length && pixels.length < totalPixels * 4) {
        const runLength = compressedData[i];
        const rgba = compressedData.slice(i + 1, i + 5);
        for (let j = 0; j < runLength; j++) {
            pixels.push(...rgba);
        }
        i += 5;
    }

    // Ensure the correct number of pixels (width * height)
    while (pixels.length < totalPixels * 4) {
        pixels.push(0, 0, 0, 255); // Fill with transparent black pixels
    }

    return pixels;
}

function pixelsAreEqual(p1, p2) {
    return p1[0] === p2[0] && p1[1] === p2[1] && p1[2] === p2[2] && p1[3] === p2[3];
}

function createTRTFormat(width, height, compressedData) {
    const header = new Uint8Array(4);
    header[0] = width >> 8;
    header[1] = width & 0xFF;
    header[2] = height >> 8;
    header[3] = height & 0xFF;

    const combinedData = new Uint8Array(header.length + compressedData.length);
    combinedData.set(header);
    combinedData.set(compressedData, header.length);

    return combinedData;
}

function parseTRTFormat(data) {
    const width = (data[0] << 8) | data[1];
    const height = (data[2] << 8) | data[3];
    const compressedData = data.slice(4);

    return { width, height, compressedData };
}

function generateRandomFilename() {
    return 'image_' + Date.now();
}
