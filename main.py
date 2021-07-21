import telebot
from multiprocessing import Process

from BotUser.utils import menu_helper
from utils.db_connector import get_api_token
from utils.logger import get_logger

log = get_logger("main handler")
TOKEN = get_api_token()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start_handler(m):
    try:
        menu_helper.add_user(bot=bot, message=m)
    except Exception as e:
        log.exception(e)
        log.exception(m)
        bot.send_message(m.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['followuser'])
def follow_user(m):
    try:
        key = m.text.split()[1]
        menu_helper.follow_user(bot=bot, message=m, key=key)
    except:
        log.debug(m)
        log.exception('Got exception on main handler')
        bot.send_message(m.chat.id, 'Не указана группа, обратитесь к администратору группы')


@bot.message_handler(content_types='text')
def simple_text_message(m):
    try:
        menu_helper.text_message_handle(bot=bot, message=m)
    except Exception as e:
        log.exception(e)
        log.exception(m)
        bot.send_message(m.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'gender_')
def gender_handler(call):
    try:
        log.info("catch callback gender")
        menu_helper.select_gender(bot=bot, call=call)
    except Exception as e:
        log.exception(e)
        log.exception(call)
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:5] == 'fpms_')
def fpms_handler(call):
    try:
        log.info("catch callback fpms menu")
        menu_helper.change_flag_state(bot=bot, call=call)
    except Exception as e:
        log.exception(e)
        log.exception(call)
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


@bot.callback_query_handler(func=lambda call: call.data[:5] == 'list_')
def lists_handler(call):
    try:
        log.info("catch callback list menu")
        menu_helper.lists_menu(bot=bot, call=call)
    except Exception as e:
        log.exception(e)
        log.exception(call)
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')


# del_subscr_
@bot.callback_query_handler(func=lambda call: call.data[:11] == 'del_subscr_')
def delete_subscriber(call):
    try:
        log.info("catch callback list menu")
        menu_helper.delete_subscriber_menu(bot=bot, call=call)
    except Exception as e:
        log.exception(e)
        log.exception(call)
        bot.send_message(call.message.chat.id, 'Что-то пошло не так')



if __name__ == '__main__':
    # p1 = Process(target=check_pending, args=(bot,))
    # p1.start()
    print('Listerning...')
    bot.polling(none_stop=True)
