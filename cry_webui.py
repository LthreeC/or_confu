import gradio as gr
import numpy as np
import cv2
import hashlib
import time

def string_to_16_digits(s):
    md5_hash = hashlib.md5(s.encode()).hexdigest()
    short_hash = md5_hash[:16]
    numeric_hash = int(short_hash, 16)
    return int(str(numeric_hash).zfill(16))

def crypt_image(select, img, key):
    img = np.array(img)
    if select == "Encrypt":
        key = string_to_16_digits(key) % (1<<32)
        np.random.seed(key)
        random_mask = np.random.randint(0, 256, size=img.shape, dtype=np.uint8)
        cipher_img = cv2.bitwise_xor(img, random_mask)
        for c in range(img.shape[2]):
            high_bits = cipher_img[:, :, c] >> 4
            low_bits = cipher_img[:, :, c] & 0x0F
            cipher_img[:, :, c] = (low_bits << 4) | high_bits
        return cipher_img
    elif select == "Decrypt":
        key = string_to_16_digits(key) % (1<<32)
        np.random.seed(key)
        for c in range(img.shape[2]):
            high_bits = img[:, :, c] >> 4
            low_bits = img[:, :, c] & 0x0F
            img[:, :, c] = (low_bits << 4) | high_bits 
        random_mask = np.random.randint(0, 256, size = img.shape, dtype = np.uint8)
        cipher_img = cv2.bitwise_xor(img, random_mask) 
        return cipher_img

global_loaded_image = None

def load_image(image):
    global global_loaded_image
    global_loaded_image = image
    return image

def process_image(select, key):
    tt_time = time.time()
    global global_loaded_image
    if global_loaded_image is None:
        return None
    return_val = crypt_image(select, global_loaded_image, key)
    print("总时间：", time.time() - tt_time)
    return return_val

with gr.Blocks() as demo:
    gr.Markdown("# image encryption and decryption")

    with gr.Row():
        with gr.Column():
            input_img = gr.Image(sources=["upload"], label="select image", type="pil")
            key_input = gr.Textbox(label="input key", type="text")
            with gr.Row():
                encrypt_button = gr.Button(value="encrypt", variant="primary")
                decrypt_button = gr.Button(value="decrypt ", variant="primary")
        with gr.Column():
            processed_img = gr.Image(label="processed image", format='png')
            
    input_img.change(fn=load_image, inputs=input_img, outputs=None)

    encrypt_button.click(fn=process_image, inputs=[gr.State("Encrypt"), key_input], outputs=processed_img)
    decrypt_button.click(fn=process_image, inputs=[gr.State("Decrypt"), key_input], outputs=processed_img)

demo.launch()