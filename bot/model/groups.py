import aiosqlite
from bot.data.config import base


async def db_connect():
    try:
        conn = await aiosqlite.connect(base, check_same_thread=False)
        return conn
    except Exception as e:
        print(e)


async def select_groups(us_id: int) -> list:
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT name_group, group_id FROM groups WHERE id in (SELECT group_id FROM following WHERE tg_id = {us_id})")
        answer = await cursor.fetchall()
        return answer
    except Exception as e:
        print(e)
        err_list = ["0", "0", "0", "error"]
        return err_list


async def select_all_groups():
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id, group_id, last_post, name_group FROM groups")
        answer = await cursor.fetchall()
        await conn.close()
        return answer
    except Exception as e:
        print(f"select_all_groups: {e}")


async def select_all_followers(group_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id_sub, tg_id, group_id "
                             f"FROM following WHERE group_id = (SELECT id FROM groups WHERE group_id = {group_id})")
        answer = await cursor.fetchall()
        return answer
    except Exception as e:
        print(f"select_all_followers: {e}")


async def select_supergroup(group_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id, id_supergroup, id_thread, add_date FROM supergroups WHERE id_supergroup = {group_id}")
        data = await cursor.fetchone()
        await conn.close()
        return data
    except Exception as e:
        print(f"groups.select_supergroup: {e}")


async def select_group(group_id: int, tg_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT id, group_id, name_group, add_date FROM groups WHERE group_id = {group_id}")
        group_info = await cursor.fetchone()
        await cursor.execute(f"SELECT count(group_id) FROM following WHERE group_id = {group_info[0]} GROUP BY group_id")
        group_data = await cursor.fetchone()
        await cursor.execute(f"SELECT add_date FROM following WHERE group_id = {group_info[0]} and tg_id = {tg_id}")
        add_date = await cursor.fetchone()
        await conn.close()
        return group_info, group_data[0], add_date[0]
    except Exception as e:
        print(f"groups.select_group: {e}")


async def get_name(group_id):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT name_group FROM groups WHERE group_id = {group_id}")
        name = await cursor.fetchone()
        return name[0]
    except Exception as e:
        print(f"groups.get_name: {e}")