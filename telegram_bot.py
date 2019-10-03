# t.me/ClassTextBot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, yaml, telegram
from find_classes import Scraper
from db import UserDB

dbase = UserDB()
scraper = Scraper()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update,context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Hi! Please type /verifyMe to start')

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='You need to type a command! (Like /verifyNumber and /getUpdate)')

def verifyMe(update, context):
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share contact', request_contact=True)]])
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Please share your contact so I can verify you with my database: ', reply_markup=reply_markup)

def contact(update, context):
    phone_number = update.message.contact.phone_number
    user_id = update.message.contact.user_id
    dbase.add_user_id(phone_number, user_id)
    print('contact:')
    print(user_id)
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Thanks, you\'re verified! Now type /begin to start getting class updates.')

def check_class(context):
    job = context.job

    #job.context is the user id
    print('working for user: ' + str(job.context))
    user = dbase.get_user(job.context)

    class_info = scraper.find_info(user['class'])
    class_name = class_info[0]
    available_seats = class_info[1]
    if available_seats <= 0:
        context.bot.send_message(job.context, text='{0} is now full!'.format(class_name))
    else:
        context.bot.send_message(job.context, text='{0} has an open spot!'.format(class_name))

def begin(update, context):
    chat_id = update.message.chat_id
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    new_job = context.job_queue.run_repeating(check_class, 9, context=chat_id) #900 sec = 15 min
    context.chat_data['job'] = new_job

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

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    echo_handler = MessageHandler(Filters.text,echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


    #block until ctrl-c pressed
    updater.idle()


if __name__ == '__main__':
    main()