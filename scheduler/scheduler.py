import time

from BotUser.bot_user import Botuser
from utils import db_connector
from utils.db_connector import set_notification_sent

from utils.logger import get_logger
from utils.notifications import Notification

log = get_logger("scheduler")


def send_notification(bot, current, message_text):
    log.info(f'Message for {current.subscriber} text = {message_text}')
    bot.send_message(chat_id=current.subscriber, text=message_text)
    log.info('message sent')
    set_notification_sent(notification_id=current.id)


def check_pending(bot):
    while True:
        for notification in db_connector.get_notifications():
            current = Notification(notification)
            log.info(f"""Found notification id={current.id} for user {current.subscriber} from {current.publisher} 
                        with time {current.datetime}""")
            if current.type == 'FLAG_ON_SUBSCRIBERS':
                message_text = db_connector.get_message_text_by_id(27)
                message_text += f"{Botuser.get_user_info(current.publisher)}"
                send_notification(bot=bot, current=current, message_text=message_text)

            elif current.type == "FLAG_OFF":
                message_text = db_connector.get_message_text_by_id(28)
                message_text += f"{Botuser.get_user_info(current.publisher)}"
                send_notification(bot=bot, current=current, message_text=message_text)

            elif current.type == "FLAG_OFF_REMINDER":
                message_text = db_connector.get_message_text_by_id(29)
                send_notification(bot=bot, current=current, message_text=message_text)

        time.sleep(5)
