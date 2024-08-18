from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.model.users import select_position


async def list_group_script(groups: list, tg_id: int):
    position = await select_position(tg_id)
    all_groups = []

    for group in groups[int(position) - 6:int(position)]:
        group_item = InlineKeyboardButton(text=f'{group[0]}', callback_data=f'{group[1]}')
        all_groups.append(group_item)

    inline_keyboard = [[button] for button in all_groups]
    bottom = []

    last = InlineKeyboardButton(text=f'⬅️', callback_data=f'back')
    next = InlineKeyboardButton(text=f'➡️', callback_data=f'next')

    if position > 6 and groups[position:]:
        bottom.append(last)
        bottom.append(next)

        inline_keyboard.append(bottom)

        groups = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return groups
    elif position == 6 and groups[position:]:
        bottom.append(next)

        inline_keyboard.append(bottom)

        groups = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return groups
    elif position == 6 and not groups[position:]:

        groups = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return groups
    elif position > 6 and not groups[position:]:
        bottom.append(last)

        inline_keyboard.append(bottom)

        groups = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return groups
