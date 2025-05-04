# Для функции удаления
import os
# Для задержки в анимациях
from time import sleep

# Для работы с настройками
import json

import requests

# Клавиатуры
import markups

# PyroGram и БЛА-БЛА-БЛА
import pyrogram.enums
from pyrogram import filters
from pyrogram.errors import FloodWait

# Функция для генерирования псевдослучайного числа
from random import randint
# Хуй знает зачем, мне так ГПТ отрефакторил
from collections import defaultdict
# Аналогично
from copy import deepcopy

# Мои модули
from config import user, bot, message_store
from chatbot import chatbot
from monster import generate_image
from image_upload import upload_photo

# Для сравнения слов
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


###################################################################################################################
# Привет, друг, если ты сюда зашел, значит тебе либо нехуй делать, либо ты мне не доверяешь. И ничего в этом нет. #
# Я бы себе тоже не доверял =)                                                                                    #
# Изначально я лишь хотел встроить ИИ в телеграм, но потом как-то закрутилось. Крч удачи здесь что-то понять.     #
###################################################################################################################


# ChatBot
@user.on_message(filters.command(["chatbot", "ai", "ии", "чатбот"]) & filters.me)
def chat_handler(client, message):
    """
    Та самая функция, ради которой это всё и затевалось
    """
    try:
        user.edit_message_text(message.chat.id, message.id, f"Думаю...")
    except FloodWait as e:
        sleep(e.x)

    if message.media is None:  # Текст
        if message.reply_to_message_id is not None:  # Если сообщение - ответ
            command = message.text.split(" ")[0]
            mes = user.get_messages(message.chat.id, message.reply_to_message_id)
            if mes.media is None:
                prompt = mes.text + "\n\n" + message.text.replace(command, "")
                img_url = None
            else:
                prompt = message.text.replace(command, "")
                file = user.download_media(mes)  # Загрузка картинки локально
                img_url = upload_photo(file)  # Загрузка в облако и получение прямой ссылки
        else:
            command = message.text.split(" ")[0]
            prompt = message.text.replace(command, "")
            img_url = None
    else:  # Фото
        command = message.caption.split(" ")[0]
        prompt = message.caption.replace(command, "")
        file = user.download_media(message)  # Загрузка картинки локально
        img_url = upload_photo(file)  # Загрузка в облако и получение прямой ссылки
    try:
        result = f"**{prompt}**\n\n" + chatbot(prompt, img=img_url)  # Отправка запроса в нейросеть
    except Exception as e:
        result = f"**{prompt}**\n\nОшибка генерации: ```{e}```"

    ####################
    # Вывод результата #
    ####################

    # Если результат не превышает лимит телеграма
    if len(result) <= 4096 and message.media is None:
        try:
            user.edit_message_text(message.chat.id, message.id, result)
        except FloodWait as e:
            sleep(e.x)
    elif len(result) <= 1024 and message.media is not None:
        try:
            user.edit_message_text(message.chat.id, message.id, result)
        except FloodWait as e:
            sleep(e.x)
        os.remove(str(file))
    # Слишком большой результат
    else:
        if message.media is not None:
            user.send_photo(message.chat.id, file)
            os.remove(str(file))
        user.delete_messages(message.chat.id, message.id)

        # Разбивка результата на секторы по 4096 символов
        # Пробовал юзать wrap, но он удалял окончания строк и ответ был сплошным текстом без абзацев
        texts = [result[i:i + 4096] for i in range(0, len(result), 4096)]
        # Отправка ответа кусками
        for text in texts:
            user.send_message(message.chat.id, text)



