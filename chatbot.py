from config import client
from config import logging


models = ["google/gemini-2.0-pro-exp-02-05:free", "google/gemini-2.0-flash-exp:free", "google/gemini-2.0-flash-lite-001", "google/gemini-flash-1.5-8b"]
def chatbot(prompt, img):
    if img is None:  # Если нет картинки
        model = models[1]  # Использование 2 модели
        content = [{"type": "text", "text": prompt}]
    else:  # Есть картинка
        model = models[1]  # Использование 1 модели
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