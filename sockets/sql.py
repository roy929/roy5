import sqlite3


class Sql:
    file_location = '../database.db'

    def __init__(self, file=file_location):
        self.conn = sqlite3.connect(file)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS accounts (
                    name text,
                    password text,
                    ip text
                    )""")

    def does_exist(self, name):
        self.c.execute("SELECT * FROM accounts WHERE name=?", (name,))
        if self.c.fetchone():
            return True
        return False

    def insert_account(self, name, pas, ip=None):
        if not self.does_exist(name):
            with self.conn:
                self.c.execute("INSERT INTO accounts VALUES (?, ?, ?)", (name, pas, ip))
            return True
        return False

    def check_account(self, name, pas):
        self.c.execute("SELECT * FROM accounts WHERE name=? AND password=?", (name, pas))
        if self.c.fetchone():
            return True
        return False

    def remove_account(self, name, pas):
        with self.conn:
            self.c.execute("DELETE FROM accounts WHERE name=? AND password=?", (name, pas))

    def get_ip(self, name):
        if self.does_exist(name):
            with self.conn:
                self.c.execute("SELECT * FROM accounts WHERE name=?", (name,))
                s = self.c.fetchone()
                return s[2]
        return ""

    def close_conn(self):
        self.conn.close()


if __name__ == '__main__':
    database = Sql()
    print(database.check_account('tumtum', '34588'))
    database.insert_account('tumtum', '34588', '5.3.3.3')
    ip = database.get_ip('tumtum')
    print(ip)
    database.close_conn()
