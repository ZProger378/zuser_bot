ZUser_bot
---

**Дорогой дневник, мне не описать ту боль и унижение, что я испытал.**

**Дело в том, что это 2 файл ридми, я целый час его писал, а потом в один момент случился ```push --force```**

**Я навсегда запомню этот урок, и прежде чем вводить ```--force``` я буду думать...**

## Установка и настройка

**По классике**
```sh
git clone https://github.com/ZProger378/zuser_bot.git
```
```sh
cd zuser_bot
```

### Запуск:
1. Установите необходимые зависимости:
   ```sh
   pip3 install -r requirements.txt
   ```
2. Откройте файл `config.ini.example` и настройте

    [pyrogram] - api_hash, api_id - получаем в <https://my.telegram.org/apps>
    
    [TeleBot] - bot_token получаем у БотаБати, надеюсь ничего трудного в этом нет (бот будет использоваться для отправки удалённых сообщений вам в ЛС)
    
    [OpenRouter] - api_key получаем в <https://openrouter.ai/settings/keys>

    [Kandinsky] - api_key, secret_key - получаем в <https://fusionbrain.ai/keys/>
    
    [imgBB] - api_key получаем в <https://api.imgbb.com/>. ImgBB нужен для загрузки картинок в облако для дальнейшей отправки в нейросеть
3. После настройки переименуйте `config.ini.example` -> `config.ini` 
4. Запустите бота:
   ```sh
   python3 main.py
   ```
   При первом запуске будет необходимо авторизоваться

---

## Функции

### 1. ChatBot
**Команды:** `/chatbot`, `/ai`, `/ии`, `/чатбот`

**Пример**: `/ии Кто такой Роберт Оппенгеймер?`

Отправляет сообщение нейросети и получает ответ. Поддерживает текстовые сообщения и изображения.

---

### 2. Генерация изображений (Kandinsky)
**Команды:** `/img`, `/gen`, `/сгенерировать`, `/изображение`, `/картинка`

**Пример**: `/картинка небо с облаками`

Генерирует изображение с помощью Kandinsky API.

---

### 3. Анимация
**Команды:** `/1111`

Отображает анимацию с самолетом.

---

### 4. Анимация сердца
**Команды:** `/love`, `/люблю`

Отображает анимированное сердечко в сообщении.

---

### 5. Получение информации о сообщении
**Команды:** `/info`, `/инфа`

Выдает информацию о сообщении: ID чата, ID пользователя, ID сообщения, количество слов, абзацев, символов.

---

### 6. Статистика сообщений
**Команды:** `/statistic`, `/статистика`, `/стата`

Анализирует историю сообщений, подсчитывает количество слов, составляет статистику популярных слов.

**Внимание: НЕ ЮЗАТЬ В КРУПНЫХ ЧАТАХ.**

Функция отрабатывает долго. Чат с 20к сообщениям >5 минут переваривает