# MonsterAPI 
@user.on_message(filters.command(["img", "gen", "сгенерировать", "изображение", "картинка"]) & filters.me)
def image_generation_handler(client, message):
    """
    Самая бесполезная функция, а именно - генерация картинки 

    P.S.
    Переехал с Кандинского на МонстерАПИ, так как Кандинский перестал работать, да и качество генерации было ну таким
    """
    if message.reply_to_message_id is not None:  # Если сообщение - ответ
        mes = user.get_messages(message.chat.id, message.reply_to_message_id)
        prompt = mes.text
    else:
        command = message.text.split(" ")[0]
        prompt = message.text.replace(command, "")
    try:
        user.edit_message_text(message.chat.id, message.id, f"Генерирую...")
    except FloodWait as e:
        sleep(e.x)
    # Генерация изображения
    req = generate_image(prompt)
    if req is not None:  # Успешная генерация
        r = requests.get(req[0])
        with open("downloads/0.png", "wb") as f:
            f.write(r.content)
        user.delete_messages(message.chat.id, message.id)
        user.send_photo(message.chat.id, "downloads/0.png", prompt)
        os.remove("downloads/0.png")  # Удаление сгенерированной картинки с сервера
    else:
        try:
            user.edit_message_text(message.chat.id, message.id, f"Ошибка в процессе генерации изображения")
        except FloodWait as e:
            sleep(e.x)



# 11.09.2001 - на всякий случай скажу, что кодил крайне осуждающе
@user.on_message(filters.command(["1111"]) & filters.me)
def _11_11_handler(client, message):
    """
    Одним утром мне было нехуй делать и пришла гениальная идея, кстати после этой функции я и сделал анимированное сердце
    """
    # Начальный кадр
    render = ".🛫                                          🏬"
    # Отрисовка кадра
    try:
        user.edit_message_text(message.chat.id, message.id, render)
    except FloodWait as e:
        sleep(e.x)

    # Перемещение самолета на 3 клетки каждую секунду
    plane_x = 2
    while plane_x < 43:
        plane_x += 3
        render = ""
        # Отрисовка каждой сущности в анимации
        for i in range(44):
            if not i: render += "."  # Точка в начале
            elif i == plane_x: render += "🛫"  # Сам самолет
            elif i == 43: render += "🏬"  # Башня
            else: render += " "  # Просто пробел)
        try:
            user.edit_message_text(message.chat.id, message.id, render)
        except FloodWait as e:
            sleep(e.x)
        sleep(0.5)  # 2FPS без учета флудваита и пинга с самим телеграм апи

    # Взрыв в конце
    try:
        user.edit_message_text(message.chat.id, message.id, "🔥")
    except FloodWait as e:
        sleep(e.x)



# Та самая хрень, что тебе никогда не понадобится, если ты это читаешь
@user.on_message(filters.command(["love", "люблю"]) & filters.me)
def love_handler(client, message):
    """
    Делает милую анимацию с сердечком

    P.S.
    Анимацию пришлось сделать маленькой из-за FloodWait. Плюсом даже после отработки анимации очень легко словить то же исключение
    """
    heart_1 = (
             "◻️◻️◻️◻️◻️◻️◻️◻️◻️◻️◻️\n"
             "◻️◻️🟥🟥🟥◻️🟥🟥🟥◻️◻️\n"
             "◻️🟥🟥🟥🟥🟥🟥🟥🟥🟥◻️\n"
             "◻️🟥🟥🟥🟥🟥🟥🟥🟥🟥◻️\n"
             "◻️◻️🟥🟥🟥🟥🟥🟥🟥◻️◻️\n"
             "◻️◻️◻️🟥🟥🟥🟥🟥◻️◻️◻️\n"
             "◻️◻️◻️◻️🟥🟥🟥◻️◻️◻️◻️\n"
             "◻️◻️◻️◻️◻️🟥◻️◻️◻️◻️◻️\n"
             "◻️◻️◻️◻️◻️◻️◻️◻️◻️◻️◻️")
    heart_2 = (
             "◻️🟥🟥🟥◻️◻️◻️🟥🟥🟥◻️\n"
             "🟥🟥🟥🟥🟥◻️🟥🟥🟥🟥🟥\n"
             "🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
             "🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\n"
             "◻️🟥🟥🟥🟥🟥🟥🟥🟥🟥◻️\n"
             "◻️◻️🟥🟥🟥🟥🟥🟥🟥◻️◻️\n"
             "◻️◻️◻️🟥🟥🟥🟥🟥◻️◻️◻️\n"
             "◻️◻️◻️◻️🟥🟥🟥◻️◻️◻️◻️\n"
             "◻️◻️◻️◻️◻️🟥◻️◻️◻️◻️◻️")
    for i in range(10):
        # ЕБАННЫЙ АПИ ТЕЛЕГРАМА. Он не позволяет сделать слипы меньше, иначе ФлудВаит. Пульс у этой анимации 52 удара
        try:
            user.edit_message_text(message.chat.id, message.id, heart_1)
        except FloodWait as e:
            sleep(e.x)
        sleep(1.3)
        try:
            user.edit_message_text(message.chat.id, message.id, heart_2)
        except FloodWait as e:
            sleep(e.x)
        sleep(1)



