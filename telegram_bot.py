# t.me/ClassTextBot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging, yaml, telegram
from db import UserDB

dbase = UserDB()

# class TelegramBot():

my_token = yaml.safe_load(open('db.yaml'))
updater = Updater(token=my_token['my_telegram_token'], use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# def __init__(self):
#     self.my_token = yaml.safe_load(open('db.yaml'))
#     self.updater = Updater(token=self.my_token['my_telegram_token'], use_context=True)
#     self.dispatcher = self.updater.dispatcher
#     logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update,context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi! A list of commands: \n /verifyMe (you must do this one) \n /stopNotifs (I will stop sending you messages about your classes) \n /restartNotifs (I will send you messages about your classes again) \n /deleteMyData (All your data will be deleted)")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

# def start_func():
#     # start(update,context)
#     start_handler = CommandHandler('start', start)
#     dispatcher.add_handler(start_handler)
#     updater.start_polling()

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='You need to type a command! (Like /verifyNumber and /getUpdate)')

echo_handler = MessageHandler(Filters.text,echo)
dispatcher.add_handler(echo_handler)


# def echo_func():
#     # start(update,context)
#     echo_handler = MessageHandler(Filters.text,echo)
#     dispatcher.add_handler(echo_handler)


def verifyMe(update, context):
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share contact', request_contact=True)]])
    context.bot.sendMessage(chat_id=update.message.chat_id, text='please share your contact so I can verify you with my database: ', reply_markup=reply_markup)

verifyNumber_handler = CommandHandler('verifyMe', verifyMe)
dispatcher.add_handler(verifyNumber_handler)

# def verifyMe_func():
#     # verifyMe(update,context)
#     verifyNumber_handler = CommandHandler('verifyMe', verifyMe)
#     dispatcher.add_handler(verifyNumber_handler)

def contact(update, context):
    phone_number = update.message.contact.phone_number
    # print(phone_number)
    user_id = update.message.contact.user_id
    # print(user_id)
    dbase.print_db()
    dbase.add_user_id(phone_number, user_id)
    dbase.print_db()

contact_handler = MessageHandler(Filters.contact, contact)
dispatcher.add_handler(contact_handler)

# def contact_func():
#     contact(update, context)
#     dispatcher.add_handler(MessageHandler(Filters.contact, contact))

def class_full(update, context):
    full = ('{} is full!'.format(class_name))
    context.bot.send_message(chat_id=update.message.chat_id,
    text=full)

class_full_handler = MessageHandler(Filters.text,echo)
dispatcher.add_handler(class_full_handler)

# def class_full_func():
#     # class_full(update, context)
#     class_full_handler = MessageHandler(Filters.text,echo)
#     dispatcher.add_handler(class_full_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't know that command")

# def unknown_func():
#     unknown_handler = MessageHandler(Filters.command, unknown)
#     dispatcher.add_handler(unknown_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
