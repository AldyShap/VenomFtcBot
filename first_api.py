import aiohttp
from app.config.cosy import BASE_URL, HEADERS, FTC_SEASON
from datetime import datetime
from pprint import pprint

# ----------------------- Get team info by team number /find_team -----------------------------
async def get_team_info(team_number: int):
    url = f"{BASE_URL}/{FTC_SEASON}/teams?teamNumber={team_number}"

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as response:

            # ❌ Любая ошибка — сразу текст
            if response.status != 200:
                error_text = await response.text()
                return f"❌ API error {response.status}: {error_text}"

            # ✅ Только 200 — можно парсить
            data = await response.json()

            if "teams" not in data or not data["teams"]:
                return "❌ Команда не найдена"

            team = data["teams"][0]

            return (
                f"🤖 Команда: #{team['teamNumber']} ({team['nameShort']})\n"
                f"🏷 Название школы: {team['nameFull']}\n"
                f"🌍 Страна: {team['country']}\n"
                f"🏙 Город: {team['city']}\n"
                f"📅 Rookie year: {team['rookieYear']}"
            )


# ---------------------- Get all events by team number -------------------------
async def get_team_events(team_number: int):
        data = await _get(f"events?teamNumber={team_number}")

        if "events" not in data or not data["events"]:
            raise ValueError("Ивенты для команды не найдены")

        # последний ивент
        event = await get_latest_event(data["events"])
        pprint(event)
        # pprint(event)
        return event



# --------------------- Get matches by event code -------------------
async def get_team(team_number):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(f'{BASE_URL}/{FTC_SEASON}/teams?teamNumber={team_number}') as response:
            if response.status == 400:
                return None
            if response.status != 200:
                return "NoneAPI"
            return await response.json()

async def get_matches_by_code(event_code):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(f'{BASE_URL}/{FTC_SEASON}/matches/{event_code}') as response:
            if response.status == 404:
                return None
            return await response.json()

async def format_matches_of_the_team(team_number, event_code):
    matches = []
    matches_got = await get_matches_by_code(event_code)
    if matches_got is None:
        return None
    for i in matches_got.get('matches'):
        for j in i.get('teams', []):
            if j['teamNumber']==team_number:
                pprint(i)
                d = {
                    "matchNumber": i.get("matchNumber"),
                    "description": i.get("description"),
                    "Level": i.get('tournamentLevel'),
                    "alliance": j.get("station")[:-1]
                }
                partner = await get_partner_of_the_matches(d['alliance'], i, team_number)
                d['partner'] = partner
                matches.append(d)
    text = await get_beautiful_text_match(matches, team_number)
    return text
            
async def get_partner_of_the_matches(station, match, team_number):
    if station.startswith("Red"):
        for j in match.get('teams', []):
            if j['station'].startswith("Red") and j['teamNumber']!=team_number:
                d = j.get('teamNumber')

                return d
    else:
        for j in match.get('teams', []):
            if j['station'].startswith("Blue") and j['teamNumber']!=team_number:
                d = j.get('teamNumber')
                
                return d
            
async def get_beautiful_text_match(matches, team_number):
    team_name = await get_team(team_number)
    text=f"Вот список матчей команды {team_number} ({team_name['teams'][0]['nameShort']})\n"
    for i in matches:
        text += f"Номер матча: {i['matchNumber']}\nЦвет команды: {i['alliance']}\nСоюзник: {i['partner']}\nОписание: {i['description']}\nУровень: {i['Level']}\n{'--'*30}\n"
    return text

# ----------------------- Get rankings of the match by event code --------------------------------------
async def get_event_by_code(event_code):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(f"{BASE_URL}/{FTC_SEASON}/events?eventcode={event_code}") as response:
            data = await response.json()
            if not data["events"]:
                return None # ивент код не правильный
            return data["events"]

async def get_ranking_by_code(event_code):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(f"{BASE_URL}/{FTC_SEASON}/rankings/{event_code}") as response:
            print(response.status)
            if response.status == 404:
                return None # не нашлось ranking по ивент коду (возможно не правильный)
            data = await response.json()
            if not data['rankings']:
                return "not published" # не нашлось информаций в rankings (возможно не опубликован результаты)
            
            return data['rankings']
        
