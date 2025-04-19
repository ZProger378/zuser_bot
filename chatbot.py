from config import client
import json

 
def chatbot(prompt, img):
    # Загрузка настроек выбранной модели
    with open("settings.json") as f:
        settings = json.load(f)

    # Базовый запрос
    content = [{"type": "text", "text": prompt}]
    if img is None:  # Если нет картинки
        model = settings['models']['current_model_1']
    else:  # Есть картинка
        model = settings['models']['current_model_2']
        # Прикрепление к запросу ссылки на изображение
        content.append({"type": "image_url", "image_url": {"url": img}})

    completion = client.chat.completions.create(
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

