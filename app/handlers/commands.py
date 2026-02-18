from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from app.config import keyboards as key
import first_api as api_parsing
from pprint import pprint
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
        await message.answer(file.read(), reply_markup=key.ftc_link)

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
    try:
        text = await api_parsing.get_team_info(team_number)
    except Exception as e:
        await msg.edit_text(e)

    await msg.edit_text(text)

@router.message(Command('ranking'))
async def cmd_ranking(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Использование: /ranking <team_number event_code>")
        return 
    args = command.args.split()
    if len(args) != 2:
        await message.answer("Вы должны прописать номер команды, потом через пробел, напишите код ивента.", reply_markup=key.both_team_number_and_event_code)
        return
    try:
        team_number = int(args[0])
        event_code = args[1]
    except ValueError:
        await message.answer("Номер команды должен быть числом, код ивента текстом", reply_markup=key.both_team_number_and_event_code)
        return
    
    msg = await message.answer("🔍 Ищу команду...")
    
    try:
        text = await api_parsing.get_ranking_of_the_team(event_code, team_number)
        print(text)
        await msg.edit_text(text)
    except Exception as e:
        await msg.edit_text(f"Error: {e}")
        return

@router.message(Command('compare'))
async def cmd_compare(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Использование: /compare <team1_number, team2_number>")
    
    args = command.args.strip().split()

    if len(args) != 2:
        await message.answer("Использование: /compare <team1_number> <team2_number>")
        return
    try:
        first_team = int(args[0])
        second_team = int(args[1])
    except ValueError:
        await message.answer("Номера команд должны быть числами")
        return
    
    msg = await message.answer("🔍 Ищу команду...")

    try:
        t1 = await api_parsing.get_team_ranking_compare(first_team)
        t2 = await api_parsing.get_team_ranking_compare(second_team)
    except Exception as e:
        await msg.edit_text(f"Error: {e}; Возможно, рейтинг ещё не опубликован")
        return

    if not t1 or not t2:
        await msg.edit_text("❌ Не удалось получить данные по одной из команд")
        return
    
    if t1 is None:
        return f"❌ Ошибка: Не нашлось команды {first_team} в ивенте. Попробуйте снова."
    
    if t2 is None:
        return f"❌ Ошибка: Не нашлось команды {second_team} в ивенте. Попробуйте снова."
    
    if t1 == "not published":
        return f"❌ Не удалось получить данные команды: {first_team}. Возможно результаты еше не опубликованы"
    
    if t2 == "not published":
        return f"❌ Не удалось получить данные команды : {second_team} . Возможно результаты еше не опубликованы"
    
    await msg.edit_text("🔍 Думаю...")
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

    await msg.edit_text(text)

@router.message(Command('fll'))
async def cmd_links(message: Message):
    with open('messages/fll.txt', 'r', encoding='utf-8') as file:
        await message.answer(file.read(), reply_markup=key.fll_link)

@router.message(Command("matches"))
async def cmd_matches(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Использование: /matches <team number eventcode>", reply_markup=key.both_team_number_and_event_code)
        return
    values = command.args.split()
    if len(values)!=2:
        await message.answer("Вы должны прописать номер команды, потом через пробел, напишите код ивента.", reply_markup=key.both_team_number_and_event_code)
        return
    try:
        team_number = int(values[0])
        event_code = values[1]
    except ValueError:
        await message.answer("Номер команды должен быть числом")
        return

    msg = await message.answer("🔍 Ищу команду...")

    try:
        team = await api_parsing.get_team(team_number)

        if team is None:
            await msg.edit_text(f"Команда {team_number} не найдена :(\nНомер команды должен быть в диапазоне от 0 до 99999\nПопробуйте снова", reply_markup=key.both_team_number_and_event_code)
            return
        if team == "NoneAPI":
                await msg.edit_text("Упс...\nПохоже произошла ошибка, попробуйте снова.", reply_markup=key.both_team_number_and_event_code)
                return

        await msg.edit_text("📊 Загружаю матчи...")

        matches = await api_parsing.format_matches_of_the_team(team_number, event_code)

        if not matches or matches is None:
            await msg.edit_text("Матчи не найдены или неправильный ивент код. Попробуйте снова.", reply_markup=key.both_team_number_and_event_code)
            return

        await msg.edit_text(matches)

    except Exception as e:
        await msg.edit_text("Произошла ошибка при запросе к API 😔")
        print("Ошибка:", e)

@router.message()
async def catch_random(message: Message):
    await message.answer("Извините, но я не знаю эту функцию. Если у вас проблемы: /help")