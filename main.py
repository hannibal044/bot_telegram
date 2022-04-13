# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from data import db_session # модули для работы с БД
from data.users import User

#главное меню
def start(update, context):
    db_sess = db_session.create_session()
    user_id, name = update["message"]["chat"]["id"], update["message"]["chat"]["first_name"]
    if str(user_id) not in [elem.user_id for elem in db_sess.query(User).all()]:
        user = User(); user.user_id = user_id; user.name = name; db_sess.add(user); db_sess.commit()
        update.message.reply_text("Привет, ты новый! Пока что ничего не сделано")
    else:
        update.message.reply_text(f'Что за люди! Привет, "{name}"')

#если пользователь пишет сообщения
def messages(update, context):
    update.message.reply_text("Я пока что не успел набрать в себя навыков. Надеюсь, что успею до 25.04.2022")


#запуск программы
def main():
    updater = Updater("5193422398:AAFde7LeP50xSgtzBE33QWD3ctg9nDSkth0", use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, messages, pass_user_data=True))
    dp.add_handler(CommandHandler("start", start, pass_user_data=True))

    
    updater.start_polling() # начало работы
    updater.idle() # прекращение работы


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()