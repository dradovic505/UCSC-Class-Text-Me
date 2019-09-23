from db import UserDB
from find_classes import Scraper
import schedule, time, threading

dbase = UserDB()
scraper = Scraper()

def access_bot(user):
    class_info = scraper.find_info(user['class'])
    # scraper.close_browser()
    #send class_info to user as a telegram message
    print(class_info)
    #class_info = [class_number, status, available_seats, wait_list_total]
    print('available seats: ' + str(class_info[2]))
    print('waitlist total: ' + str(class_info[3]))
    # return class_info

def run_threaded(job_func): #access_bot() is the job
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def send_messages():
    print('first here')
    for user in dbase.return_all_verified_data():
        print('first here and user: ')
        print(user)
        schedule.every(1).minutes.do(run_threaded, access_bot(user))
        print('second here and user: ')
        print(user)
    while True:
        print('doing anything? 1')
        schedule.run_pending()
        print('doing anything? 2')
        time.sleep(1)

send_messages()
