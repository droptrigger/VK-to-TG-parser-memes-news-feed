from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

my_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='канал создателя', url='https://t.me/CreateTrigger')]
])

group_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='добавить группу', callback_data='add_group')],
    [InlineKeyboardButton(text='список групп', callback_data='list_group')],
])

otmena_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='отмена', callback_data='back_groups')]
])

stop_add_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='назад', callback_data='stop_add')],
])