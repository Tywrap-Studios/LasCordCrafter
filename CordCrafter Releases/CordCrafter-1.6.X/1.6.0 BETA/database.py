import sqlite3


async def init_db():
    conn = sqlite3.connect('databases/tempbans.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tempbans
                 (user_id INTEGER PRIMARY KEY,
                  guild_id INTEGER,
                  unban_time TEXT,
                  reason TEXT)''')
    conn.commit()
    conn.close()


async def add_temp_ban(user_id: int, guild_id: int, unban_time: str, reason: str):
    conn = sqlite3.connect('databases/tempbans.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO tempbans VALUES (?, ?, ?, ?)',
              (user_id, guild_id, unban_time, reason))
    conn.commit()
    conn.close()


async def get_active_bans():
    conn = sqlite3.connect('databases/tempbans.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tempbans')
    bans = c.fetchall()
    conn.close()
    return bans


async def remove_temp_ban(user_id: int):
    conn = sqlite3.connect('databases/tempbans.db')
    c = conn.cursor()
    c.execute('DELETE FROM tempbans WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
