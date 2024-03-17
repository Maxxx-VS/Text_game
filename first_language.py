import telebot, json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

chatid = {}
TOKEN = "6547363557:AAGANK3kV2ywllU3LAAXzO7AxIUrtiHj0G0"
bot = telebot.TeleBot(token=TOKEN)

with open("../Text_game/first_language.json", "r", encoding='utf-8') as f:
    data = json.load(f)

@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, text="Добро пожаловать в пиложение по выбору своего первого языка программирования!\n"
                                           "Вам предстоит отвтить на вопросы, а также сделать очень тяжёлый выбор...\n"
                                           "по команде /help.")

@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, text="Чтобы начать игру введите команду /letsgo.\n"
                                           "Чтобы выбирать действия, вам будут представлены кнопки с выбором.\n"
                                           "Думайте перед тем, как делать выбор, потому что от этого зависит конечный результат.\n"
                                           "В приложении есть 13 концовок.\n"
                                           "Удачи :)")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: telebot.types.CallbackQuery):
    print(f"{chatid[call.message.chat.id][1]}: {call.message.message_id}")
    if chatid[call.message.chat.id][1] != call.message.message_id:
        bot.answer_callback_query(call.id, "Вы уже выбрали!")
    for k, v in chatid[call.message.chat.id][0].items():
        print(f"{k}:{v}:{call.data}")
        if call.data == v:
            if "options" in data[v]:
                message = send_question(data[v]["description"], data[v]["options"], data[v]["photos"],
                                        call.message.chat.id)
                chatid[message.chat.id][1] = message.message_id
                chatid[message.chat.id][0] = data[v]["options"]
            else:
                bot.send_message(chat_id=call.message.chat.id, text=data[v]["description"])
                bot.send_message(chat_id=call.message.chat.id, text="Хотите попробовать ещё раз. /letsgo")

def send_question(description: str, options: dict, photos: dict, id: int):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for k, v in options.items():
        markup.add(InlineKeyboardButton(k, callback_data=v))
    if len(photos) == 0:
        message = bot.send_message(chat_id=id, text=description, reply_markup=markup)
        return message
    if len(photos) == 1:
        value = tuple(photos.values())
        with open("photos/" + value[0], "rb") as f:
            message = bot.send_photo(chat_id=id, photo=f, caption=description, reply_markup=markup)
            return message
    else:
        photo_list = []
        for k, v in photos.items():
            photo_list.append(telebot.types.InputMediaPhoto(open("photos/" + v, "rb")))
        bot.send_media_group(chat_id=id, media=photo_list)
        message = bot.send_message(chat_id=id, text=description, reply_markup=markup)
        return message

@bot.message_handler(commands=["letsgo"])
def letsgo(msg):
    message = send_question(data["start"]["description"], data["start"]["options"], data["start"]["photos"],
                            msg.chat.id)
    chatid[message.chat.id] = [data["start"]["options"], message.message_id]

bot.polling()
