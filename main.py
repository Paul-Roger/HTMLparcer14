# Telegram bot which can find all news on news.auto.ru for "keyword" since "date"
# Commands:
# /help - shows command list and description.
# /abort - stops current search
# /find <keyword> <yyyy-mm-dd>- search news containing <keyword>, in articles styarting from date for example /find BMW 2023-01-01
# 5980165046 #:# AAE_C4ZVVz # EEWWrImuTERmqQEQiv # CIHUQHQ

import ParserNewsAtoRu
import telebot
import shelve
import time
from datetime import date
from datetime import datetime
import threading
import os

#Constants
Token = ""
DefDateStr = "2023-02-01"
DefSearchStr = "Mercedes"
MaxUsers = 100 #max number of users registered
dbname = "shelve.db"

def request_list(bot, dbname):
    #check the list of request and start parser when any request is in list
    print("request List start")
    while True:
        with shelve.open(dbname) as storage:
            print(list(storage.keys()))
            if len(list(storage.keys())) > 0: #list is not empty, find the eldest
                print("if len()")
                with shelve.open(dbname) as storage:
                    print("with shelve")
                    eldest_key = ""
                    eldest_date = datetime.now()
                    print(eldest_date)
                    for req in storage.keys():
                        userreq = storage[req]
                        print(req, userreq)
                        str_date = userreq[2]
                        req_date = datetime.strptime(str_date, '%m-%d-%Y %H:%M:%S')
                        print(req_date, eldest_date )
                        if req_date < eldest_date:
                            eldest_date = userreq[2]
                            eldest_key = req
                    #request data from parser
                    userreq = storage[eldest_key]
                    parser_result = 0
                    #parser_result = ParserNewsAtoRu.parser(eldest_key, userreq[0], userreq[1])
                    print("Parser Call")
                    if parser_result > 0:
                        bot.send_message(eldest_key, f"Thes result of your search'{userreq[0]} {userreq[1]} see in the file")
                        file_name = eldest_key + ".csv"
                        with open(file_name, 'r', encoding='utf-8') as data:
                             bot.send_document(eldest_key, data)
                        #remove request from the list
                        del storage[eldest_key]
                        #delete file
                        file_name = str(eldest_key) + ".csv"
                        os.remove(file_name)
                    else:
                        bot.send_message(eldest_key, "Sorry, we were unable to find anything reflecting your search conditions")
                        del storage[eldest_key]
            else: #empty list
                time.sleep(10)
#request_list(bot) end

# def request_list end

req_list = []

#open storage (or create if not exist)
#list format: {<UserID>,[<Date>, <keyword>, <QueNo>] where data = yyyy-mm-dd, keyword = search string, QueNo = -1 (initial), or 0 - current active or 1...99 - number in queue
#storage = shelve.open(dbname)

#bot logic
bot = telebot.TeleBot(Token)

my_thread = threading.Thread(target=request_list, args=(bot, dbname), daemon=True)
my_thread.start()

@bot.message_handler(commands=['help'])
def register_user(message):
    bot.send_message(message.chat.id, "Bot can find articles about cars and send result as a csv file\n /help - this information\n /start - register user before start search\n /date yyyy-mm-dd - set start date for search\n /find <keyword> - start search for a keyword\n /abort - aborts currently running search\n /end - remove registered user from the list\n ")

@bot.message_handler(commands=['date'])
def set_date(message):
    bot.send_message(message.chat.id, "Your date has been set")

@bot.message_handler(commands=['find'])
def search_news(message):
    with shelve.open(dbname) as storage:
        #check if list is full
        if len(storage.keys())>=100:
            bot.reply_to(message, "Sorry, queue is already full. Try later.")
            print(">100")
            return()
        #check if this user has already had open request
        if str(message.chat.id) in storage:
            bot.reply_to(message, "Sorry, yor previous request is still in a queue")
            return()
        arg = message.text.split()[1:]
        if (len(arg) > 0 and len(arg[0]) < 3) or len(arg) == 0 :
            bot.reply_to(message, "Wrong keyword string")
            return()
        str_startdate = DefDateStr
        if len(arg) > 1:
            try:
                str_startdate = arg[1]
                startdate = date.fromisoformat(arg[1])
            except:
                print(f"неверный формат даты, выбрана {DefDateStr} по умолчанию")
                str_startdate = DefDateStr
        req_list.append(arg[0])
        req_list.append(str_startdate)
        str_time = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        print(str_time)
        req_list.append(str_time)
        storage[str(message.chat.id)] = req_list
        bot.send_message(message.chat.id,"Your search has been put in a queue. It can take from several minutes to several hours. You will get a file when it's ready")

@bot.message_handler(content_types=['text'])
def TextRespond(message):
    print(message)
    bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, "This Bot can find articles in newas.auto.ru. Please, use /help for details")

if __name__ == '__main__':
    bot.polling()

#storage.close()
