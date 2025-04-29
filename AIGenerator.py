import json
import time
import base64
import requests
from PIL import Image
from io import BytesIO
from config import API_KEY, SECRET_KEY
import os

class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f'{prompt}'
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

    def decode_base64_to_image(self, base64_string):
        decoded_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(decoded_data))
        return image

def save_base64_images(self, base64_string, file_path):
    decoded_data = base64.b64decode(base64_string)

    image = Image.open(BytesIO(decoded_data))

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image.save(file_path)
    print(f"Görüntü kaydedildi: {file_path}")

def generate_image_from_text(prompt, api_url, api_key, secret_key):
    api = FusionBrainAPI(api_url, api_key, secret_key)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)
    return files

if __name__ == '__main__':
    api_url = 'https://api-key.fusionbrain.ai/'
    prompt = "Wave"

    files = generate_image_from_text(prompt, api_url, API_KEY, SECRET_KEY)

    # JSON olarak kaydet (istersen)
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=4, ensure_ascii=False)

    # Base64 veriyi resimlere çevir
    save_base64_images(files)
