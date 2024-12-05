const convertButton = document.getElementById('convertButton');
const loadButton = document.getElementById('loadButton');
const imageInput = document.getElementById('imageInput');
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

            // Save to localStorage (simulating a file save)
            localStorage.setItem('trtImage', trtData);

            alert('Image converted and saved in TRT format!');
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
});

loadButton.addEventListener('click', () => {
    const trtData = localStorage.getItem('trtImage');
    if (!trtData) {
        alert('No TRT data found!');
        return;
    }

    const { width, height, compressedData } = JSON.parse(trtData);
    const pixels = decompressImage(compressedData, width, height);

    const newImageData = new ImageData(new Uint8ClampedArray(pixels), width, height);
    ctx.putImageData(newImageData, 0, 0);
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

    while (i < compressedData.length) {
        const runLength = compressedData[i];
        const rgba = compressedData.slice(i + 1, i + 5);
        for (let j = 0; j < runLength; j++) {
            pixels.push(...rgba);
        }
        i += 5;
    }

    return pixels;
}

function pixelsAreEqual(p1, p2) {
    return p1[0] === p2[0] && p1[1] === p2[1] && p1[2] === p2[2] && p1[3] === p2[3];
}

function createTRTFormat(width, height, compressedData) {
    return JSON.stringify({ width, height, compressedData });
}
