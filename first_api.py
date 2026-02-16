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
    # event_code = "KZCMPJNB2" event code of Central Asia FIRST Championship
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

# -------------------------- Get ranking of the team by event code ------------------------------------
async def get_team_ranking(team_number: int):
    event = await get_team_events(team_number)
    event_code = event["code"] 

    rankings = await get_ranking(event_code)

    if isinstance(rankings, str):
        return rankings

    team_rank = await find_team_ranking(rankings, team_number)

    if not team_rank:
        return "❌ Команда не найдена в рейтинге ивента"

    return (
        f"📍 Последний Ивент: {event['name']} ({event_code})\n"
        f"🏆 Ranking команды {team_rank['teamNumber']} ({team_rank['teamName']})\n\n"
        f"🥇 Место: {team_rank['rank']}\n"
        f"🎮 Матчи: {team_rank['matchesPlayed']}\n"
        f"✅ Победы: {team_rank['wins']}\n"
        f"❌ Поражения: {team_rank['losses']}\n"
        f"⚖ Ничьи: {team_rank['ties']}\n"
        f"🚫 DQ: {team_rank['dq']}\n"
        f"📊 Avg Score: {team_rank.get('sortOrder2', '—')}"
    )

# ------------------------ Get ranking of the team for /compare -----------------------------
async def get_team_ranking_compare(team_number: int):
    event = await get_team_events(team_number)
    event_code = event["code"]

    rankings = await get_ranking(event_code)
    team = await find_team_ranking(rankings, team_number)

    if not team:
        return "❌ Команда не найдена в рейтинге ивента"
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

# ------------------------------- Helper method for /compare --------------------------
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


# ------------------- Helper method of /ranking command --------------------
async def get_ranking(event_code: str):
    data = await _get(f"rankings/{event_code}")
    print(data)

    if "rankings" not in data or not data['rankings']:
        return "Error: Rankings wasn't found; Возможно, рейтинг ещё не опубликован"
    
    return data['rankings']

async def find_team_ranking(rankings: list, team_number: int):
    if rankings == "Error: Rankings wasn't found; Возможно, рейтинг ещё не опубликован":
        return None
    for r in rankings:
        if r['teamNumber'] == team_number:
            return r
    return None