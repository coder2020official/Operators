from telebot import types

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup1.add("FAQ","Вопрос Оператору")

confirm = types.InlineKeyboardMarkup()
confirm.add(types.InlineKeyboardButton('Подтвердить',callback_data="confirm"))

get_new = types.InlineKeyboardMarkup()
get_new.add(types.InlineKeyboardButton('Ответить',callback_data='get_new_user'))

cancel_talk = types.InlineKeyboardMarkup()
cancel_talk.add(types.InlineKeyboardButton('Отменить разговор',callback_data='cancel_talk'))

cancel_talk_confirm = types.InlineKeyboardMarkup()
cancel_talk_confirm.add(types.InlineKeyboardButton('Отменить разговор',callback_data='cancel_talk_confirm'),types.InlineKeyboardButton('🔙Назад',callback_data='back_menu'))

cancel_talk_user = types.InlineKeyboardMarkup()
cancel_talk_user.add(types.InlineKeyboardButton('Отменить разговор',callback_data='cancel_talk_user'))

cancel_talk_confirm_user = types.InlineKeyboardMarkup()
cancel_talk_confirm_user.add(types.InlineKeyboardButton('Отменить разговор',callback_data='cancel_talk_confirm_user'),types.InlineKeyboardButton('🔙Назад',callback_data='back_menu_user'))

