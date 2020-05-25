import os
import telebot
from flask import Flask, request
# Initial variables
token = os.environ.get('token')  # Bot`s token
url = os.environ.get('url')  # Heroku app url
private_chat = os.environ.get('private')  # Private chat ID of main person :)
public_chat = os.environ.get('public')  # Public chat ID
# Create bot and Flask app
bot = telebot.TeleBot(token)
server = Flask(__name__)
# Keyboard for user
choose_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
choose_key.add("👥 В чат", "👤 В ЛС")


@bot.message_handler(commands=['start'])
def start_com(message):
    bot.send_message(message.chat.id, f"✌🏻 Здравствуйте {message.from_user.first_name}!\n\n"
                                      f"📨 Я являюсь средством для анонимной передачи отзывов о внутренних процессах происходящих в компании <b>GrandTechGroup</b>\n\n"
                                      f"🔰<b> Несколько советов для анонимизации:\n"
                                      f" - Отпрвьте ваше сообщения одним сообщениям\n"
                                      f" - Не пишите информацию о себе\n"
                                      f" - Используйте другой стиль общения\n"
                                      f" - В лучшем случае используете Google Translate, чтобы вас нельзя было вычеслить!</b>\n\n"
                                      f"<i>⁉️ Помните что этот бот никак не хранит и обратывает инфомацию о вас, и не передает информацию третьим лицам!</i>\n\n"
                                      f"✳️ Выберите куда вы хотите отправить ваше сообщения:",
                     parse_mode="html", reply_markup=choose_key)


@bot.message_handler(func=lambda message: message.text == "👥 В чат")
@bot.message_handler(commands=['public'])
def public_com(message):
    bot.send_message(message.chat.id, "📬 Отправьте ваше сообщения чтобы опубликовать его в публичный чат: ")
    bot.register_next_step_handler(message, public_send)


@bot.message_handler(func=lambda message: message.text == "👤 В ЛС")
@bot.message_handler(commands=['private'])
def private_com(message):
    bot.send_message(message.chat.id, "📬 Отправьте ваше сообщения чтобы отправить его Директору: ")
    bot.register_next_step_handler(message, private_send)


@bot.message_handler(commands=['check'])
def check_com(message):
    bot.send_message(message.chat.id, "🤖 Система активная и находиться в штатном режиме!")


def private_send(message):
    try:
        if message.photo is not None:
            bot.send_photo(private_chat, photo=message.photo[2].file_id)
        elif message.video is not None:
            bot.send_video(private_chat, data=message.video.file_id)
        elif message.video_note is not None:
            bot.send_video_note(private_chat, data=message.video_note.file_id)
        elif message.document is not None:
            bot.send_document(private_chat, data=message.document.file_id)
        else:
            bot.send_message(private_chat, message.text)

        bot.send_message(message.chat.id, "✅ Ваше сообщения успешно доставлено!")
    except Exception as PrivateSendError:
        bot.send_message(message.chat.id, "😵 Упс...\n"
                                          "🚧 Ватсон у нас ошибка!\n"
                                          "⛔️ Ошибка при обработке вашего запроса! Попробуйте позже или обратитесь к саппорту: @myservebot")
        print(f"[!] PrivateSendError: {PrivateSendError}")


def public_send(message):
    try:
        if message.photo is not None:
            bot.send_photo(public_chat, photo=message.photo[2].file_id)
        elif message.video is not None:
            bot.send_video(public_chat, data=message.video.file_id)
        elif message.video_note is not None:
            bot.send_video_note(public_chat, data=message.video_note.file_id)
        elif message.document is not None:
            bot.send_document(public_chat, data=message.document.file_id)
        else:
            bot.send_message(public_chat, message.text)

        bot.send_message(message.chat.id, "✅ Ваше сообщения успешно доставлено!")
    except Exception as PublicSendError:
        bot.send_message(message.chat.id, "😵 Упс...\n"
                                          "🚧 Ватсон у нас ошибка!\n"
                                          "⛔️ Ошибка при обработке вашего запроса! Попробуйте позже или обратитесь к саппорту: @myservebot")
        print(f"[!] PublicSendError: {PublicSendError}")


@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=url + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    # bot.polling(none_stop=True)
