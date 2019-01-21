from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import constants


def start(bot, update):
    custom_keyboard = [["🔔Меню", "✉Связаться с нами"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

    text = 'Приятно познакомиться,\n{name}!\nЧто бы ты хотел заказать?'.format(name=update['message']['chat']['first_name'])

    update.message.reply_text(text=text,
                              reply_markup=reply_markup)


def menu(bot, update):
    custom_keyboard = []
    a = []
    for item in constants.foods.keys():
        a.append(InlineKeyboardButton(item, callback_data=item))
        if len(a) == 2:
            custom_keyboard.append(a.copy())
            a.clear()
    if a:
        custom_keyboard.append(a.copy())
    custom_keyboard.append([InlineKeyboardButton("Вместе дешевле", callback_data="discounts")])
    reply_markup = InlineKeyboardMarkup(custom_keyboard, resize_keyboard=True)


    text = "🔔Наше меню"
    update.message.reply_text(text=text,
                              reply_markup=reply_markup)


def show_categories(category, bot, query):
    categories = constants.types[category]
    custom_keyboard = []
    for cat in categories:
        custom_keyboard.append([InlineKeyboardButton(cat, callback_data=category + "::" + cat)])
    custom_keyboard.append([InlineKeyboardButton("Назад", callback_data="prev")])
    reply_markup = InlineKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    text = "Выбери категорию"

    bot.edit_message_text(text=text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)

def get_food(cat, type):
    data =  constants.foods[cat]
    result = []
    for eat in data:
        if eat["type"] == type:
            result.append(eat)
    return result

def send_food(food, bot, update):
    print(food)
    name = food["name\n"]
    url = food["photo\n"]
    describe = food["descrption\n"]

    bot.send_photo(caption=name,
                   chat_id=update.callback_query.message.chat_id,
                   photo = url)

def show_eat(cat, typ , bot, update):
    bot.edit_message_text(text=typ+":",
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id)
    foods = get_food(cat, typ)
    for food in foods:
        send_food(food, bot, update)



def inlines(bot, update):
    data = update['callback_query']['data']
    if data in constants.types.keys():
        show_categories(data, bot, update.callback_query)
    elif "::" in data:
        cat, typ = data.split("::")
        show_eat(cat, typ, bot, update)
