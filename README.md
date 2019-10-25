# UCSC-Class-Text-Me

NOTE: to run this yourself you need to install flask, yaml, selenium, python-telegram-bot, and pymongo.
You will also need your own yaml file with your database name and your telegram bot token (if you made your own to replicate functionality)

  This program allows a user to access a web app (local host for now) and enter their information and a class they wish to be notified for. Then, the user can go to Telegram and search for ClassTextBot and begin a conversation with the bot. When the class status changes (was open and now closed or vice versa), the user will get a Telegram message from the bot!

To run this program, simply run:

    python3 app.py

to activate the web app, and 

    python3 telegram_bot.py

to activate the telegram bot.
