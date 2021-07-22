import datetime

from BotUser.utils.keyboard_helper import get_gender_select_keyboard, get_calendar_keyboard

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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=get_message_text_by_id(19))
        if user.get_user_flag_state():
            send_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user.send_notification_to_all_subscribers(
                send_datetime=send_datetime,
                notification_type="FLAG_OFF"
            )
        else:
            datetime_now = datetime.datetime.now()
            keyboard = get_calendar_keyboard(show_time=datetime_now)
            bot.send_message(user.uid, "Время и дата окончания", reply_markup=keyboard)

        user.change_user_flag_state()

    elif data == 'reco':
        """Рекомендации"""


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


def change_time(bot, call):
    input_data = call.data.split('_')
    subject = input_data[1]
    pm = input_data[2]
    cur_time = datetime.datetime.strptime(input_data[3], '%Y-%m-%d %H:%M:%S')
    if subject == 'd':
        delta = datetime.timedelta(days=1)
    elif subject == 'h':
        delta = datetime.timedelta(hours=1)
    else:
        delta = datetime.timedelta(minutes=1)

    if pm == 'p':
        changed_time = cur_time + delta
    else:
        changed_time = cur_time - delta

    keyboard = get_calendar_keyboard(show_time=changed_time)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=call.message.text,
        reply_markup=keyboard
    )

def add_notification(bot, call):
    input_data = call.data.split('_')
    user_time = input_data[1]


    now_datetime = datetime.datetime.now()
    formatted_now_datetime = now_datetime.strftime('%Y-%m-%d %H:%M:%S')
    formatted_now_datetime = datetime.datetime.strptime(formatted_now_datetime, '%Y-%m-%d %H:%M:%S')

    selected_time = datetime.datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S')

    user = Botuser(call.message.chat.id)

    """ Отправлка напоминания опустить флаг """
    user.send_self_notification(selected_time, "FLAG_OFF_REMINDER")

    """ отправлка уведомления подписчикам """
    user.send_notification_to_all_subscribers(
        send_datetime=formatted_now_datetime,
        notification_type="FLAG_ON_SUBSCRIBERS"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_message_text_by_id(19)
    )