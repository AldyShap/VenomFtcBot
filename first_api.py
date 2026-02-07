import aiohttp
from pprint import pprint
from app.config.cosy import BASE_URL, HEADERS, FTC_SEASON
from datetime import datetime

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
            pprint(data)

            team = data["teams"][0]

            return (
                f"🤖 Команда: #{team['teamNumber']} ({team['nameShort']})\n"
                f"🏷 Название школы: {team['nameFull']}\n"
                f"🌍 Страна: {team['country']}\n"
                f"🏙 Город: {team['city']}\n"
                f"📅 Rookie year: {team['rookieYear']}"
            )

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

async def get_team_events(team_number: int):
        data = await _get(f"events?teamNumber={team_number}")

        if "events" not in data or not data["events"]:
            raise ValueError("Ивенты для команды не найдены")

        # последний ивент
        event = await get_latest_event(data["events"])
        # pprint(event)
        return event


async def get_matches(event_code: str):
    data = await _get(f"matches/{event_code}")
    pprint(data)

    if "matches" not in data:
        raise ValueError("Матчи не найдены")

    return data["matches"]

# -------------------Helper method---------------------
async def get_team_match_info(match, team_number):
    for t in match['teams']:
        if t.get("teamNumber") == team_number:
            station = t.get("station")
            if station.startswith("Red"):
                color = "Red"
                score = match.get('scoreRedFinal')
            else:
                color = "Blue"
                score = match.get('scoreBluefinal')
            return color, score
    return None

async def get_ranking(event_code: str):
    data = await _get(f"rankings/{event_code}")
    pprint(data)

    if "rankings" not in data or not data['rankings']:
        raise ValueError("Rankings wasn't found")
    
    return data['rankings']

async def find_team_ranking(rankings: list, team_number: int):
    for r in rankings:
        if r['teamNumber'] == team_number:
            return r
    return None

async def get_team_ranking(team_number: int):
    event = await get_team_events(team_number)
    event_code = event["code"]

    rankings = await get_ranking(event_code)
    team_rank = await find_team_ranking(rankings, team_number)

    if not team_rank:
        return "❌ Команда не найдена в рейтинге ивента"

    return (
        f"📍 Последний Ивент: {event['name']} ({event['code']})\n"
        f"🏆 Ranking команды {team_rank['teamNumber']} ({team_rank['teamName']})\n\n"
        f"🥇 Место: {team_rank['rank']}\n"
        f"🎮 Матчи: {team_rank['matchesPlayed']}\n"
        f"✅ Победы: {team_rank['wins']}\n"
        f"❌ Поражения: {team_rank['losses']}\n"
        f"⚖ Ничьи: {team_rank['ties']}\n"
        f"🚫 DQ: {team_rank['dq']}\n"
        f"📊 Avg Score: {team_rank.get('sortOrder2', '—')}"
    )

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


