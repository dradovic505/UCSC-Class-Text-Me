from db import UserDB
from find_classes import Scraper
from telegram_bot import TelegramBot
import schedule, time, threading
from telegram_bot import dispatcher

dbase = UserDB()
scraper = Scraper()
bot = TelegramBot()

def access_bot(user):
    class_info = scraper.find_info(user['class'])
    available_seats = class_info[2]
    wait_list_total = class_info[3]
    if available_seats <= 0:
        bot.class_full()

def run_threaded(job_func): #access_bot() is the job
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def send_messages():
    for user in dbase.return_all_verified_data():
        schedule.every(1).minutes.do(run_threaded, access_bot(user))
    while True:
        schedule.run_pending()
        time.sleep(1)

send_messages()
