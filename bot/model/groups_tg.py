import aiosqlite

from datetime import datetime
from bot.data.config import base


async def db_connect():
    try:
        conn = await aiosqlite.connect(base, check_same_thread=False)
        return conn
    except Exception as e:
        print(e)


async def add_group(id_gr: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        await cursor.execute(f"INSERT INTO groups_tg(id_group, add_date) VALUES ({id_gr}, '{date}')")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"supergroups.add_sup_group: {e}")


async def select_gr(gr_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id, id_group, add_date FROM groups_tg WHERE id_group = {gr_id}")
        data = await cursor.fetchone()
        await conn.close()
        return data
    except Exception as e:
        print(f"groups_tg.select_sgr: {e}")


async def add_creator_group(tg_id: int, group_id: int, title: str):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"INSERT INTO creators(tg_id, group_id, title) VALUES ({tg_id}, {group_id}, '{title}')")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"groups_tg.add_creator_group: {e}")


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