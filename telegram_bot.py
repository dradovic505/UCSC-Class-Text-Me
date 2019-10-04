# t.me/ClassTextBot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, yaml, telegram
from find_classes import Scraper
from db import UserDB

dbase = UserDB()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update,context):
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share contact', request_contact=True)]])
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Please share your contact so I can verify you with my database: ', 
                            reply_markup=reply_markup)

def contact(update, context):
    phone_number = update.message.contact.phone_number
    user_id = update.message.contact.user_id
    dbase.add_user_id(phone_number, user_id)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text='Thanks, you\'re verified! Now type /begin to start getting class updates.')

def check_classes(context):
    job = context.job
    scraper = Scraper()
    #job.context is the user id
    user = dbase.get_user(job.context)
    class_list = user['class_list']

    for c in class_list:
        class_info = scraper.find_info(c['class_name'])
        available_seats = class_info[1]
        if available_seats <= 0 and c['previously_open']:
            dbase.set_availability(job.context, c['class_name'], False)
            context.bot.send_message(job.context, text='{0} is now full!'.format(c['class_name']))
        elif available_seats > 0 and not c['previously_open']:
            dbase.set_availability(job.context, c['class_name'], True)
            context.bot.send_message(job.context, text='{0} has an open spot!'.format(c['class_name']))
    scraper.close_browser()

def begin(update, context):
    chat_id = update.message.chat_id
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    new_job = context.job_queue.run_repeating(check_classes, 900, context=chat_id) #900 sec = 15 min
    context.chat_data['job'] = new_job

def end(update, context):
    if 'job' not in context.chat_data:
        update.message.reply_text('You don\'t have any messaging processes to end! To start one, type /begin')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Thanks, you\'ll stop receiving messages from me now!')

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't know that command")

def main():
    my_token = yaml.safe_load(open('db.yaml'))
    updater = Updater(token=my_token['my_telegram_token'], use_context=True)
    dispatcher = updater.dispatcher
    
    #handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    begin_handler = CommandHandler('begin', begin, pass_args=True, pass_job_queue=True, pass_chat_data=True)
    dispatcher.add_handler(begin_handler)

    end_handler = CommandHandler('end', end, pass_chat_data=True)
    dispatcher.add_handler(end_handler)

    contact_handler = MessageHandler(Filters.contact, contact)
    dispatcher.add_handler(contact_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

    #block until ctrl-c pressed
    updater.idle()


if __name__ == '__main__':
    main()