from BotUser.utils.keyboard_helper import get_main_keyboard_female, get_main_keyboard_male, \
    get_fpms_menu_keyboard_flag_off, get_fpms_menu_keyboard_flag_on, get_lists_menu_keyboard_male, \
    get_lists_menu_keyboard_female, get_subscribres_keyboard
from utils import db_connector
from utils.logger import get_logger
from utils.notifications import Notification

log = get_logger("bot_user")


class Botuser:

    def __init__(self, uid):
        self.uid = uid
        self.gender = self.__get_user_gender()

    @staticmethod
    def get_user_info(uid):
        user_info = db_connector.get_user_info(uid=uid)
        first_name = user_info[0]
        last_name = user_info[1]
        username = user_info[2]
        formatted_username = Botuser.prepare_user_name(first_name=first_name,
                                                   last_name=last_name,
                                                   username=username
                                                   )
        return formatted_username



    @staticmethod
    def prepare_user_name(first_name, last_name, username):
        if username != 'None':
            return username
        else:
            name = first_name
            if last_name != "None":
                name += f" {last_name}"
            return name

    def check_auth(self):
        if db_connector.check_auth(self.uid):
            return True
        else:
            return False

    def __get_user_gender(self):
        log.info(db_connector.get_user_gender(uid=self.uid))
        return db_connector.get_user_gender(uid=self.uid)

    def add_user(self, gender, first_name, last_name, username):
        if gender == "fem":
            gender = "FEMALE"
        else:
            gender = "MALE"
        db_connector.add_user(uid=self.uid, gender=gender, first_name=first_name, last_name=last_name,
                              username=username)

    def check_user_state_input(self):
        if db_connector.get_user_state(uid=self.uid)[0] == "INPUT":
            return True

    def get_user_main_menu_keyboard(self):
        log.info(self.gender)
        if self.gender == 'MALE':
            return get_main_keyboard_male()
        else:
            return get_main_keyboard_female()

    def get_user_flag_state(self):
        if db_connector.get_user_flag_state_by_uid(uid=self.uid) == "ON":
            return True
        else:
            return False

    def change_user_flag_state(self):
        if self.get_user_flag_state():
            db_connector.update_user_flag_state(uid=self.uid, state="OFF")
        else:
            db_connector.update_user_flag_state(uid=self.uid, state="ON")

    def get_fpms_menu_keyboard(self):
        if self.get_user_flag_state():
            return get_fpms_menu_keyboard_flag_on()
        else:
            return get_fpms_menu_keyboard_flag_off()

    def update_gender(self, gender):
        if gender == "fem":
            db_connector.update_user_gender(uid=self.uid, gender="FEMALE")
        elif gender == "mal":
            db_connector.update_user_gender(uid=self.uid, gender="MALE")

    def check_subscription(self, publisher_id):
        if db_connector.check_subscription(publisher_id=publisher_id, subscriber_id=self.uid) > 0:
            return True
        else:
            return False

    def __check_publisher_id(self, publisher_id):
        return db_connector.check_publisher_id(publisher_id)

    def add_subscription(self, publisher_id):
        if self.__check_publisher_id(publisher_id) > 0:
            db_connector.add_subscription(publisher_id=publisher_id, subscriber_id=self.uid)
            return True
        else:
            return False

    def get_subscribers(self):
        subscribers = db_connector.get_subscribers_list(self.uid)
        subscribers_list = []
        if len(subscribers) > 0:
            for elem in subscribers:
                user_name_prepared = Botuser.prepare_user_name(first_name=elem[2], last_name=elem[3], username=elem[4])
                subscribers_list.append((elem[1], user_name_prepared))
            return subscribers_list
        else:
            return None

    def get_lists_menu_keyboard(self):
        if self.gender == 'MALE':
            log.info("male")
            return get_lists_menu_keyboard_male()
        else:
            log.info("female")
            return get_lists_menu_keyboard_female()

    def get_subscribers_list_keyboard(self):
        return get_subscribres_keyboard(self.get_subscribers())

    def delete_subscriber(self, subscriber_id):
        db_connector.delete_subscriber_db(self.uid, subscriber_id)


    def send_self_notification(self, send_datetime, notification_type):
        data_set = ("NEW", notification_type, self.uid, self.uid, send_datetime, "NEW")
        notification = Notification(data_set=data_set)
        db_connector.add_notification(notification=notification)


    def send_notification_to_all_subscribers(self, send_datetime, notification_type):
        subscribers = db_connector.get_subscribers_list(self.uid)
        for subscriber in subscribers:
            log.info(notification_type)
            log.info(send_datetime)
            data_set = ("NEW", notification_type, self.uid, subscriber[1], send_datetime, "NEW")
            notification = Notification(data_set=data_set)
            db_connector.add_notification(notification=notification)
