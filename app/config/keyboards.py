from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


back_values = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад <-", callback_data="back_values")]
])

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="главное меню" , callback_data="main_menu")]
])
#                               0                          1                    2                              3                              4                    5                                           
inline_values = ["🔹 Gracious Professionalism", "🔹 Coopertition", "🔹 Командная работа", "🔹 Инженерное мышление и обучение", "🔹 Вклад в сообщество", "🏁 Заключение"]

async def build_values():
    keyboard = InlineKeyboardBuilder()
    for i in range(len(inline_values)):
        keyboard.add(InlineKeyboardButton(text=inline_values[i], callback_data=f'values_{i}'))
    keyboard.add(InlineKeyboardButton(text="главное меню" , callback_data="main_menu"))
    return keyboard.adjust(2).as_markup()
    
