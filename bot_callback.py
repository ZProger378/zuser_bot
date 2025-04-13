from config import bot
import markups
import json

print("[i] Панель управления ботом запущена")


@bot.callback_query_handler(lambda call: True)
def callback(call):
    data = call.data
    message = call.message
    with open("settings.json") as f:
        settings = json.load(f)
    animated_words = settings['animation']['animated_words'] 
    if data == "settings_laughter":
        settings['animation']['laughter'] = not settings['animation']['laughter']
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"<b>Настройки</b>\n\n"
                                   f"<b>Текущая модель для text2text</b>: <code>{settings['models']['current_model_1']}</code>\n" 
                                   f"<b>Текущая модель для img2text</b>: <code>{settings['models']['current_model_2']}</code>", 
        reply_markup=markups.settings_markup(settings))

    elif data == "animated_words":
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text="<b>Анимированные слова</b>\n\n"
                                   f"{'\n'.join([f'<b>{x+1})</b> <code>{i}</code>' for x, i in enumerate(animated_words)])}",
                              reply_markup=markups.words_markup())

    elif data == "add_words":
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"Отправь <i>слово</i>, которое <b>нужно добавить</b>",
                              reply_markup=markups.to_settings_markup())
        bot.register_next_step_handler(message, add_word)

    elif data == "delete_words":
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"Выберите <i>слова</i>, которые <b>хотите удалить</b>",
                              reply_markup=markups.delete_words_markup(animated_words))
    elif data.startswith("delete_"):
        word = data.split("_")[-1]
        settings['animation']['animated_words'].remove(word)
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"<b>Слово удалено</b> ✅",
                              reply_markup=markups.to_settings_markup())
    elif data.startswith("edit_model_"):
        model = f"current_model_{data.split('_')[-1]}"
        models = settings['models']
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"Выберите <b>модель</b>",
                              reply_markup=markups.edit_model_markup(models, model))
    elif data.startswith("current_model_"):
        model = f"current_model_{data.split('_')[-2]}"
        selected_model = data.split("_")[-1]
        settings['models'][model] = selected_model
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        models = settings['models']
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"Выберите <b>модель</b>",
                              reply_markup=markups.edit_model_markup(models, model))

    elif data == "settings":
        bot.clear_step_handler(message)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=f"<b>Настройки</b>\n\n"
                                   f"<b>Текущая модель для text2text</b>: <code>{settings['models']['current_model_1']}</code>\n" 
                                   f"<b>Текущая модель для img2text</b>: <code>{settings['models']['current_model_2']}</code>", 
        reply_markup=markups.settings_markup(settings))


def add_word(message):
    word = message.text
    with open("settings.json") as f:
        settings = json.load(f)
    settings['animation']['animated_words'].append(word)
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, f"<b>Слово добавлено</b> ✅",
                     reply_markup=markups.to_settings_markup())

bot.polling(none_stop=True, interval=0)

