from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import RegexHandler, Filters, CommandHandler
import logging
import constants
import functions
import spreadsheet


def create_log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def set_updaters(dispatcher):
    # Старт
    start_handler = CommandHandler('start', functions.start)
    dispatcher.add_handler(start_handler)

    # Открыть меню
    menu_handler = RegexHandler("🔔Меню", functions.menu)
    dispatcher.add_handler(menu_handler)

    # Клик по Inline
    dispatcher.add_handler(CallbackQueryHandler(functions.inlines))


def update_food():
    constants.foods = spreadsheet.get_food()


    for key, value in constants.foods.items():
        types = []
        for eat in value:
            if eat["type"] not in types:
                types.append(eat["type"])
        constants.types.update({key: types})

def main():
    create_log()
    update_food()

    updater = Updater(token=constants.key)

    dispatcher = updater.dispatcher
    set_updaters(dispatcher)
    updater.start_polling()

if __name__ == '__main__':
    main()
