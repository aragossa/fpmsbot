from BotUser.bot_user import Botuser
from utils.db_connector import check_subscription
from utils.logger import get_logger

log = get_logger("test")


def get_result():
    user = Botuser(556047985)
    result = user.get_subscribers()
    print(result)



def check_subscriptio():
    result = check_subscription(556047985, 556047985)
    print(result)

if __name__ == '__main__':
    get_result()
