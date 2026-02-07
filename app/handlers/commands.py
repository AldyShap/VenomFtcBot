from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from app.config import keyboards as key
import first_api as api_parsing

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    with open("messages/start.txt", encoding="utf-8") as file:
        await message.answer(file.read())

@router.message(Command('first'))
async def cmd_first(message: Message):
    with open('messages/first.txt', 'r', encoding='utf-8') as file:
        await message.answer(file.read(), reply_markup=key.main_menu)

@router.message(Command('ftc'))
async def cmd_first(message: Message):
    with open('messages/ftc.txt', 'r', encoding='utf-8') as file:
        await message.answer(file.read(), reply_markup=key.main_menu)

@router.message(Command('values'))
async def cmd_values(message: Message):
    with open('messages/values.txt', 'r', encoding='utf-8') as file:
        await message.answer(file.read(), reply_markup=await key.build_values())

@router.message(Command('help'))
async def cmd_help(message: Message):
    with open('messages/help.txt', 'r', encoding='utf-8') as file:
        await message.answer(file.read())

@router.message(Command('about_us'))
async def cmd_team(message: Message):
    with open('messages/team.txt', 'r', encoding='utf-8') as file:
        await message.answer(file.read(), reply_markup=key.main_menu)


@router.message(Command('find_team'))
async def cmd_first(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Использование: /find_team <team number>")
        return
    args = command.args.strip().split()

    if len(args) != 1:
        await message.answer("❌ Укажите только номер команды")
        return
    
    try:
        team_number = int(args[0])
    except ValueError:
        await message.answer("❌ Номер команды должен быть числом")
        return
    
    msg = await message.answer("🔍 Ищу команду...")
    text = await api_parsing.get_team_info(team_number)
    await msg.edit_text(text)

@router.message(Command('ranking'))
async def cmd_ranking(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Использование: /ranking <team number>")
        return 
    
    try:
        team_number = int(command.args)
    except ValueError:
        await message.answer("Номер команды должен быть числом")
        return
    
    try:
        text = await api_parsing.get_team_ranking(team_number)
        await message.answer(text)
    except Exception as e:
        await message.answer(f"Error: {e}; Возможно, рейтинг ещё не опубликован")
        return

@router.message(Command('compare'))
async def cmd_compare(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Использование: /compare <team number, team2_number>")
    
    args = command.args.split()

    if len(args) != 2:
        await message.answer("Использование: /compare <team1> <team2>")
        return
    try:
        first_team = int(args[0])
        second_team = int(args[1])
    except ValueError:
        await message.answer("Номера команд должны быть числами")
        return
    try:
        t1 = await api_parsing.get_team_ranking_compare(first_team)
        t2 = await api_parsing.get_team_ranking_compare(second_team)
    except Exception as e:
        await message.answer(f"Error: {e}; Возможно, рейтинг ещё не опубликован")
        return

    if not t1 or not t2:
        await message.answer("❌ Не удалось получить данные по одной из команд")
        return
    
    s1, s2 = await api_parsing.compare_stats(t1, t2)

    text = (
        f"⚔️ Сравнение команд\n\n"
        f"🤖 {t1['teamNumber']} — {t1['teamName']}\n"
        f"🏆 Rank: {t1['rank']}\n"
        f"✅ Wins: {t1['wins']}\n"
        f"📊 Avg Score: {t1['avgScore']}\n\n"
        f"🤖 {t2['teamNumber']} — {t2['teamName']}\n"
        f"🏆 Rank: {t2['rank']}\n"
        f"✅ Wins: {t2['wins']}\n"
        f"📊 Avg Score: {t2['avgScore']}\n\n"
        f"🔥 Итог: {s1} : {s2}\n"
    )

    if s1 > s2:
        text += f"🏅 Побеждает команда {t1['teamNumber']}"
    elif s2 > s1:
        text += f"🏅 Побеждает команда {t2['teamNumber']}"
    else:
        text += "🤝 Ничья"

    await message.answer(text)

    
