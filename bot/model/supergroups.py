import aiosqlite

from datetime import datetime
from bot.data.config import base


async def db_connect():
    try:
        conn = await aiosqlite.connect(base, check_same_thread=False)
        return conn
    except Exception as e:
        print(f"posts 10: {e}")


async def add_sup_group(id_gr: int, id_thread=None):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        if id_thread is None:
            await cursor.execute(f"INSERT INTO supergroups(id_supergroup, id_thread, add_date) VALUES ({id_gr}, -1, '{date}')")
        else:
            await cursor.execute(f"INSERT INTO supergroups(id_supergroup, id_thread, add_date) VALUES ({id_gr}, {id_thread}, '{date}')")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"supergroups.add_sup_group: {e}")


async def add_creator_group(tg_id: int, group_id: int, title: str):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"INSERT INTO creators(tg_id, group_id, title) VALUES ({tg_id}, {group_id}, '{title}')")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"supergroups.add_creator_group: {e}")


async def select_creator(tg_id: int, chat_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT * FROM creators WHERE tg_id = {tg_id} AND group_id = {chat_id}")
        row = await cursor.fetchone()
        await cursor.close()
        return row
    except Exception as e:
        print(f"select_creator: {e}")


async def select_sgr(sgr_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id, id_supergroup, id_thread, add_date FROM supergroups WHERE id_supergroup = {sgr_id}")
        data = await cursor.fetchone()
        await conn.close()
        return data
    except Exception as e:
        print(f"supergroups.select_sgr: {e}")


async def update_thread(sgr_id: int, id_thread: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"UPDATE supergroups SET id_thread = {id_thread} WHERE id_supergroup = {sgr_id}")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"supergroups.update_thread: {e}")