# Кидает характеристики чата и сообщения
@user.on_message(filters.command(["info", "инфа"]) & filters.me)
def info_handler(client, message):
    """
    Просто скидывает параметры чата и сообщения, на которое ты ответил
    """
    # Получает текст или описание картинки
    # P.S. Что-то я тут нахуевертил, что сам нихуя не понимаю, но оно работает
    mes = user.get_messages(message.chat.id, message.reply_to_message_id) if message.reply_to_message_id is not None else None
    text = (mes.text if message.text is not None else mes.caption) if mes is not None else None

    # Если текст не нон
    if text is not None:
        # Получает характеристики сообщения
        words_count = len([i for i in text.split(" ") if i])  # Считает слова
        par_count = len([i for i in text.split("\n") if i.replace(" ", "")])  # Считает абзацы
        sym_count = len(text)  # Считает общее кол-во символов
        try:
            user.edit_message_text(message.chat.id, message.id, f"<b>ID чата</b>: <code>{mes.chat.id}</code>\n"
                                                                f"<b>ID юзера</b>: <code>{mes.from_user.id}</code>\n"
                                                                f"<b>ID сообщения</b>: <code>{mes.id}</code>\n\n"
                                                                f"<b>Кол-во слов</b>: <b>{words_count}</b>\n"
                                                                f"<b>Кол-во абзацев</b>: <b>{par_count}</b>\n"
                                                                f"<b>Кол-во символов</b>: <b>{sym_count}</b>",
                                   parse_mode=pyrogram.enums.ParseMode.HTML)
        except FloodWait as e:
            sleep(e.x)
    else:
        try:
            if mes is not None:
                user.edit_message_text(message.chat.id, message.id, f"<b>ID чата</b>: <code>{mes.chat.id}</code>\n"
                                                                    f"<b>ID юзера</b>: <code>{mes.from_user.id}</code>\n"
                                                                    f"<b>ID сообщения</b>: <code>{mes.id}</code>",
                                       parse_mode=pyrogram.enums.ParseMode.HTML)
            else:
                user.edit_message_text(message.chat.id, message.id, f"<b>ID чата</b>: <code>{message.chat.id}</code>\n"
                                                                    f"<b>ID юзера</b>: <code>{message.from_user.id}</code>",
                                       parse_mode=pyrogram.enums.ParseMode.HTML)
        except FloodWait as e:
            sleep(e.x)



