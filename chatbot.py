from config import client
from config import logging
import json

with open("settings.json") as f:
    settings = json.load(f)
    
def chatbot(prompt, img):
    if img is None:  # Если нет картинки
        model = settings['models']['current_model_1']
        content = [{"type": "text", "text": prompt}]
    else:  # Есть картинка
        model = settings['models']['current_model_2']
        # Прикрепление к запросу ссылки на изображение
        content = [{"type": "text", "text": prompt}, { "type": "image_url", "image_url": {"url": img}}]

    completion = client.chat.completions.create(
        extra_body={},
        model=model,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    try:
        return completion.choices[0].message.content
    except Exception as e:
        logging.critical(str(e) + " - " + completion)
