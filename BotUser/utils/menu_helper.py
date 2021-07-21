from BotUser.utils.keyboard_helper import get_gender_select_keyboard

from utils.db_connector import get_message_text_by_id
from utils.logger import get_logger
from BotUser.bot_user import Botuser

log = get_logger("menu_helper")


def add_user(bot, message):
    user = Botuser(message.chat.id)

    if user.check_auth():
        log.info("auth checked")
        keyboard = user.get_user_main_menu_keyboard()
        message_text = get_message_text_by_id(17)
        bot.send_message(user.uid, message_text, reply_markup=keyboard)

    else:
        log.info("auth not checked")
        keyboard = get_gender_select_keyboard()
        message_text = get_message_text_by_id(18)
        bot.send_message(user.uid, message_text, reply_markup=keyboard)


def text_message_handle(bot, message):
    user = Botuser(message.chat.id)

    if message.text == get_message_text_by_id(1):
        log.info("lists menu")
        keyboard = user.get_lists_menu_keyboard()
        message_text = get_message_text_by_id(24)
        bot.send_message(user.uid, message_text, reply_markup=keyboard)


    elif message.text == get_message_text_by_id(2) and user.gender == "FEMALE":
        log.info("fpms menu")
        keyboard = user.get_fpms_menu_keyboard()
        message_text = get_message_text_by_id(20)
        bot.send_message(user.uid, message_text, reply_markup=keyboard)

    elif message.text == get_message_text_by_id(3):
        """ меню настройка """
        pass

    elif message.text == get_message_text_by_id(4) and user.gender == "FEMALE":
        """ меню регулярные действия """
        pass

    elif message.text == get_message_text_by_id(5):
        """ меню лента по умолчанию """
        pass

    elif user.check_user_state_input():
        pass


def select_gender(bot, call):
    user = Botuser(call.message.chat.id)
    data = call.data[7:]
    first_name = call.from_user.first_name
    last_name = call.from_user.last_name
    username = call.from_user.username
    user.add_user(gender=data, first_name=first_name, last_name=last_name, username=username)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=get_message_text_by_id(19))
    user = Botuser(call.message.chat.id)
    keyboard = user.get_user_main_menu_keyboard()
    message_text = get_message_text_by_id(17)
    bot.send_message(user.uid, message_text, reply_markup=keyboard)


def change_flag_state(bot, call):
    user = Botuser(call.message.chat.id)
    data = call.data[5:]
    if data == 'flag':
        if user.get_user_flag_state():
            "уведомление подписчикам об прекращении флага"
        else:
            "выбор даты для окончания флага"

        user.change_user_flag_state()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=get_message_text_by_id(19))
    elif data == 'reco':
        pass


def follow_user(bot, message, key):
    user = Botuser(message.chat.id)
    if user.check_subscription(publisher_id=key):
        message_text = get_message_text_by_id(21)
        bot.send_message(user.uid, message_text)
    else:
        subscription_result = user.add_subscription(publisher_id=key)
        if subscription_result:
            message_text = get_message_text_by_id(22)
            bot.send_message(user.uid, message_text)
        else:
            message_text = get_message_text_by_id(23)
            bot.send_message(user.uid, message_text)


def lists_menu(bot, call):
    data = call.data[5:]
    user = Botuser(call.message.chat.id)
    if data == 'out':
        keyboard = user.get_subscribers_list_keyboard()
        message_text = get_message_text_by_id(25)
        bot.send_message(user.uid, message_text, reply_markup=keyboard)


    elif data == 'inc':
        pass
    elif data == 'flag':
        pass
    elif data == 'sync':
        pass
    elif data == 'add':
        pass

def delete_subscriber_menu(bot, call):
    subscriber_id = call.data[11:]
    user = Botuser(call.message.chat.id)
    user.delete_subscriber(subscriber_id)
    message_text = get_message_text_by_id(26)
    bot.send_message(user.uid, message_text)

