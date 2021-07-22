import time
from utils import db_connector
from utils.db_connector import set_notification_sent

from utils.logger import get_logger
from utils.notifications import Notification

# 8-9, 12-14, 18-21

log = get_logger("scheduler")


def check_pending(bot):
    while True:
        #log.info('Prepare to sql query')
        for notification in db_connector.get_notifications():
            current = Notification(notification)
            log.info(f'Found notification id={current.id} for user {current.uid} with time {current.datetime}')
            if current.type == 'FLAG_ON_SUBSCRIBERS':
                message_text = db_connector.get_message_text_by_id(7)
                log.info(f'Message for {current.uid} text = {message_text}')
                bot.send_message(chat_id=current.uid, text=message_text)
                log.info('message sent')
                set_notification_sent(notification_id=current.id)
            elif current.type == "FLAG_OFF_REMINDER":
                pass

        time.sleep(5)
