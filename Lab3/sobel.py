from PIL import Image, ImageOps
from multiprocessing import Pool
import numpy as np
import os

mask_horizontal = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])

mask_vertical = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
])


def div_img(img, n):
    width, height = img.size

    img_gray = ImageOps.grayscale(img)
    img_gray_np = np.array(img_gray)
    img_gray_np_padded = np.pad(img_gray_np, pad_width=1, mode='constant', constant_values=0)

    img_fragments = list()
    step = height // n

    for i in range(n):
        start = i * step
        end = (i+1)* step if i < n-1 else height
        padded_start = start
        padded_end = end + 2
        img_fragments.append(img_gray_np_padded[padded_start:padded_end, :])

    return img_fragments


def join_img(img_fragments):
    full_img_np = np.vstack(img_fragments)
    full_img = Image.fromarray(full_img_np.astype(np.uint8))

    return full_img


def sobel_filter(img_np):
    height, width = img_np.shape
    output = np.zeros((height - 2, width - 2), dtype=np.uint8)

    for y in range(height - 2):
        for x in range(width - 2):
            region = img_np[y:y+3, x:x+3]
            Gx = np.sum(region * mask_horizontal)
            Gy = np.sum(region * mask_vertical)
            magnitude = np.sqrt(Gx**2 + Gy**2)
            value = int(np.clip(magnitude, 0, 255))
            output[y, x] = value

    return output


if __name__ == '__main__':

    img_path = 'img1.png'
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"File not found: {img_path}")
    
    img = Image.open(img_path)
    
    strips = div_img(img, 10)

    with Pool(10) as p:
        results = p.map(sobel_filter, strips)

    sobel_img = join_img(results)
    sobel_img.show()