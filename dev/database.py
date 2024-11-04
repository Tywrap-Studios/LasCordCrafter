import sqlite3


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def execute_query(self, query: str, params: tuple = None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()


class DatabaseManager:
    def __init__(self):
        self.tempbans = TempBanDB()
        self.illiterate = IlliterateDB()

    def get_db(self, db_name: str) -> Database:
        return getattr(self, db_name)

    def init_all(self):
        self.tempbans.init_table()
        self.illiterate.init_table()


class TempBanDB(Database):
    def __init__(self):
        super().__init__('databases/tempbans.db')
        self.init_table()

    def init_table(self):
        query = '''CREATE TABLE IF NOT EXISTS tempbans
                  (user_id INTEGER PRIMARY KEY,
                   guild_id INTEGER,
                   unban_time TEXT,
                   reason TEXT)'''
        self.execute_query(query)

    def add_temp_ban(self, user_id: int, guild_id: int, unban_time: str, reason: str):
        self.execute_query('INSERT OR REPLACE INTO tempbans VALUES (?, ?, ?, ?)',
                           (user_id, guild_id, unban_time, reason))

    def get_active_bans(self):
        return self.execute_query('SELECT * FROM tempbans')

    def remove_temp_ban(self, user_id: int):
        self.execute_query('DELETE FROM tempbans WHERE user_id = ?', (user_id,))


class IlliterateDB(Database):
    def __init__(self):
        super().__init__('databases/illiterate.db')
        self.init_table()

    def init_table(self):
        query = '''CREATE TABLE IF NOT EXISTS illiterate
                          (user_id INTEGER PRIMARY KEY)'''
        self.execute_query(query)

    def add_person(self, user_id: int):
        self.execute_query('INSERT OR REPLACE INTO illiterate VALUES (?)', (user_id,))

    def get_amount(self):
        return self.execute_query('SELECT * FROM illiterate')
