import asyncio
import aiohttp

from HERO_MAP import hero_ids, hero_names, hero_ids_default, brackets
from TOKEN import token

headers = {
    "Authorization": f"Bearer {token}"}
stratz_url = "https://api.stratz.com/graphql"
data = []


async def make_request(query, session):
    global data
    response = await session.post(stratz_url, json={"query": query}, headers=headers, allow_redirects=True)
    data.append(await response.json())
    return data


async def best_worst_pos_winrate(hero_name, bracket_id):
    global data
    data = []
    winrates = []
    matches = []
    hero_id = hero_names[hero_name.lower()]
    tasks = []
    session = aiohttp.ClientSession(trust_env=True)

    for i in range(1, 6):
        query = f'''
                        {{
                            heroStats {{
                                winWeek(
                                    take: 1,
                                    heroIds: [{hero_id}]
                                    bracketIds: [{bracket_id.upper()}],
                                    positionIds: [POSITION_{str(i)}],
                                    gameModeIds: [ALL_PICK_RANKED]
                                ) {{
                                    heroId,
                                    matchCount,
                                    winCount,
                                }}
                            }}
                        }}
                    '''
        tasks.append(asyncio.create_task(make_request(query, session)))
        await asyncio.sleep(0.05)
    await asyncio.gather(*tasks)
    await session.close()

    for i in data:
        winrates.append(
            round(i['data']['heroStats']['winWeek'][0]['winCount'] / i['data']['heroStats']['winWeek'][0][
                'matchCount'] * 100, 2))
        matches.append(i['data']['heroStats']['winWeek'][0]['matchCount'])

    most_popular, best, worst = max(matches), max(winrates), min(winrates)

    return {'most_popular': [matches.index(most_popular) + 1, winrates[matches.index(most_popular)], most_popular],
            'best': [winrates.index(best) + 1, best, matches[winrates.index(best)]],
            'worst': [winrates.index(worst) + 1, worst, matches[winrates.index(worst)]]}


# print(asyncio.run(best_worst_pos_winrate('axe', 'HERALD')))


async def most_popular_characters_for_pos(position_id, bracket_id):
    global data
    data = []
    winrates = {}
    matches = {}
    tasks = []
    session = aiohttp.ClientSession(trust_env=True)

    query = f'''
                            {{
                                heroStats {{
                                    winWeek(
                                        take: 1,
                                        heroIds: [{', '.join([str(i) for i in hero_ids.keys()])}]
                                        bracketIds: [{bracket_id.upper()}],
                                        positionIds: [POSITION_{position_id}],
                                        gameModeIds: [ALL_PICK_RANKED]
                                    ) {{
                                        heroId,
                                        matchCount,
                                        winCount
                                    }}
                                }}
                            }}
                        '''
    data = await make_request(query, session)
    await session.close()
    print(data)

    for i in data[0]['data']['heroStats']['winWeek']:
        winrates.update({i['heroId']: round(i['winCount'] / i['matchCount'] * 100, 2)})
        matches.update({i['matchCount']: i['heroId']})

    return {1: [
        hero_ids_default[matches[sorted(matches)[-1]]], sorted(matches)[-1], winrates[matches[sorted(matches)[-1]]]],
        2: [hero_ids_default[matches[sorted(matches)[-2]]], sorted(matches)[-2],
            winrates[matches[sorted(matches)[-2]]]],
        3: [hero_ids_default[matches[sorted(matches)[-3]]], sorted(matches)[-3],
            winrates[matches[sorted(matches)[-3]]]]}


# print(asyncio.run(most_popular_characters_for_pos(3, 'HERALD')))
