import asyncio
import aiosqlite
import vk_api
import os

from bot.data.config import TOKEN_VK

vk_session = vk_api.VkApi(token=TOKEN_VK)
vk = vk_session.get_api()


async def check_post():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'memkid_base.db')
    conn = await aiosqlite.connect(db_path)
    cursor = await conn.cursor()

    url = "https://vk.com/wall-224587053_3"
    post = url[url.find("wall") + 4:]

    post_info = vk.wall.getById(posts=post)
    print(post_info)

    group_id = url[url.find("-") + 1:url.find("_")]

    post = url[url.find("_") + 1:]

    tg_id = 123
    if len(post_info) == 0:
        try:
            await cursor.execute(f"SELECT id_request, tg_id, group_id, last_post FROM requests WHERE group_id = {group_id}")
            data = await cursor.fetchone()
            if data is None:
                vk_session.method('groups.join', {'group_id': f'{group_id}'})
                await cursor.execute(f"INSERT INTO requests (tg_id, group_id, last_post) VALUES ({tg_id}, {group_id}, {post})")
                await conn.cursor()
                error = "closed"
                return error
            else:
                print("test2")
                msg = "the_request"
                return msg
        except vk_api.exceptions.ApiError:
            print("test")
            error = "no_group"
            return error
        except Exception as _ex:
            print(_ex)
            error = "gavno"
            return error
    else:
        list = vk_session.method('groups.get', {'user_id': '744375807'})['items']
        print(list)

        if f"{group_id}" in list:
            print("yes")
        elif f"{group_id}" not in list:
            vk_session.method('groups.join', {'group_id': f'{group_id}'})


asyncio.run(check_post())