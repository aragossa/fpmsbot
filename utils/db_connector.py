import sqlite3

from utils.logger import get_logger

log = get_logger("db_connector")


def connection():
    connect = sqlite3.connect('data/database.db')
    cursor = connect.cursor()
    return connect, cursor


""" CONFIG METHODS"""


def get_api_token():
    con, cur = connection()
    with con:
        cur.execute("""SELECT value FROM configuration WHERE name = 'api_token'""")
        return cur.fetchone()[0]


def get_bot_name():
    con, cur = connection()
    with con:
        cur.execute("""SELECT value FROM configuration WHERE name = 'bot_name'""")
        return cur.fetchone()[0]


def check_auth(uid):
    con, cur = connection()
    with con:
        cur.execute(f"SELECT id FROM users WHERE id = {uid}")
        return cur.fetchone()


""" BOT METHODS"""


def get_message_text_by_id(message_id):
    con, cur = connection()
    with con:
        cur.execute(f"""SELECT message_text FROM messages WHERE id = '{message_id}'""")
        return cur.fetchone()[0]


""" USER METHODS"""


def get_user_state(uid):
    con, cur = connection()
    with con:
        cur.execute(f"""SELECT state, input_value FROM users_state WHERE id ={uid}""")
        return cur.fetchone()


def get_user_flag_state_by_uid(uid):
    con, cur = connection()
    with con:
        cur.execute(f"""SELECT fpms_flag FROM users_state WHERE id ={uid}""")
        return cur.fetchone()[0]


def update_user_flag_state(uid, state):
    con, cur = connection()
    with con:
        cur.execute(f"""UPDATE users_state SET fpms_flag = '{state}' WHERE id ={uid}""")


def update_user_state(uid, state, input_value):
    con, cur = connection()
    with con:
        cur.execute(f"""UPDATE users_state SET state = '{state}', input_value = '{input_value}' WHERE id ={uid}""")


def update_user_gender(uid, gender):
    con, cur = connection()
    with con:
        cur.execute(f"""UPDATE users SET gender = '{gender}' WHERE id ={uid}""")


def get_user_gender(uid):
    con, cur = connection()
    with con:
        cur.execute(f"SELECT gender FROM users WHERE id = {uid}")
        query_result = cur.fetchone()
        if query_result:
            return query_result[0]
        else:
            return "not specified"


def check_subscription(publisher_id, subscriber_id):
    con, cur = connection()
    with con:
        cur.execute(
            f"SELECT COUNT(*) FROM subscriptions WHERE publisher_id = {publisher_id} AND subscriber_id={subscriber_id}")
        return int(cur.fetchone()[0])


def check_publisher_id(publisher_id):
    con, cur = connection()
    with con:
        cur.execute(f"SELECT COUNT(*) FROM users WHERE id = {publisher_id}")
        return int(cur.fetchone()[0])


def add_subscription(publisher_id, subscriber_id):
    con, cur = connection()
    with con:
        cur.execute(
            f"""INSERT INTO subscriptions (publisher_id, subscriber_id) VALUES ({publisher_id}, {subscriber_id})""")


def add_user(uid, gender, first_name, last_name, username):
    con, cur = connection()
    with con:
        cur.execute(f"""INSERT INTO users (id, gender, first_name, last_name, username)
                        VALUES ({uid}, '{gender}', '{first_name}', '{last_name}', '{username}')""")
        if gender == "MALE":
            cur.execute(f"""INSERT INTO users_state (id) VALUES ({uid})""")
        else:
            cur.execute(f"""INSERT INTO users_state (id, fpms_flag) VALUES ({uid}, 'OFF')""")
        return True


def get_subscribers_list(publisher_id):
    con, cur = connection()
    with con:
        query = f"""SELECT publisher_id, subscriber_id, first_name, last_name, username
            FROM subscriptions 
            INNER JOIN users
	            ON subscriber_id = id
            WHERE publisher_id = {publisher_id}"""
        cur.execute(query)
        return cur.fetchall()


def delete_subscriber_db(publisher_id, subscriber_id):
    con, cur = connection()
    with con:
        query = f"""DELETE FROM subscriptions
                    WHERE publisher_id = {publisher_id}
                    AND subscriber_id = {subscriber_id}"""
        cur.execute(query)
