# t.me/ClassTextBot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, yaml, telegram
from db import UserDB

dbase = UserDB()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update,context):
    context.bot.send_message(chat_id=update.message.chat_id,
    text="Hi! A list of commands: \n /verifyMe (you must do this one)     \
    \n /stopNotifs (I will stop sending you messages about your classes)  \
    \n /restartNotifs (I will send you messages about your classes again) \
    \n /deleteMyData (All your data will be deleted)")

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='You need to type a command! (Like /verifyNumber and /getUpdate)')

def verifyMe(update, context):
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share contact', request_contact=True)]])
    context.bot.sendMessage(chat_id=update.message.chat_id, text='please share your contact so I can verify you with my database: ', reply_markup=reply_markup)

def contact(update, context):
    phone_number = update.message.contact.phone_number
    user_id = update.message.contact.user_id
    dbase.add_user_id(phone_number, user_id)

def class_full(update, context):
    full = ('{} is full!'.format(class_name))
    context.bot.send_message(chat_id=update.message.chat_id, text=full)

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't know that command")

def main():
    my_token = yaml.safe_load(open('db.yaml'))
    updater = Updater(token=my_token['my_telegram_token'], use_context=True)
    dispatcher = updater.dispatcher
    

    #handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    verifyNumber_handler = CommandHandler('verifyMe', verifyMe)
    dispatcher.add_handler(verifyNumber_handler)

    begin_handler = CommandHandler('begin', begin)
    dispatcher.add_handler(begin_handler)

    contact_handler = MessageHandler(Filters.contact, contact)
    dispatcher.add_handler(contact_handler)

    class_full_handler = MessageHandler(Filters.text,class_full)
    dispatcher.add_handler(class_full_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    echo_handler = MessageHandler(Filters.text,echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


    #block until ctrl-c pressed
    updater.idle()


if __name__ == '__main__':
    main()