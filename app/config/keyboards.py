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

ftc_link = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Про ftс" , url="https://www.firstinspires.org/programs/ftc/")],
    [InlineKeyboardButton(text="главное меню" , callback_data="main_menu")]
])

fll_link = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Про fll" , url="https://www.firstinspires.org/programs/fll/")],
    [InlineKeyboardButton(text="главное меню" , callback_data="main_menu")]
])


both_team_number_and_event_code = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ℹ️ Что такое Event Code?", callback_data="event_code_info")],
    [InlineKeyboardButton(text="🔢 Что такое номер команды?", callback_data="team_number_info")],
    [InlineKeyboardButton(text="главное меню" , callback_data="main_menu")]
])

link_to_matches= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Инфа о матчах и команд', url="https://ftc-events.firstinspires.org/2025/region/KZ")],
    [InlineKeyboardButton(text="Назад <-", callback_data="back_team_events")]

])

async def build_values():
    keyboard = InlineKeyboardBuilder()
    for i in range(len(inline_values)):
        keyboard.add(InlineKeyboardButton(text=inline_values[i], callback_data=f'values_{i}'))
    keyboard.add(InlineKeyboardButton(text="главное меню" , callback_data="main_menu"))
    return keyboard.adjust(2).as_markup()



    
