import aiosqlite
from bot.data.config import base
from datetime import datetime


async def db_connect():
    try:
        conn = await aiosqlite.connect(base, check_same_thread=False)
        return conn
    except Exception as e:
        print(e)


async def select_user_info(us_id: int) -> list:
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT us_id, tg_id, count_groups, state, add_date FROM users WHERE tg_id = {us_id}")
        answer = await cursor.fetchone()
        await conn.close()
        return answer
    except Exception as e:
        print(e)
        err_list = ["0", "0", "0", "error"]
        return err_list


async def add_user(us_id: int) -> bool:
    conn = await db_connect()
    cursor = await conn.cursor()
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        await cursor.execute(f"INSERT INTO users (tg_id, state, add_date) VALUES ({us_id}, 'hello_menu', '{date}')")
        await conn.commit()
        await cursor.execute(f"INSERT INTO list_position (tg_id, list_pos) VALUES ({us_id}, 6)")
        await conn.commit()
        await conn.close()
        return True
    except Exception as e:
        print(e)
        return False


async def update_state(us_id: int, state: str):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"UPDATE users SET state = '{state}' WHERE tg_id = {us_id}")
        await conn.commit()
        await conn.close()
        return True
    except Exception as e:
        print(f"update_state: {e}")


async def reset_position(us_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"UPDATE list_position SET list_pos = 6 WHERE tg_id = {us_id}")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"reposition: {e}")


async def reposition(us_id: int, what: str):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        if what == "back":
            await cursor.execute(f"UPDATE list_position SET list_pos = list_pos - 6 WHERE tg_id = {us_id}")
            await conn.commit()
        elif what == "next":
            await cursor.execute(f"UPDATE list_position SET list_pos = list_pos + 6 WHERE tg_id = {us_id}")
            await conn.commit()

        await conn.close()
    except Exception as e:
        print(f"reposition: {e}")


async def select_position(us_id: int) -> int:
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"SELECT list_pos FROM list_position WHERE tg_id = {us_id}")
        answer = await cursor.fetchone()
        await conn.close()
        return answer[0]
    except Exception as e:
        print(f"select_postition: {e}")


async def add_list_position(us_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"INSERT INTO list_position (tg_id, list_pos) VALUES ({us_id}, 6)")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"users.add_list_position: {e}")


async def unfollow(tg_id: int, group_id: int):
    try:
        conn = await db_connect()
        cursor = await conn.cursor()
        await cursor.execute(f"DELETE FROM following WHERE tg_id = {tg_id} AND group_id = (SELECT id FROM groups WHERE group_id = {group_id})")
        await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"users.unfollow: {e}")