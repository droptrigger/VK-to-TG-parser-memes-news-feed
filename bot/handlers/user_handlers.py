import bot.keyboards.user_keyboards as key

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery

from bot.data.config import TOKEN_TG
from bot.model import users
from bot.model import groups as group
from bot.model import supergroups as sgr
from bot.model import groups_tg as gr
from bot.functions.check_follow import check_post
from bot.functions.get_id_func import getID
from bot.keyboards.list_group import list_group_script
from bot.keyboards.list_group_for_groups import list_group_script as lgs
from bot.keyboards.setting_group import get_keyboard_group


router = Router()
bot = Bot(TOKEN_TG)


@router.callback_query()
async def general_callback(callback: CallbackQuery):
    tg_id = int(callback.from_user.id)

    match callback.message.chat.type:
        case "private":
            match callback.data:

                case "add_group":
                    await users.update_state(us_id=tg_id, state='add_group')
                    await callback.message.edit_text("Отправьте ссылку на группу", reply_markup=key.otmena_key)

                case "back_groups":
                    await users.update_state(state='start_menu', us_id=tg_id)
                    await callback.message.edit_text("Окей!", reply_markup=key.group_main)

                case "stop_add":
                    await users.update_state(state='start_menu', us_id=tg_id)
                    await callback.message.edit_text("Окей!", reply_markup=key.group_main)

                case "list_group":
                    groups = await group.select_groups(tg_id)

                    if len(groups) == 0:
                        await callback.answer("Вы не подписаны ни на одну группу")
                    else:
                        await callback.message.edit_text("Ляляля!", reply_markup=await list_group_script(groups, tg_id))
                        await users.update_state(state='see_list', us_id=tg_id)

                case "back_from_list":
                    await users.reset_position(tg_id)
                    await users.update_state(state='start_menu', us_id=tg_id)
                    await callback.message.edit_text("Окей!", reply_markup=key.group_main)

                case "back_list":
                    groups = await group.select_groups(tg_id)
                    await callback.message.edit_text("Окей!", reply_markup=await list_group_script(groups, tg_id))

                case "next":
                    gr = await group.select_groups(tg_id)
                    position = await users.select_position(tg_id)

                    if int(position) < len(gr):
                        await users.reposition(tg_id, "next")
                        await callback.message.edit_text(f"{int((position + 6) / 6)} | {int(len(gr) / 6) + 1}",
                                                         reply_markup=await list_group_script(gr, tg_id))
                    else:
                        await callback.message.edit_text("Ошибка!", reply_markup=await list_group_script(gr, tg_id))

                case "back":
                    gr = await group.select_groups(tg_id)
                    position = await users.select_position(tg_id)

                    if position > 6:
                        await users.reposition(tg_id, "back")
                        await callback.message.edit_text(f"{int((position - 6) / 6)} | {int(len(gr) / 6) + 1}",
                                                         reply_markup=await list_group_script(gr, tg_id))
                    else:
                        await callback.message.edit_text("Ошибка!", reply_markup=await list_group_script(gr, tg_id))

                case _:
                    if "delete" in callback.data:
                        test = callback.data
                        x = test.find("_") + 1

                        id = test[x:]
                        gr = await group.select_groups(tg_id)
                        name = await group.get_name(id)

                        await users.unfollow(tg_id, id)
                        await callback.answer(f"Вы отписались от группы {name}")
                        await callback.message.edit_text("Успешно!", reply_markup=await list_group_script(gr, tg_id))
                    else:
                        try:
                            group_info, followers, add_date = await group.select_group(callback.data, tg_id)

                            text = (f"Группа - {group_info[2]}\nДобавлена в базу данных - {group_info[3]}\n"
                                    f"Вы подписаны на нее с {add_date}\nВсего подписчиков: {followers}")

                            await callback.message.edit_text(text=text,
                                                             reply_markup=await get_keyboard_group(group_info[1]))
                        except:
                            gr = await group.select_groups(tg_id)
                            await callback.message.edit_text(text="Что-то пошло не так",
                                                             reply_markup=await list_group_script(gr, tg_id))

        case _:  # supergroups, groups
            tg_id = callback.message.chat.id
            match callback.data:

                case "back_list":
                    groups = await group.select_groups(tg_id)
                    await callback.message.edit_text("Окей!", reply_markup=await lgs(groups, tg_id))

                case "next":
                    gr = await group.select_groups(tg_id)
                    position = await users.select_position(tg_id)

                    if int(position) < len(gr):
                        await users.reposition(tg_id, "next")
                        await callback.message.edit_text(f"{int((position + 6) / 6)} | {int(len(gr) / 6) + 1}",
                                                         reply_markup=await lgs(gr, tg_id))
                    else:
                        await callback.message.edit_text("Ошибка!", reply_markup=await lgs(gr, tg_id))

                case "back":
                    gr = await group.select_groups(tg_id)
                    position = await users.select_position(tg_id)

                    if position > 6:
                        await users.reposition(tg_id, "back")
                        await callback.message.edit_text(f"{int((position - 6) / 6)} | {int(len(gr) / 6) + 1}",
                                                         reply_markup=await lgs(gr, tg_id))
                    else:
                        await callback.message.edit_text("Ошибка!", reply_markup=await lgs(gr, tg_id))

                case _:
                    if "delete" in callback.data:
                        test = callback.data
                        x = test.find("_") + 1

                        id = test[x:]
                        name = await group.get_name(id)

                        await users.unfollow(tg_id, id)
                        gr = await group.select_groups(tg_id)
                        await callback.answer(f"Вы отписались от группы {name}")
                        await callback.message.edit_text("Успешно!", reply_markup=await lgs(gr, tg_id))
                    else:
                        try:
                            group_info, followers, add_date = await group.select_group(callback.data, tg_id)

                            text = (f"Группа - {group_info[2]}\nДобавлена в базу данных - {group_info[3]}\n"
                                    f"Вы подписаны на нее с {add_date}\nВсего подписчиков: {followers}")

                            await callback.message.edit_text(text=text,
                                                             reply_markup=await get_keyboard_group(group_info[1]))
                        except:
                            gr = await group.select_groups(tg_id)
                            await callback.message.edit_text(text="Что-то пошло не так",
                                                             reply_markup=await lgs(gr, tg_id))


