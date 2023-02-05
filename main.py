# Telegram bot which can find all news on news.auto.ru for "keyword" since "date"
# Commands:
# /help - shows command list and description.
# /abort - stops current search
# /find <keyword> <yyyy-mm-dd>- search news containing <keyword>, in articles styarting from date for example /find BMW 2023-01-01


#import ParserNewsAtoRu
import telebot
import shelve
from datetime import date
import threading

#Constants
Token = "5980165046:AAE_C4ZVVzEEWWrImuTERmqQEQivCIHUQHQ"
DefDateStr = "2023-01-01"
DefSearchStr = "Mercedes"
MaxUsers = 100 #max number of users registered
dbname = 'shelve.db'


#open storage (or create if not exist)
#list format: {<UserID>,[<Date>, <keyword>, <QueNo>] where data = yyyy-mm-dd, keyword = search string, QueNo = -1 (initial), or 0 - current active or 1...99 - number in queue
storage = shelve.open(dbname)
rows_num = len(storage.keys())

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['help'])
def register_user(message):
    bot.send_message(message.chat.id, "Bot can find articles about cars and send result as a csv file\n /help - this information\n /start - register user before start search\n /date yyyy-mm-dd - set start date for search\n /find <keyword> - start search for a keyword\n /abort - aborts currently running search\n /end - remove registered user from the list\n ")

@bot.message_handler(commands=['date'])
def set_date(message):
    bot.send_message(message.chat.id, "Your date has been set")

@bot.message_handler(commands=['find'])
def search_news(message):
    bot.send_message(message.chat.id, "Search has been started. It can take from several minutes to a couple of hours. You will get a file when it's ready")
    arg = message.text.split()[1:]
    if (len(arg) > 0 and len(arg[0]) < 3) or len(arg) == 0 :
        bot.reply_to(message, "Wrong keyword string")
        return()
    if len(arg) > 1:
        try:
            str_startdate = date.fromisoformat(arg[1])
        except:
            print("неверный формат даты, выбрана 2023-01-01 по умолчанию")
            date_str = '2023-01-01'
    my_thread = threading.Thread(target=parser, args=(arg[0],str_startdate))
    my_thread.start()

@bot.message_handler(content_types=['text'])
def TextRespond(message):
    print(message)
    bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, "This Bot can find articles in newas.auto.ru. Please, use /help for details")

if __name__ == '__main__':
    bot.polling()


