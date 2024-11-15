import cv2
from PIL import Image
import numpy as np
import hashlib
import time

def string_to_16_digits(s):
    md5_hash = hashlib.md5(s.encode()).hexdigest()
    short_hash = md5_hash[:16]
    numeric_hash = int(short_hash, 16)
    return int(str(numeric_hash).zfill(16))

def encrypt_image(image_path, key):
    key = (string_to_16_digits(key)) % (1<<32)
    img = cv2.imread(image_path)
    np.random.seed(key)
    random_mask = np.random.randint(0, 256, size = img.shape, dtype = np.uint8)
    cipher_img = cv2.bitwise_xor(img, random_mask)
    return cipher_img

def decrypt_image(image_path, key):
    key = (string_to_16_digits(key)) % (1<<32)
    img = cv2.imread(image_path)
    np.random.seed(key)
    random_mask = np.random.randint(0, 256, size = img.shape, dtype = np.uint8)
    cipher_img = cv2.bitwise_xor(img, random_mask)
    return cipher_img
    