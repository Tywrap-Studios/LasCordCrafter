import sqlite3

from util import info_time


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
    info_time('>SQLITE> Connected to tempbans.db.')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO tempbans VALUES (?, ?, ?, ?)',
              (user_id, guild_id, unban_time, reason))
    info_time('--> Cursor command executed.')
    conn.commit()
    info_time('--> Committed to database.')
    conn.close()
    info_time('--> Closed database connection.')


async def get_active_bans():
    conn = sqlite3.connect('databases/tempbans.db')
    info_time('>SQLITE> Connected to tempbans.db.')
    c = conn.cursor()
    c.execute('SELECT * FROM tempbans')
    info_time('--> Cursor command executed.')
    bans = c.fetchall()
    info_time('--> Fetched all from database.')
    conn.close()
    info_time('--> Closed database connection.')
    return bans


async def remove_temp_ban(user_id: int):
    conn = sqlite3.connect('databases/tempbans.db')
    info_time('>SQLITE> Connected to tempbans.db.')
    c = conn.cursor()
    c.execute('DELETE FROM tempbans WHERE user_id = ?', (user_id,))
    info_time('--> Cursor command executed.')
    conn.commit()
    info_time('--> Committed to database.')
    conn.close()
    info_time('--> Closed database connection.')