# Составляет статистику наиболее часто используемых слов (НЕ ЮЗАТЬ В КРУПНЫХ ЧАТАХ)
# P.S. Отрабатывает очень долго, в чатах по 20к сообщений минут 5 тратит на то, чтобы извлечь всю историю переписки
# U.D. "БЛЯТЬ, я заплакал" (с) Тиньков
@user.on_message(filters.command(["statistic", "статистика", "стата"]) & filters.me)
def statistic_handler(client, message):
    """
    Извлекает сообщения из чата, анализирует текст, подсчитывает слова и формирует статистику.

    P.S.
    Парни, изучайте алгоритмы, в эту хрень писал часа 2 и этот пиздец чатгпт только с 4 раза отрефакторил
    """
    # Обновляем сообщение о начале обработки
    edit_message(message, "**Извлекаю сообщения...**")

    # Извлекаем историю сообщений
    messages = list(user.get_chat_history(message.chat.id))

    # Обновляет сообщение
    edit_message(message, "**Считаю слова...**")

    # Инициализация счетчиков и словарей
    is_media = 0
    is_text = 0
    word_count = defaultdict(lambda: defaultdict(int))  # {user_id: {word: count}}
    uncensured_word_count = defaultdict(int)
    all_word_count = defaultdict(int)
    senders = defaultdict(int)  # {user_id: message_count}

    # Игнорируемые слова, не включаемые в статистику
    ignored_words = {"кто", "кем", "чтоли", "чем", "тем", "как", "эта", "этот", "что-то", "что", "как-то", "как-нибудь",
                     "нибудь", "она", "оно", "они", "это", "для", "или", "его", "который", "если", "без", "так",
                     "также", "даже", "чтобы", "только", "при", "про", "еще", "ещё", "там", "уже", "всё", "все", "я",
                     "меня", "мной", "мне", "вот", "когда", "тогда", "тот", "тут", "тоже", "раз", "где", "тобой",
                     "тебе", "тебя", "себя", "собой", "него", "неё", "после", "нет"}

    # Великий и могучий русский, ёбанный его рот
    # P.S. мой словарный запас, во время написания этого хэндлера be like
    uncensured_words = {"хуй", "хуи", "пиздец", "пизда", "ебать", "ебал", "ахуеть", "охуеть", "опиздохуеть", "блять",
                        "бля", "блядь", "бляздец", "гандон", "гондон", "нахуй", "нахуя", "разъебать", "разъебанный",
                        "ёбанный", "ебанный", "наебать", "уебок", "уёбок", "уебать", "хуесос", "похуй", "нихуя", "охуенно",
                        "охуенный", "охуенная", "охуенное", "хуесосик", "хуесосина", "хуесосище", "долбаёб", "долбаеб",
                        "далбаеб", "далбаёб", "ебало", "ебала", "залупа", "блядина", "залупы", "блядины", "еблан",
                        "еблана", "пиздопротивный", "пиздопротивно", "пиздопротивное", "пиздопротивная", "схуя",
                        "схуяли", "идинахуй", "динахуй", "динаху", "зуй", "еби", "ебите", "ебитесь", "ебали", "ебала",
                        "заебали", "заебли", "заебала", "заебла", "заеб", "заебал", "уебская", "уёбская", "уебский",
                        "уёбский", "злоебучий", "злоебучая", "злоебучее", "злоебучие", "нахуячил", "нахуячить",
                        "нахуячила", "нахуячило", "еблет", "хуепутала", "еблетом", "еблета", "хуепутало", "хуепуталом",
                        "захуячил", "захуячить", "захуячила", "захуячило", "пидор", "пидора", "пидорас", "пидораса",
                        "спиздить", "спиздил", "спиздила", "спиздило", "упиздил", "упиздила", "упидить", "упиздило"}

    # Допускаемые символы в слове
    valid_chars = set("qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбюё-")

    # Обрабатываем каждое сообщение
    for msg in messages:
        # Извлекаю текст
        text = msg.caption if msg.media else msg.text

        # Определяю тип сообщения и прибавляю соответствующий счётчик
        if msg.media:
            is_media += 1
        else:
            is_text += 1

        # Обработка текста (если он есть)
        if text:
            text = text.lower()  # Привожу к нижнему регистру
            words = ["".join([char for char in word if char in valid_chars]) for word in text.split()]
            words = [word for word in words if word and word not in ignored_words and len(word) > 2]

            for word in words:
                word_count[msg.from_user.id][word] += 1
                if word.replace("-", ""):
                    match, score = process.extractOne(word, uncensured_words, scorer=fuzz.ratio)
                    if score >= 85:
                        uncensured_word_count[msg.from_user.id] += 1
                    all_word_count[msg.from_user.id] += 1

        senders[msg.from_user.id] += 1

    # Обновляю сообщение
    edit_message(message, "**Составляю статистику...**")

    # Формируем рейтинг популярных слов для каждого пользователя
    rating = {}
    _word_count = deepcopy(word_count)

    for user_id, words in word_count.items():
        sorted_words = sorted(words, key=words.get, reverse=True)[:30]
        rating[user_id] = sorted_words

    # Отправляем статистику по пользователям
    user.delete_messages(message.chat.id, message.id)
    for user_id, words in rating.items():
        user_name = user.get_users(user_id).first_name
        words_stat = "\n".join(f"**{i+1})** {word} (**{_word_count[user_id][word]}**)" for i, word in enumerate(words))
        user.send_message(message.chat.id, f"**Статистика {user_name}**\n\n{words_stat}\n\n"
                                           f"**Кол-во матов: ** {uncensured_word_count[user_id]} "
                                           f"(**{round(uncensured_word_count[user_id] / all_word_count[user_id] * 100, 2)}%**)\n"
                                           f"**Общее кол-во слов:** {all_word_count[user_id]}")

    # Подсчет количества сообщений по пользователям
    senders_stat = "\n".join(
        f"**{user.get_users(user_id).first_name}**: {count} сообщени{'е' if count % 10 == 1 else 'я' if count % 10 in [2, 3, 4] else 'й'}"
        for user_id, count in senders.items()
    )

    # Вывод итогов
    user.send_message(message.chat.id, f"**Итоги**\n\n"
                                       f"**Всего сообщений**: {len(messages)}\n"
                                       f"**Медиа**: {is_media}\n"
                                       f"**Текст**: {is_text}\n\n"
                                       f"**Статистика по юзерам**\n"
                                       f"{senders_stat}")


