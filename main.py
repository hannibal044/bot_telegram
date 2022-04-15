# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters # импорт объектов
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler # импорт объектов
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove # импорт объектов

from data import db_session # модуль для работы с БД
from data.users import User # модель ORM (информация о новом пользователе -> объект класса User -> запись в БД)



class AboutUser: # создание класса, отслеживающего действия пользователя и хранящего его данные
    opportunities = ["Переводчик", "Геокодер", "Википоиск"]

    def __init__(self, user_id, username):
        self.user_id = user_id; self.username = username
        self.action = None # переменная для хранения действия пользователя
    


def start(update, context): # обработчик команды "start"
    db_sess = db_session.create_session() # подключение к БД
    user_id, name = update["message"]["chat"]["id"], update["message"]["chat"]["first_name"] # получение данных о пользователе
    if str(user_id) not in [elem.user_id for elem in db_sess.query(User).all()]: # если такого пользователя еще не было
        user = User(); user.user_id = user_id; user.name = name; db_sess.add(user); db_sess.commit() # то добавляем его
        massiv.append(AboutUser(user_id, name)) # добавление пользователя в массив
        update.message.reply_text("Здравствуйте, бот к вашим услугам. Я умею выполнять некоторые вещи",
                                  reply_markup=ReplyKeyboardMarkup([[elem] for elem in new_user.opportunities]))
    else:
        update.message.reply_text("Вам нужна помощь? Тогда вызовите эту команду: /help")

def help(update, context):
    user = [user for user in massiv if str(user.user_id) == str(update["message"]["chat"]["id"])][0] # определение по id кто вызвал команду
    update.message.reply_text(f'''Здравствуйте, "{user.username}"!
Общение с ботом выглядит примерно таким образом:
Пользователь выбирает какое-то действие и начинает на его тему общаться с ботом.
Для того чтобы выйти из темы, пользователь должен набрать слово "стоп". С остальным проблем возникнуть не должно''')

def messages(update, context): # обработчик сообщений без команд
    user = [user for user in massiv if str(user.user_id) == str(update["message"]["chat"]["id"])][0] # определение по id кто вызвал команду
    if user.action:# если пользователь что-то ввел и он уже в какой-то теме
        if update.message.text.lower() == "выйти": user.action = None; update.message.reply_text('Меню', reply_markup=ReplyKeyboardMarkup([[elem] for elem in user.opportunities])) # пользователь вышел из какой-либо темы
        elif user.action.lower() == "геокодер": geocoder(update, context)# пользователь в теме "геокодер"
    elif update.message.text in user.opportunities: user.action = update.message.text # пользователь не был ни в одной теме, и он выбрал ее

def geocoder(update, context):
    if context.user_data:
        pass
    update.message.reply_text('')

def main(): # основная функция
    updater = Updater("5193422398:AAFde7LeP50xSgtzBE33QWD3ctg9nDSkth0", use_context=True) # создание объекта, осуществляющего связь между ботом и пользрвателем

    dp = updater.dispatcher # полученные сообщения передаются в диспетчер, а он их обрабатывает через обработчиков(функций)

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, messages, pass_user_data=True)) # добавление обработчика сообщений без команд
    dp.add_handler(CommandHandler("start", start)) # добавление обработчика команды "start"
    dp.add_handler(CommandHandler("help", help)) # добавление обработчика команды "help"

    
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта


if __name__ == '__main__': # запуск программы
    db_session.global_init("db/blogs.db") # Создание БД, если еще не создана
    db_sess = db_session.create_session() # подключение к БД
    massiv = [AboutUser(user.user_id, user.name) for user in db_sess.query(User).all()] # массив с пользователями
    main() # запуск основной функции