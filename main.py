#pytelegrambotapi
import telebot
from telebot import types

#database
from connection import *

#config file
import config

create_db_new()

from buttons import *

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome_message(message):
    if message.chat.type == "private":
        #copier = bot.copy_message(message.chat.id,message.chat.id,message.message_id)
        check_step1 = database_query_fetchall(f"SELECT step FROM users WHERE user_id = '{message.chat.id}'")
        print(check_step1)
        if str(check_step1) != "None":
            #print("there is something")
            bot.send_message(message.chat.id, "Вы уже в разговоре!",reply_markup=cancel_talk_user)
        else:
            bot.send_message(message.chat.id, "Привет! Выберите что-то из меню.",reply_markup=markup1)
            check_user_in_db = database_query(f"SELECT step FROM users WHERE user_id = '{message.chat.id}'")
            if str(check_user_in_db) == "[]":
                database_query(f"INSERT INTO users VALUES('{message.from_user.id}','{message.from_user.first_name}','menu')")
            else:
                database_query(f"UPDATE users SET step = 'menu' WHERE user_id = '{message.chat.id}'")
        
@bot.message_handler(content_types=['text'])
def text_msg(message):
    if message.chat.type == "private":
        check_step = database_query(f"SELECT step FROM users WHERE user_id = '{message.chat.id}'")
        for i in check_step:
            if  i[0] == "menu":
                if message.text == "Вопрос Оператору":
                    bot.send_message(message.chat.id, "Подтвердите, что хотите связаться с оператором👇👇👇",reply_markup=confirm)
        check_operator = database_query(f"SELECT operator_id FROM operators WHERE user_id = '{message.chat.id}'")
        #print(str(check_operator))
        if str(check_operator) == "[]":
            check_user = database_query(f"SELECT user_id FROM operators WHERE operator_id = '{message.chat.id}'")
            #print("user" + str(check_user))
            if str(check_user) != "[]":
                try:
                    print(check_user)
                    bot.copy_message(check_user[0][0],message.chat.id,message.message_id)
                    bot.send_message(message.chat.id, "📨Письмо отправлено.",reply_markup=cancel_talk)
                except:
                    database_query(f"DELETE FROM operators WHERE operator_id = '{message.from_user.id}'")
                    print("error")
                    bot.send_message(message.chat.id, "Ошибка. Разговор отменен")
        else:
            print("else is working")
            bot.copy_message(check_operator[0][0],message.chat.id,message.message_id)
            bot.send_message(message.chat.id, "📨Письмо отправлено.",reply_markup=cancel_talk_user)
@bot.message_handler(content_types=['photo','sticker','video','audio','voice','location','animation','contact','document','dice','poll'])
def content_msgs(message):
    check_operator1 = database_query(f"SELECT operator_id FROM operators WHERE user_id = '{message.chat.id}'")
    print(str(check_operator1))
    if str(check_operator1) == "[]":
        check_user1 = database_query(f"SELECT user_id FROM operators WHERE operator_id = '{message.chat.id}'")
        print("user" + str(check_user1))
        if str(check_user1) != "[]":
            try:
                print(check_user1)
                bot.copy_message(check_user1[0][0],message.chat.id,message.message_id)
                bot.send_message(message.chat.id, "📨Письмо отправлено.",reply_markup=cancel_talk)
            except:
                database_query(f"DELETE FROM operators WHERE user_id = '{message.from_user.id}'")
                print("error")
                bot.send_message(message.chat.id, "Ошибка. Разговор отменен")
    else:
        print("else is working")
        bot.copy_message(check_operator1[0][0],message.chat.id,message.message_id)
        bot.send_message(message.chat.id, "📨Письмо отправлено.",reply_markup=cancel_talk_user)
@bot.callback_query_handler(func = lambda call: True)
def callback_Data_handler(call):
    if call.data == "confirm":
        database_query(f"UPDATE users SET step = 'seek' WHERE user_id = '{call.from_user.id}'")
        bot.send_message(config.admin_group, f"#{call.message.chat.id}\nНовый Юзер хочет поговорить с вами\n\nИмя: {call.from_user.first_name}",reply_markup=get_new)

        bot.send_message(call.message.chat.id, "Ждите нового оператора")
    elif call.data == "get_new_user":
        check_is_farted = database_query(f"SELECT user_id FROM operators WHERE operator_id = '{call.from_user.id}'")
        print(str(check_is_farted))
        if str(check_is_farted) == "[]":
            try:
                #print(call.message.text.split()[0][1:])
                database_query(f"INSERT INTO operators VALUES('{call.from_user.id}','{call.message.text.split()[0][1:]}')")
                bot.send_message(call.message.chat.id, F"Сообщение отправлено в ЛС")
                bot.send_message(call.from_user.id, F"Напишите что-нибудь и бот отправит это юзеру")
                bot.send_message(call.message.text.split()[0][1:],"С вами связался оператор. Напишите что нибудь")
                bot.edit_message_text(chat_id=call.message.chat.id, text=call.message.text + f"\n✅Уже взяли\n\nИнформация об операторе:\nИмя: {call.from_user.first_name}\nID: {call.from_user.id}\nUsername: {call.from_user.username}",message_id=call.message.message_id,reply_markup=None)
                database_query(f"UPDATE users SET step = 'menu' WHERE user_id = '{call.message.text.split()[0][1:]}'")
            except Exception as e:
                print(str(e))
        else:
            bot.send_message(call.message.chat.id, "У вас уже есть разговор!",reply_markup=cancel_talk)
    elif call.data == "cancel_talk":
        check_talking = database_query(f"SELECT user_id FROM operators WHERE operator_id = '{call.from_user.id}'")
        if str(check_talking) != "[]":
            bot.send_message(call.message.chat.id, "Вы уверены что хотите остановить этот разговор?",reply_markup=cancel_talk_confirm)
    elif call.data == "cancel_talk_user":
        check_talking = database_query(f"SELECT operator_id FROM operators WHERE user_id = '{call.from_user.id}'")
        if str(check_talking) != "[]":
            bot.send_message(call.message.chat.id, "Вы уверены что хотите остановить этот разговор?",reply_markup=cancel_talk_confirm_user)
    elif call.data == "cancel_talk_confirm":
        check_talking = database_query(f"SELECT user_id FROM operators WHERE operator_id = '{call.from_user.id}'")
        
        if str(check_talking) != "[]":
            get_user_talking = database_query(f"SELECT user_id FROM operators WHERE operator_id = '{call.from_user.id}'")
            #print(get_user_talking)
            bot.send_message(get_user_talking[0][0],"Разговор был отменен оператором. Если хотите опять связаться, напишите старт")
            database_query(f"DELETE FROM operators WHERE operator_id = '{call.from_user.id}'")

            bot.edit_message_text(text='☑️Вы разорвали связь',chat_id=call.message.chat.id,message_id=call.message.message_id)
    elif call.data == "cancel_talk_confirm_user":
        check_talking = database_query(f"SELECT operator_id FROM operators WHERE user_id = '{call.from_user.id}'")
        if str(check_talking) != "[]":
            get_user_talking = database_query(f"SELECT operator_id FROM operators WHERE user_id = '{call.from_user.id}'")
            #print(get_user_talking)
            for i in get_user_talking:
                bot.send_message(get_user_talking[0][0],"Разговор был отменен юзером.")
                database_query(f"DELETE FROM operators WHERE user_id = '{call.from_user.id}'")
                bot.send_message(call.message.chat.id, "Вы успешно отменили разговор с оператором")
    

    

bot.polling()