# Хэндлер бота
@user.on_message(filters.chat(bot.get_me().id) & filters.me)
def bot_handler(client, message):
    command = message.text
    user_id = message.from_user.id
    if command == "/start" or command == "Профиль 👤":
        user_info = user.get_me()
        info = f"<b><i>{user_info.first_name}</i></b>\n\n<b>ID:</b> <code>{user_info.id}</code>\n<b>Username:</b> {'@' + user_info.username if user_info.username else 'Нет'}\n<b>Premium:</b> {'Да' if user_info.is_premium else 'Нет'}"
        photos = client.get_chat_photos(user_id)
        photos = [*photos]
        if len(photos) > 0:
            # Получаем ссылку на первую фотографию профиля (аватарку)
            photo_file = photos[0].file_id
            # Загружаем фотографию
            downloaded_file = client.download_media(photo_file)
            # Отправляю
            bot.send_photo(user_id, photo=open(str(downloaded_file), "rb"), caption=info, reply_markup=markups.main_markup())
            os.remove(str(downloaded_file))
        else:
            bot.send_message(user_id, info, reply_markup=markups.main_markup())

    elif command == "Тест ИИ-функций 🟢":
        mes = bot.send_message(user_id, f"<b>Проверка работоспособности ИИ-функций</b>\n\n"
                                        f"<b>Запрос к ИИ (без картинки):</b> <i>Загрузка</i>\n"
                                        f"<b>Запрос к ИИ (с картинкой):</b> <i>Загрузка</i>\n"
                                        f"<b>MonsterAPI:</b> <i>Загрузка</i>")
        # Тест модели без картинки
        try:
            chatbot("hi", None)
        except:
            test_1 = False
        else:
            test_1 = True
        # Обновляю сообщение
        bot.edit_message_text(chat_id=mes.chat.id, message_id=mes.id,
                              text=f"<b>Проверка работоспособности ИИ-функций</b>\n\n"
                                   f"<b>Запрос к ИИ (без картинки):</b> <i>{'OK' if test_1 else 'ERROR'}</i>\n"
                                   f"<b>Запрос к ИИ (с картинкой):</b> <i>Загрузка</i>\n"
                                   f"<b>MonsterAPI:</b> <i>Загрузка</i>")
        # Тест модели с картинкой
        try:
            chatbot("hi", "https://memchik.ru//images/memes/61994612b1c7e34675112608.jpg")
        except:
            test_2 = False
        else:
            test_2 = True
        # Обновляю сообщение
        bot.edit_message_text(chat_id=mes.chat.id, message_id=mes.id,
                              text=f"<b>Проверка работоспособности ИИ-функций</b>\n\n"
                                   f"<b>Запрос к ИИ (без картинки):</b> <i>{'OK' if test_1 else 'ERROR'}</i>\n"
                                   f"<b>Запрос к ИИ (с картинкой):</b> <i>{'OK' if test_2 else 'ERROR'}</i>\n"
                                   f"<b>MonsterAPI:</b> <i>Загрузка</i>")
        # Тест генерации изображения
        res = generate_image("blue sky")
        test_3 = True if res else False
        # Обновляю сообщение и вывожу результат каждого тестирования
        bot.edit_message_text(chat_id=mes.chat.id, message_id=mes.id,
                              text=f"<b>Проверка работоспособности ИИ-функций</b>\n\n"
                                   f"<b>Запрос к ИИ (без картинки):</b> <i>{'OK' if test_1 else 'ERROR'}</i>\n"
                                   f"<b>Запрос к ИИ (с картинкой):</b> <i>{'OK' if test_2 else 'ERROR'}</i>\n"
                                   f"<b>MonsterAPI:</b> <i>{'OK' if test_3 else 'ERROR'}</i>")


    elif command == "Скачать логи 📑":
        with open("py_log.log") as f:
            bot.send_document(user_id, f, caption="Логи")

    elif command == "Настройки ⚙️":
        # Чтение файла настроек
        with open("settings.json") as f:
            settings = json.load(f)
        bot.send_message(message.from_user.id, f"<b>Настройки</b>\n\n"
                                               f"<b>Текущая модель для text2text</b>: <code>{settings['models']['current_model_1']}</code>\n" 
                                               f"<b>Текущая модель для img2text</b>: <code>{settings['models']['current_model_2']}</code>", 
                         reply_markup=markups.settings_markup(settings))

