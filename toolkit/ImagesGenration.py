import asyncio
import requests
from random import randint
from PIL import Image
import os
from time import sleep

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
KEY_FILE = os.path.join("keys", "huggingface2")
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_api_key():
    with open(KEY_FILE, 'r') as f:
        return f.read().strip()

headers = {"Authorization": f"Bearer {get_api_key()}"}

async def query(payload, retries=3, backoff_factor=0.5):
    for attempt in range(retries):
        try:
            response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error during API request (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"Retrying in {sleep_time} seconds...")
                await asyncio.sleep(sleep_time)
            else:
                return None

async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {"inputs": f"{prompt} seed={randint(0, 100000)}"}
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)
    image_files = []

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            image_path = os.path.join(OUTPUT_DIR, f"image_{i + 1}.jpg")
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            image_files.append(image_path)
    
    return image_files

def Generate_Images(prompt: str):
    return asyncio.run(generate_images(prompt))

class Show_Image:
    def __init__(self, image_files: list) -> None:
        self.image_files = image_files

    def open(self, no):
        if no >= len(self.image_files):
            print("No more images to show.")
            return
        try:
            img = Image.open(self.image_files[no])
            img.show()
        except Exception as e:
            print(f"Error opening image {self.image_files[no]}: {e}")
            self.open(no + 1)

    def close(self, no):
        # TODO: Implement if necessary
        pass
