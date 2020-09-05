import sqlite3


class SqliteHandle:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Exception as e:
            print(e)
        return conn

    def check_user(self, data):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM log_users WHERE user_id = '" + str(data) + "'")
        row = cur.fetchone()
        if row == None: return False
        else: return True

    def insert_users(self, data):
        conn = self.create_connection()
        cur = conn.cursor()
        if not self.check_user(data[0]):
            cur.execute("INSERT INTO log_users(user_id, username, chat_id, first_name) VALUES(?,?,?,?)", data)
            conn.commit()
            conn.close()

    def insert_log(self, data):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO log_request(user_id, chat_id, request) VALUES(?,?,?)", data)
        conn.commit()
        conn.close()