# Хэндлер всех сообщений
@user.on_message()
def message_handler(client, message):
    """Обработчик входящих сообщений."""
    if message.from_user is None:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    is_private = chat_id == user_id
    is_bot = message.from_user.is_bot
    is_self = message.from_user.is_self
    text = (message.text or message.caption or "").lower()
    with open("settings.json") as f:
        settings = json.load(f)
    if not is_self and is_private and not is_bot:
        # Сохраняем сообщение, если оно отправлено пользователем в личные сообщения
        message_store[message.id] = {
            "chat_id": chat_id,
            "text": text,
            "sender": message.from_user.first_name if message.from_user.username is None else f"@{message.from_user.username}"
        }

    elif is_self:
        # Обрабатываем собственные сообщения.

        # Извлекаю уникальные символы ИМЕННО в том порядке, что они в сообщении
        unique_chars = ""
        for i in text: unique_chars += i if i not in unique_chars else ""

        if ("ха" in unique_chars or "ах" in unique_chars) and len(unique_chars) <= 4 and settings['animation']['laughter']:
            # Эффект случайного выделения букв при смехе
            for _ in range(10):
                bigs = {randint(0, len(text) - 1) for _ in range(int(len(text) // 1.2))}
                new_text = "".join(f"**{char.upper()}**" if idx in bigs else char for idx, char in enumerate(text))
                edit_message(message, new_text)
                sleep(1)

        elif unique_chars in settings['animation']['animated_words']:
            # Эффект покачивания текста
            for _ in range(3):
                for up_pos in range(len(text)):
                    new_text = "".join(f"**{text[i].upper()}**" if i == up_pos else text[i] for i in range(len(text)))
                    edit_message(message, new_text)
                    sleep(0.7)

            # Чередование заглавных и строчных букв
            for _ in range(3):
                edit_message(message, f"**{text.upper()}**")
                sleep(0.7)
                edit_message(message, text.lower())
                sleep(0.7)

            # Возвращаем оригинальный текст
            edit_message(message, message.text or message.caption)



# Отлавливает удалённые сообщения
@user.on_deleted_messages()
def handle_deleted_messages(client, messages):
    """
    Перебирает удаленные сообщения, и если они сохранены в словаре, то бот скинет их в лс
    """
    with open("settings.json") as f:
        settings = json.load(f)

    for message in messages:
        if message and message.id in message_store and settings['send_deleted_messages']:
            deleted_message = message_store.pop(message.id)
            bot.send_message(user.get_me().id, f"<b>Удаленное сообщение</b>\n\n"
                                               f"<b>Чат</b>: <code>{deleted_message['chat_id']}</code>\n"
                                               f"<b>Юзер</b>: <code>{deleted_message['sender']}</code>\n"
                                               f"<b>Текст</b>: <pre>{deleted_message['text']}</pre>")


# Редактирует сообщение
def edit_message(message, new_text):
    """Функция редактирования текста или подписи к медиа."""
    try:
        if message.text != new_text:
            if message.media is None:
                user.edit_message_text(message.chat.id, message.id, new_text)
            else:
                user.edit_message_caption(message.chat.id, message.id, new_text)
    except FloodWait as e:
        sleep(e.x)



if __name__ == "__main__":
    # Запуск бота и информирование в консоли
    user.run(print("[i] Бот запущен"))
