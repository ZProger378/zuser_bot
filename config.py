from pyrogram import Client
from telebot import TeleBot
from configparser import ConfigParser
from huggingface_hub import InferenceClient
import monsterapi as monster


# Config
config = ConfigParser()
config.read("config.ini")
p_conf, bot_conf, hf_conf, m_conf, img_bb = config['pyrogram'], config['TeleBot'], config['HuggingFace'], config['MosterAPI'], config['imgBB']

# Messages
message_store = {}

# Api Telegram
user = Client(name=p_conf['name'],
             api_id=p_conf['api_id'],
             api_hash=p_conf['api_hash'],
             phone_number=p_conf['phone_number'])
bot = TeleBot(token=bot_conf['bot_token'], parse_mode="HTML")

# Переехал на HuggingFace
client = InferenceClient(
    provider=hf_conf['provider'],
    api_key=hf_conf['api_key'],
)

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=or_conf['api_key'],
# )

# Переехал с Кандинского на МонстерАПИ
monster_client = monster.client(m_conf['api_key'])

# Kandinsky
# kandinsky_api = Text2ImageAPI('https://api-key.fusionbrain.ai/', kand_conf['api_key'], kand_conf['secret_key'])
