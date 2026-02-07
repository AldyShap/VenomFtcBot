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
        with open('messages/value/vkald.txt', 'r', encoding='utf-8') as file:
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

