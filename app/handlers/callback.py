from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.config import keyboards as key

router1 = Router()

@router1.callback_query(F.data.startswith("values_"))
async def callback_values(callback: CallbackQuery):
    await callback.answer()
    index = int(callback.data.split('_')[1])
    if index == 0:
        with open('messages/value/cracious.txt', 'r', encoding='utf-8') as file:
            await callback.message.edit_text(file.read(), reply_markup=key.back_values)
    if index == 1:
        with open('messages/value/coopertition.txt', 'r', encoding='utf-8') as file:
            await callback.message.edit_text(file.read(), reply_markup=key.back_values)
    if index == 2:
        with open('messages/value/team_work.txt', 'r', encoding='utf-8') as file:
            await callback.message.edit_text(file.read(), reply_markup=key.back_values)
    if index == 3:
        with open('messages/value/engeneering.txt', 'r', encoding='utf-8') as file:
            await callback.message.edit_text(file.read(), reply_markup=key.back_values)
    if index == 4:
        with open('messages/value/vklad.txt', 'r', encoding='utf-8') as file:
            await callback.message.edit_text(file.read(), reply_markup=key.back_values)
    if index == 5:
        with open('messages/value/conclusion.txt', 'r', encoding='utf-8') as file:
            await callback.message.edit_text(file.read(), reply_markup=key.back_values)
    

@router1.callback_query(F.data == "back_values")
async def back_to_values(callback: CallbackQuery):
    await callback.answer()
    with open('messages/values.txt', 'r', encoding='utf-8') as file:
        await callback.message.edit_text(file.read(), reply_markup= await key.build_values())

@router1.callback_query(F.data=="main_menu")
async def chat_menu(callback: CallbackQuery):
    await callback.answer()
    with open('messages/help.txt', 'r', encoding='utf-8') as file:
        await callback.message.edit_text(file.read())

@router1.callback_query(F.data == "event_code_info")
async def event_code_info(callback: CallbackQuery):
    text = """📌 Что такое Event Code?

В соревнованиях FIRST Tech Challenge каждый турнир имеет уникальный код — Event Code.

Он используется для получения матчей, рейтингов и результатов через API.

Пример:
/matches 24783 KZCMPJNB2 
                                        ^
                                        |
                               event code
"""
    await callback.message.edit_text(text, reply_markup=key.link_to_matches)
    await callback.answer()

@router1.callback_query(F.data == "team_number_info")
async def team_number_info(callback: CallbackQuery):
    text = """🔢 Что такое номер команды?

В FIRST Tech Challenge каждая команда имеет уникальный номер.

Он используется для поиска информации о команде и её матчах.

Пример:
/matches 24783 KZCMPJNB2
                        ^
                        |
                номер команды
⚠️ Номер команды должен быть числом.
"""
    await callback.message.edit_text(text, reply_markup=key.link_to_matches)
    await callback.answer()

@router1.callback_query(F.data == "event_code_info")
async def event_code_info(callback: CallbackQuery):
    text = """📌 Что такое Event Code?

В соревнованиях FIRST Tech Challenge каждый турнир имеет уникальный код — Event Code.

Он используется для получения матчей, рейтингов и результатов через API.

Пример:
/matches 24783 KZCMPJNB2 
                                        ^
                                        |
                               код ивента
"""
    await callback.message.edit_text(text, reply_markup=key.link_to_matches)
    await callback.answer()

@router1.callback_query(F.data == "back_team_events")
async def team_number_info(callback: CallbackQuery):
    text = "Матчи не найдены или неправильный ивент код. Попробуйте снова."
    await callback.message.edit_text(text, reply_markup=key.both_team_number_and_event_code)
    await callback.answer()