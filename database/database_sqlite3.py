import sqlite3
from sqlite3 import Error

from utils.punishment import get_datetime, get_unpunish_date


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('punishments.db')
    except Error as e:
        print(f"Encountered an error with SQLite3:\n{e}")
    return conn


def execute_sql(conn, sql_data):
    try:
        c = conn.cursor()
        c.execute(sql_data)
        conn.commit()
    except Error as e:
        print(e)


def query_sql(conn, sql_data):
    c = None
    try:
        c = conn.cursor()
        c.execute(sql_data)
    except Error as e:
        print(e)
    finally:
        return c.fetchall()


def insert_ban(member_id: int, punisher_id: int, duration: str, reason: str, guild_id: int):
    conn = create_connection()
    execute_sql(conn,
                f"INSERT INTO bans VALUES ('{get_datetime()}', "
                f"{member_id}, "
                f"{punisher_id}, "
                f"{guild_id}, "
                f"'{get_unpunish_date(duration)}', "
                f"'{reason}', "
                f"'FALSE')")
    conn.commit()


def insert_mute(member_id: int, punisher_id: int, duration: str, reason: str, guild_id: int):
    execute_sql(create_connection(),
                f"INSERT INTO mutes VALUES ('{get_datetime()}', "
                f"{member_id}, "
                f"{punisher_id}, "
                f"{guild_id}, "
                f"'{get_unpunish_date(duration)}', "
                f"'{reason}', "
                f"'FALSE')")


def get_current_bans():
    return query_sql(create_connection(),
                     f"SELECT unban_date, member_id, guild_id, rowid FROM bans WHERE expired = 'FALSE' AND "
                     f"unban_date != 'Never'")


def get_current_mutes():
    return query_sql(create_connection(),
                     f"SELECT unmute_date, member_id, guild_id, rowid FROM mutes WHERE expired = 'FALSE' AND "
                     f"unmute_date != 'Never'")


def currently_muted(member_id: int):
    if query_sql(create_connection(), f"SELECT * FROM mutes WHERE expired = 'FALSE'"
                                          f"AND member_id = {member_id}"):
        return True


def expire_ban(ban_id: int):
    execute_sql(create_connection(), f"UPDATE bans SET expired = 'TRUE' WHERE rowid = {ban_id}")


def expire_mute(mute_id: int):
    execute_sql(create_connection(), f"UPDATE mutes SET expired = 'TRUE' WHERE rowid = {mute_id}")


def get_ban_history(member_id: int):
    return query_sql(create_connection(), f"SELECT * FROM bans WHERE member_id = {member_id}")


def get_mute_history(member_id: int):
    return query_sql(create_connection(), f"SELECT * FROM mutes WHERE member_id = {member_id}")


def setup():
    conn = create_connection()

    execute_sql(conn, '''CREATE TABLE IF NOT EXISTS bans 
                        (date text, 
                        member_id int, 
                        punisher_id int, 
                        guild_id int, 
                        unban_date text, 
                        reason text, 
                        expired text);''')
    execute_sql(conn, '''CREATE TABLE IF NOT EXISTS mutes 
                        (date text, 
                        member_id int, 
                        punisher_id int, 
                        guild_id int, 
                        unmute_date text, 
                        reason text, 
                        expired text);''')
