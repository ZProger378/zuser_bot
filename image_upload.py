import base64
import requests

from config import img_bb


def upload_photo(img):
    with open(img, "rb") as file:  #
        # Запрос к api imgbb
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": img_bb['api_key'],
            "image": base64.b64encode(file.read()),
        }
        # Получение ответа
        res = requests.post(url, payload)

    # Возврат прямой ссылки
    return res.json()['data']['url']