@router.message()
async def general(message: Message):
    """Eating all messages"""
    if message.chat.type == "private":
        tg_id = message.from_user.id

        user_data = await users.select_user_info(us_id=tg_id)

        if user_data is None:
            await users.add_user(us_id=tg_id)
            await message.answer("Привет, я - мемкид бот", reply_markup=key.main_key)

        else:
            state = user_data[3]
            print(f"\n     user: {tg_id} | state: {state}")

            match state:
                case "start_menu":
                    await message.answer("Используйте кнопки!", reply_markup=key.group_main)
                case "hello_menu":
                    await message.answer("Используйте кнопки!", reply_markup=key.group_main)
                case "add_group":
                    if message.text is not None:
                        link = message.text
                        link = await getID(link)

                        if link is False:
                            await message.reply("Что-то не могу найти такую группу :/",
                                                reply_markup=key.stop_add_key)
                        else:
                            reply = await check_post(link, message.from_user.id)
                            match reply:
                                case "join":
                                    await message.reply("Теперь вы получаете новости с данной группы",
                                                        reply_markup=key.stop_add_key)
                                case "already":
                                    await message.reply("Теперь вы получаете новости с данной группы",
                                                        reply_markup=key.stop_add_key)
                                case "follow":
                                    await message.reply("Вы уже подписаны на новости данной группы",
                                                        reply_markup=key.stop_add_key)
                                case "kaka":
                                    await message.reply("Не пытайтесь меня обмануть!",
                                                        reply_markup=key.stop_add_key)
                    else:
                        await message.reply("Не пытайся меня обмануть!",
                                            reply_markup=key.stop_add_key)
                case "error":
                    await message.reply("Ёмаё, что-то мне плохо, попробуй еще раз...")

    elif message.chat.type == "supergroup":

        if message.new_chat_members is not None:  # Приветственное сообщение
            new_members = message.new_chat_members
            for member in new_members:
                user_id = member.id
                if user_id == 7062857043:
                    yes = await sgr.select_sgr(message.chat.id)
                    if yes is None:
                        await users.add_list_position(message.chat.id)
                        await sgr.add_sup_group(message.chat.id)

                        await message.answer("Привет!\n\nВижу в этой беседе есть темы, для работы "
                                         "мне необходимо, чтобы кто-нибудь из администраторов использовал команду "
                                         "«мем сюда», в тему, куда будут отправляться мемы.\nТемы можно будет менять "
                                         "этой же командой.\n\nЕсли все прошло успешно, я дам знать ответным сообщением,"
                                         " в котором расскажу как мной управлять, "
                                         "иначе проверьте имею ли я доступ к сообщениям, если нет, выдайте.")
                    else:
                        await message.answer("Рад вернуться!")

        if message.new_chat_members is None:
            if message.text is not None:

                if message.text == "list":
                    groups = await group.select_groups(message.chat.id)

                    if len(groups) == 0:
                        await message.reply("Вы не подписаны ни на одну группу")
                    else:
                        await message.reply("Вот группы, на которые вы подписаны!",
                                            reply_markup=await lgs(groups, message.chat.id))

                if message.text.startswith("add "):
                    link = message.text.split(" ")[1]
                    link = await getID(link)

                    if link is False:
                        await message.reply("Что-то не могу найти такую группу :/")
                    else:
                        reply = await check_post(link, message.chat.id)
                        match reply:
                            case "join":
                                await message.reply("Теперь вы получаете новости с данной группы")
                            case "already":
                                await message.reply("Теперь вы получаете новости с данной группы")
                            case "follow":
                                await message.reply("Вы уже подписаны на новости данной группы")
                            case "kaka":
                                await message.reply("Не пытайтесь меня обмануть!")

                if message.text.lower() in ["мем сюда", "vtv c.lf", "meme here"]:
                    admins = await bot.get_chat_administrators(message.chat.id)
                    admin_list = []

                    creator = 0
                    for admin in admins:
                        if admin.status == "creator":
                            creator = admin.user.id
                        admin_list.append(admin.user.id)

                    if message.from_user.id in admin_list:

                        yes = await sgr.select_sgr(message.chat.id)
                        yes_creator = await sgr.select_creator(creator, message.chat.id)

                        if yes is None:
                            await sgr.add_sup_group(message.chat.id, message.message_thread_id)

                        else:
                            if yes_creator is None:
                                await sgr.add_creator_group(creator, message.chat.id, message.chat.title)
                                await message.reply(f"Отлично! Теперь завершили мою настройку рассылки.")
                            else:
                                await sgr.update_thread(message.chat.id, message.message_thread_id)
                                await message.reply(f"Отлично! Теперь мемы будут отправляться сюда")
                    else:
                        await message.reply("Вы не администратор!")

    elif message.chat.type == "group":
        if message.new_chat_members is not None:  # Приветственное сообщение
            new_members = message.new_chat_members
            for member in new_members:
                user_id = member.id
                if user_id == 7062857043:
                    admins = await bot.get_chat_administrators(message.chat.id)

                    creator = 0
                    for admin in admins:
                        if admin.status == "creator":
                            creator = admin.user.id
                            break

                    crea = await gr.select_creator(creator, message.chat.id)

                    if crea is None:
                        await gr.add_creator_group(creator, message.chat.id, message.chat.title)

                    yes = await gr.select_gr(message.chat.id)
                    if yes is None:
                        await users.add_list_position(message.chat.id)
                        await gr.add_group(message.chat.id)

                        await message.answer("Привет!")
                    else:
                        await message.answer("Рад вернуться!")

        if message.new_chat_members is None:
            if message.text is not None:
                if message.text == "list":
                    groups = await group.select_groups(message.chat.id)

                    if len(groups) == 0:
                        await message.reply("Вы не подписаны ни на одну группу")
                    else:
                        await message.reply("Вот группы, на которые вы подписаны!",
                                            reply_markup=await lgs(groups, message.chat.id))

                if message.text.startswith("add "):
                    link = message.text.split(" ")[1]
                    link = await getID(link)

                    if link is False:
                        await message.reply("Что-то не могу найти такую группу :/")
                    else:
                        reply = await check_post(link, message.chat.id)
                        match reply:
                            case "join":
                                await message.reply("Теперь вы получаете новости с данной группы")
                            case "already":
                                await message.reply("Теперь вы получаете новости с данной группы")
                            case "follow":
                                await message.reply("Вы уже подписаны на новости данной группы")
                            case "kaka":
                                await message.reply("Не пытайтесь меня обмануть!")