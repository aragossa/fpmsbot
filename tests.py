from BotUser.bot_user import Botuser
from utils.db_connector import check_subscription
from utils.logger import get_logger
from utils.notifications import Notification

log = get_logger("test")


def get_result():
    name = Botuser.get_user_info(1903075433)
    print(name)



if __name__ == '__main__':
    get_result()
