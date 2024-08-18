import asyncio

import colorama
import vk_api
import os
import requests
import glob
import bot.model.groups as gr

from datetime import datetime
from colorama import Fore, Back

from bot.data.config import TOKEN_VK
from bot.model.groups import select_all_groups, select_all_followers
from bot.functions.check_follow import get_count
from bot.data.config import TOKEN_TG
from bot.model.posts import uplast_post

from aiogram import Bot
from aiogram.types import FSInputFile, InputMediaPhoto

vk_session = vk_api.VkApi(token=TOKEN_VK)
vk = vk_session.get_api()

bot = Bot(token=TOKEN_TG)

colorama.init(autoreset=True)  # цветной текст в консоли


async def get_photos(post_info):
    photos = []
    i = 0

    while True:
        try:
            photo = post_info[0]['attachments'][i]['photo']['sizes'][4]['url']
            photos.append(photo)
            i += 1
        except:
            break

    return photos, i


async def download_photos(photos, group, post):
    i = 0
    for url in photos:
        i += 1
        response = requests.get(url)
        with open(f"../memes/{group}/{post}_{i}.png", "wb") as file:  # можно поменять папку при необходимости
            file.write(response.content)


async def send_memes(group, post, name):
    folder_path = f'../memes/{group}'  # можно поменять папку при необходимости
    files = glob.glob(os.path.join(folder_path, f'{post}_*'))  # берем все фото с поста

    if len(files) == 1:
        users = await select_all_followers(group)
        for user in users:
            try:
                if int(user[1]) < 0:  # если это группа, а не пользователь
                    data = await gr.select_supergroup(user[1])  # ищем айди в таблице супергрупп
                    if data is None:
                        await bot.send_photo(user[1], photo=FSInputFile(f"{files[0]}"), caption=f"{name}")
                    else:
                        if int(data[2]) > 0:
                            await bot.send_photo(user[1], message_thread_id=data[2], photo=FSInputFile(f"{files[0]}"),
                                                 caption=f"{name}")

                        # это нужно из-за того, что в супергруппах есть топики, если не указать
                        # message_thread_id - выдаст ошибку

                else:
                    await bot.send_photo(user[1], FSInputFile(f"{files[0]}"), caption=f"{name}")
            except Exception as e:
                print(f"tg_id: {user[1]} ошибка с рассылкой - {e}")
    else:
        i = 0
        media = []
        users = await select_all_followers(group)

        for photo in files:
            i += 1
            if i == 1:
                media.append(InputMediaPhoto(type='photo', media=FSInputFile(f"{photo}"), caption=name))
            else:
                media.append(InputMediaPhoto(type='photo', media=FSInputFile(f"{photo}")))

        for user in users:
            try:
                if int(user[1]) < 0:
                    data = await gr.select_supergroup(user[1])
                    if data is None:
                        await bot.send_media_group(user[1], media=media, caption=f"{name}")
                    else:
                        if int(data[2]) > 0:
                            await bot.send_media_group(user[1], message_thread_id=data[2],
                                                       media=media)
                else:
                    await bot.send_media_group(user[1], media)
            except Exception as e:
                print(f"tg_id: {user[1]} ошибка с рассылкой - {e}")


async def check():
    print(f"--------------------------------------------------------------")
    while True:

        now = datetime.now()
        formatted_time = now.strftime('%H:%M:%S')

        print(f"{Back.BLACK}- time: {formatted_time} | cheсker start")
        groups = await select_all_groups()

        for group in groups:
            count = await get_count(group[1])

            if count > int(group[2]):
                print(f"{Fore.RED}n: {count} > l: {group[2]} | {group[1]} | {group[3]}")
                owner = "-" + str(group[1]) + "_" + str(count)
                try:
                    post_info = vk.wall.getById(posts=owner)

                    photos, i = await get_photos(post_info)

                    if not os.path.exists(f'../memes/{group[1]}'):
                        os.mkdir(f'../memes/{group[1]}')

                    if len(photos) != 0:
                        if len(post_info[0]['text']) < 100:  # минимальная фильтрация от рекламы
                            await download_photos(photos, group[1], group[2])
                            await send_memes(group[1], group[2], group[3])
                except Exception as e:
                    print(f"checker {e}")
            else:
                print(f"{Fore.GREEN}n: {count} = l: {group[2]} | {group[1]} | {group[3]}")

            await uplast_post(group[1], count)

        now = datetime.now()
        formatted_time = now.strftime('%H:%M:%S')

        print(f"{Back.RED}- time: {formatted_time} | cheсker sleep")
        print(f"--------------------------------------------------------------")

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(check())
