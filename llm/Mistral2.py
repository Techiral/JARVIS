from huggingface_hub import InferenceClient
import random
from time import sleep, time as t
from os import listdir

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
# Replace YOUR_API_KEY_HERE with the obtained API key from Hugging Face
headers = {"Authorization": f"Bearer {open('keys//huggingface').read()}"}

def LoadInjection(end="mistral"):
    files = listdir(r"injection/")
    TotData = []
    for i in files:
        if i.split(".")[-1] == end:
            with open(fr"injection/{i}","r") as f:
                data = f.read()
            temp = {"role": "system", "content": data}
            TotData.append(temp)
    return TotData

messages = [
    {"role": "system", "content": "I'm the latest JARVIS AI, designed by Techiral with capabilities to access systems through various programming languages using modules like webbrowser, pyautogui, time, pyperclip, random, mouse, wikipedia, keyboard, datetime, tkinter, PyQt5, etc."},
    {"role": "user", "content": "Open Google Chrome."},
    {"role": "assistant", "content": "```python\nimport webbrowser\nwebbrowser.open('https://www.google.com')```"},
    {"role": "system", "content": "Python includes built-in functions you can use. For instance:"},
    ]
'''{"role": "system", "content": """```python
from Genration_Of_Images import Generate_Images, Show_Image
IMGS = Generate_Images(prompt="iron man")
print(IMGS)
IMGS_TO_SHOW = Show_Image(IMGS)
IMGS_TO_SHOW.open(0)
IMGS_TO_SHOW.open(1)
```"""},
    {"role": "user", "content": "Jarvis, generate a cute cat image using Python."},
    {"role": "assistant", "content": """```python
from Genration_Of_Images import Generate_Images, Show_Image
IMGS = Generate_Images(prompt="A playful kitten with bright eyes and a fluffy tail.")
IMGS_TO_SHOW = Show_Image(IMGS)
IMGS_TO_SHOW.open(0)
```"""},
    {"role": "user", "content": "Jarvis, show me the next image using Python."},
    {"role": "assistant", "content": """```python
IMGS_TO_SHOW.open(1)
```"""}'''

messages.extend(LoadInjection())

# Function to format prompt
def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f"[INST] {custom_instructions} [/INST]"
    prompt += f"[INST] {message} [/INST]"
    return prompt

# Function to generate response based on user input
def Mistral7B(prompt, temperature=0.9, max_new_tokens=1024, top_p=0.95, repetition_penalty=1.0):
    start_time = t()
    temperature = max(float(temperature), 1e-2)
    top_p = max(float(top_p), 0.1)

    generate_kwargs = {
        "temperature": temperature,
        "max_new_tokens": max_new_tokens,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "do_sample": True,
        "seed": random.randint(0, 10**7),
    }

    custom_instructions = str(messages)
    formatted_prompt = format_prompt(prompt, custom_instructions)
    messages.append({"role": "user", "content": prompt})

    while True:
        try:
            client = InferenceClient(API_URL, headers=headers)
            response = client.text_generation(formatted_prompt, **generate_kwargs)
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying after 10 seconds...")
            sleep(10)  # Add a delay before retrying

    messages.append({"role": "assistant", "content": response})
    print(f"Response time: {t() - start_time} seconds")
    return response

if __name__ == "__main__":
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == 'exit':
            break

        generated_text = Mistral7B(user_prompt)
        print("Bot:", generated_text)
