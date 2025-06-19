import os
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("API_KEY")

import requests
import re
from datetime import datetime

def generate_image_with_prompt(prompt, output_size="1792x1024"):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size=output_size
    )
    image_url = response.data[0].url
    print(f"Generated image URL: {image_url}")

    # Prepare output directory
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize prompt for filename
    safe_prompt = re.sub(r'[^a-zA-Z0-9_-]', '_', prompt)[:40]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_prompt}_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)

    # Download and save image
    try:
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Image saved to: {output_path}")
    except Exception as e:
        print(f"Failed to save image: {e}")

    return image_url

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    generate_image_with_prompt(prompt)
