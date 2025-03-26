from openai import OpenAI
from pyrogram import Client
from telebot import TeleBot
from kandinsky import Text2ImageAPI
from configparser import ConfigParser
# Модуль для логирования
import logging

# Логирование и БЛА-БЛА-БЛА. Код скомуниздил с Хабра
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# Config
config = ConfigParser()
config.read("config.ini")
p_conf, bot_conf, or_conf, kand_conf, img_bb = config['pyrogram'], config['TeleBot'], config['OpenRouter'], config['Kandinsky'], config['imgBB']

# Messages
message_store = {}

# Api Telegram
user = Client(name=p_conf['name'],
             api_id=p_conf['api_id'],
             api_hash=p_conf['api_hash'],
             phone_number=p_conf['phone_number'])
bot = TeleBot(token=bot_conf['bot_token'], parse_mode="HTML")

# Client Gemini
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=or_conf['api_key'],
)

# Kandinsky
kandinsky_api = Text2ImageAPI('https://api-key.fusionbrain.ai/', kand_conf['api_key'], kand_conf['secret_key'])
