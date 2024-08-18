from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_keyboard_group(group_id: int):

    config_key = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отписаться', callback_data=f'delete_{group_id}')],
        [InlineKeyboardButton(text='назад', callback_data='back_list')]
    ])

    return config_key