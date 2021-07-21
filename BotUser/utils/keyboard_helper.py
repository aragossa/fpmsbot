from telebot import types

from utils import db_connector
from utils.logger import get_logger

log = get_logger("keyboardhelper")


def get_main_keyboard_female():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(db_connector.get_message_text_by_id(1))
    btn2 = types.KeyboardButton(db_connector.get_message_text_by_id(2))
    btn3 = types.KeyboardButton(db_connector.get_message_text_by_id(3))
    btn4 = types.KeyboardButton(db_connector.get_message_text_by_id(4))
    btn5 = types.KeyboardButton(db_connector.get_message_text_by_id(5))
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return keyboard


def get_main_keyboard_male():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(db_connector.get_message_text_by_id(1))
    btn2 = types.KeyboardButton(db_connector.get_message_text_by_id(3))
    btn3 = types.KeyboardButton(db_connector.get_message_text_by_id(5))
    keyboard.add(btn1, btn2, btn3)
    return keyboard


def get_gender_select_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Женщина', callback_data='gender_fem')
    btn2 = types.InlineKeyboardButton(text='Мужчина', callback_data='gender_mal')
    keyboard.add(btn1, btn2)
    return keyboard


def get_fpms_menu_keyboard_flag_on():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Опустить флаг', callback_data='fpms_flag')
    btn2 = types.InlineKeyboardButton(text='Рекомендации', callback_data='fpms_reco')
    keyboard.add(btn1, btn2)
    return keyboard


def get_fpms_menu_keyboard_flag_off():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Поднять флаг', callback_data='fpms_flag')
    btn2 = types.InlineKeyboardButton(text='Рекомендации', callback_data='fpms_reco')
    keyboard.add(btn1, btn2)
    return keyboard


def get_lists_menu_keyboard_female():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Кому отсылается уведомление', callback_data='list_out')
    btn2 = types.InlineKeyboardButton(text='От кого приходит уведомление', callback_data='list_inc')
    btn3 = types.InlineKeyboardButton(text='У кого поднят флаг', callback_data='list_flag')
    btn4 = types.InlineKeyboardButton(text='Синхронизация', callback_data='list_sync')
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard


def get_lists_menu_keyboard_male():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='От кого приходит уведомление', callback_data='list_inc')
    btn2 = types.InlineKeyboardButton(text='Добавить', callback_data='list_add')
    keyboard.add(btn1, btn2)
    return keyboard

def get_subscribres_keyboard(user_list):
    keyboard = types.InlineKeyboardMarkup()
    for user in user_list:
        btn1 = types.InlineKeyboardButton(text='-', callback_data=f'del_subscr_{user[0]}')
        btn2 = types.InlineKeyboardButton(text=f'{user[1]}', callback_data='null')
        keyboard.add(btn1, btn2)
    return keyboard