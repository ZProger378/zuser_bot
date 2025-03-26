import base64
import json
import time
import requests

# Всё на что падают лучи солнца - спизженно под чистую с официального сайта API Fusion Brain
# P.S. Я так и не понял, как работает цензура. Вроде бы голых тянок рисует,
# но иногда на слишком наркоманские запросы кидает какой-то синий героиновый приход, вместо результата.

# Класс для работы с Кандинским
class Text2ImageAPI:
    # Инициализация
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    # Получение названия модели
    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    # Начать генерацию
    def generate(self, prompt, images=1, width=1024, height=1024):
        model = self.get_model()
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        # Отправка запроса
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()

        # Возврат результата
        return data['uuid']

    # Получение изображения
    def check_generation(self, request_id, attempts=30, delay=5):
        while attempts > 0:  # Пока не кончатся попытки (30 раз с промежутком в 5 секунд)
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

        # Кончились попытки -> возврат None
        return None

    # Генерация изображения
    def generate_image(self, prompt):
        uuid = self.generate(prompt)  # Начать генерацию
        images = self.check_generation(uuid)  # Получения изображения
        if images is not None:  # Если успешно сгенерировались
            for index, img in enumerate(images):
                # Запись изображений в файл
                with open(f"downloads/{index}.png", "wb") as fh:
                    fh.write(base64.decodebytes(bytes(img, "utf-8")))
            return "OK"
        else:
            return None
