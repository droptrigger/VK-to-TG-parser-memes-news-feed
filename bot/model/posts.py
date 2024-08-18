import aiosqlite

from datetime import datetime
from bot.data.config import base


async def db_connect():
    try:
        conn = await aiosqlite.connect(base, check_same_thread=False)
        return conn
    except Exception as e:
        print(f"posts 10: {e}")


async def follow_group(us_id: int, group_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        await cursor.execute(f"SELECT id from groups WHERE group_id = {group_id}")
        group_id = await cursor.fetchone()

        await cursor.execute(f"INSERT INTO following(tg_id, group_id, add_date) "
                             f"VALUES({us_id}, {group_id[0]}, '{date}')")
        await conn.commit()
        await conn.close()
        return True
    except Exception as e:
        print(f"follow_group: {e}")
        return False


async def add_follow_group(us_id: int, group_id: int, last_post: int, name: str):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        await cursor.execute(f"INSERT INTO groups(group_id, last_post, name_group, add_date) "
                             f"VALUES({group_id}, {last_post}, '{name}', '{date}')")
        await conn.commit()

        await cursor.execute(f"SELECT id from groups WHERE group_id = {group_id}")
        group_id = await cursor.fetchone()

        await cursor.execute(f"INSERT INTO following(tg_id, group_id, add_date) VALUES({us_id},{group_id[0]}, '{date}')")
        await conn.commit()
        await conn.close()

        return True
    except Exception as e:
        await conn.commit()
        print(f"add_follow_group: {e}")
        return False


async def get_follow(us_id: int, group_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id_sub, tg_id, group_id, add_date FROM following "
                             f"WHERE group_id = "
                             f"(SELECT id FROM groups WHERE group_id = {group_id}) and tg_id = {us_id}")
        answer = await cursor.fetchone()
        await conn.close()
        return answer
    except Exception as e:
        print(f"get_follow: {e}")
        return "error"


async def uplast_post(group_id: int, last_post: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"UPDATE groups SET last_post = {last_post} WHERE group_id = {group_id}")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"uplast_post: {e}")