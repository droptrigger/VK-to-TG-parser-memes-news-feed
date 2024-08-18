import vk_api
import requests

from bot.data.config import TOKEN_VK
from bot.model.posts import follow_group, add_follow_group, get_follow

vk_session = vk_api.VkApi(token=TOKEN_VK)
vk = vk_session.get_api()


async def get_count(group_id) -> int:
    try:
        url = f'https://api.vk.com/method/wall.get?owner_id=-{group_id}&count=2&access_token={TOKEN_VK}&v=5.131'
        response = requests.get(url)
        data = response.json()
        is_pin = data['response']['items'][0]['id']
        two_post = data['response']['items'][1]['id']

        if is_pin > two_post:
            return is_pin
        elif two_post > is_pin:
            return two_post
        else:
            return is_pin

    except Exception as e:
        print(f"get_count: {e}")


async def get_group_name(group_id):
    url = f'https://api.vk.com/method/groups.getById?group_id={group_id}&access_token={TOKEN_VK}&v=5.131'
    response = requests.get(url)

    try:
        data = response.json()
        group_name = data['response'][0]['name']
        return group_name
    except Exception as e:
        print(e)


async def check_post(group_id: int, user_id: int):
    groups_list = vk_session.method('groups.get', {'user_id': '744375807'})['items']

    if group_id != 0:
        if group_id in groups_list:
            answer = await get_follow(user_id, group_id)
            if answer is None:
                print(f"Пользователь tg_id: {user_id} подписался на группу: {group_id}")
                answer = await follow_group(user_id, group_id)
                if answer is False:
                    count = await get_count(group_id)
                    name = await get_group_name(group_id)
                    await add_follow_group(user_id, group_id, count, name)

                return "already"
            else:
                print(f"Пользователь tg_id: {user_id} уже подписан на группу: {group_id}")
                return "follow"
        elif group_id not in groups_list:
            try:
                vk_session.method('groups.join', {'group_id': f'{group_id}'})

                print(f"Пользователь tg_id: {user_id} отправил запрос на добавление группы: {group_id}")
                count = await get_count(group_id)

                name = await get_group_name(group_id)

                await add_follow_group(user_id, group_id, count, name)
                return "join"
            except:
                return "kaka"