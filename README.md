# 🤖 Venom FTC Bot

Интерактивный Telegram-бот для фанатов FIRST и команды Venom #24783.
Позволяет получать информацию о соревнованиях, командах и ценностях программы.

# 🚀 Возможности бота

- Познакомиться с программой FIRST
- Узнать о FIRST Tech Challenge (FTC) и FIRST LEGO League (FLL)
- Получить информацию о команде Venom
- Находить статистику команд по номеру
- Сравнивать показатели двух команд

# 📜 Команды
### Общие

- /start — приветствие и информация о боте

- /help — список всех доступных команд

### О программе

- /first — что такое FIRST

- /ftc — информация о FTC

- /fll — информация о FLL

- /values — ключевые ценности FIRST

### О команде

- /about_us — информация о команде Venom

### Работа с командами

- /find_team <team number> — найти команду по номеру

- /ranking <team number> — статистика команды по последнему ивенту

- /compare <team1_number> <team2_number> — сравнение двух команд

# ⚡ Быстрый старт

1. Установить Python 3.10+

2. Клонировать репозиторий:
```
git clone https://github.com/yourusername/VenomFtcBot.git
```

3. Установить зависимости:
```
pip install -r requirements.txt
```

4. Создать .env файл:
```
python -m venv .venv
```

5. регистрируемся на сайте:
```
https://ftc-events.firstinspires.org/services/API/register
```

получаем: 
```
FTC_USER_NAME=ваш_логин
FTC_TOKEN=ваш_api_ключ
```

6. Запустить бота:

```
python main.py
```

# 📈 Примеры использования

- Найти команду:

```
/find_team 12345
```

- Посмотреть статистику команды по коду ивента:
```
/ranking 12345 EVENT_CODE
```

- Сравнить две команды:
```
/compare 12345 67890
```

- Получить список матчей по коду ивента:
```
/matches 12345 EVENT_CODE
```

# ❤️ Цель бота

- Сделать FIRST доступным каждому
- Помочь новичкам быстро понять соревнования
- Удобно анализировать и сравнивать команды

# 📬 Контакты

- Команда Venom: 
```
team_contacts = {
    'Instagram': 'https://www.instagram.com/venom_firstkz?igsh=MTh4ZWF3eGJtZ290',
    'Telegram': 'https://t.me/venomteam24783',
    'Website': None
}
```

- GitHub: создавай issues, предлагай фичи, фикс баги
