from BotUser.bot_user import Botuser
from utils.db_connector import check_subscription
from utils.logger import get_logger
from utils.notifications import Notification

log = get_logger("test")


def get_result():
    data_set = ("NEW", "FLAG_ON", 12354345, "2021-06-12 09:00:00", "NEW")
    notification = Notification(data_set=data_set)
    print(notification.id)
    print(notification.type)
    print(notification.uid)
    print(notification.datetime)
    print(notification.status)




if __name__ == '__main__':
    get_result()