async def find_rankings_of_the_team(team_number, rankings):
    pprint(rankings)
    for i in rankings:
        if i['teamNumber'] == team_number:
            return i
    return None # не нашли команду на rankings

async def get_ranking_of_the_team(event_code, team_number):
    is_team = await get_team(team_number)
    if is_team is None:
        return "❌ Ошибка: Не нашлось резултатов.\n Возможно, номер команды неправильный. Попробуйте снова."
    
    rankings = await get_ranking_by_code(event_code)
    if rankings is None:
        return "❌ Ошибка: Не нашлось резултатов.\n Возможно, код ивента неправильный. Попробуйте снова."
    
    if rankings == "not published":
        return "❌ Ошибка: Не нашлось резултатов.\n Возможно, результаты еше не опубликованы. Попробуйте снова."
    
    event = await get_event_by_code(event_code)
    if event is None:
        return "❌ Ошибка: Не нашлось резултатов.\n Возможно, код ивента неправильный. Попробуйте снова."
    
    team_ranking = await find_rankings_of_the_team(team_number, rankings)
    if team_ranking is None:
        return f"❌ Ошибка: Не нашлось команды {team_number} в ивенте. Попробуйте снова."
    
    return (
        f"📍 Ивент: {event[0]['name']} ({event_code})\n"
        f"🏆 Ranking команды {team_ranking['teamNumber']} ({team_ranking['teamName']})\n\n"
        f"🥇 Место: {team_ranking['rank']}\n"
        f"🎮 Матчи: {team_ranking['matchesPlayed']}\n"
        f"✅ Победы: {team_ranking['wins']}\n"
        f"❌ Поражения: {team_ranking['losses']}\n"
        f"⚖ Ничьи: {team_ranking['ties']}\n"
        f"🚫 DQ: {team_ranking['dq']}\n"
        f"📊 Avg Score: {team_ranking.get('sortOrder2', '—')}"
    )

# ------------------------ Get ranking of the team for /compare -----------------------------
async def get_team_ranking_compare(team_number: int):
    event = await get_team_events(team_number)
    print("EVENTS")
    pprint(event)
    event_code = event["code"]
    
    if event_code == "KZCMP":

        KEREI_DIV_CODE = "KZCMPKER1"
        ZHANIBEK_DIV_CODE = "KZCMPJNB2"

        rankings_kerei = await get_ranking_by_code(KEREI_DIV_CODE)
        rankings_zhanibek = await get_ranking_by_code(ZHANIBEK_DIV_CODE)

        team_kerei = await find_rankings_of_the_team(team_number, rankings_kerei)
        team_zhanibek = await find_rankings_of_the_team(team_number, rankings_zhanibek)
        
        team = team_kerei if team_zhanibek is None else team_zhanibek

        return {
        "teamNumber": team["teamNumber"],
        "teamName": team["teamName"],
        "rank": team["rank"],
        "wins": team["wins"],
        "losses": team["losses"],
        "ties": team["ties"],
        "matches": team["matchesPlayed"],
        "avgScore": team["sortOrder2"]
        }     

    rankings = await get_ranking_by_code(event_code)
    pprint(rankings)
    if rankings == "not published":
        return "not published" #результаты не опубликованы
    
    team = await find_rankings_of_the_team(team_number, rankings)

    if team is None:
        return None
    
    return {
        "teamNumber": team["teamNumber"],
        "teamName": team["teamName"],
        "rank": team["rank"],
        "wins": team["wins"],
        "losses": team["losses"],
        "ties": team["ties"],
        "matches": team["matchesPlayed"],
        "avgScore": team["sortOrder2"]
    }

async def _get(path: str):
    url = f"{BASE_URL}/{FTC_SEASON}/{path}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as response:
            if response.status != 200:
                text = await response.text()
                raise RuntimeError(f"API {response.status}: {text}")

            return await response.json()

async def get_latest_event(events: list):
    return max(
        events,
        key=lambda e: datetime.fromisoformat(e["dateEnd"])
    )

async def compare_stats(a, b):
    score_a = 0
    score_b = 0

    if a["rank"] < b["rank"]:
        score_a += 1
    else:
        score_b += 1

    if a["wins"] > b["wins"]:
        score_a += 1
    else:
        score_b += 1

    if a["avgScore"] > b["avgScore"]:
        score_a += 1
    else:
        score_b += 1

    return score_a, score_b


