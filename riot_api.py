import requests
from database import Database

db = Database()

def valid_api():
    api = db.get_api # Fetches api

    league_user = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/bob?api_key={api}").json()
    for key in league_user:
        if isinstance(league_user[key], dict):
            return False
        else:
            return True

def refresh_rank(id):
    user = db.get_user(id=id)
    server = user['server'][0]
    ign = user['ign'][0]
    api = db.get_api # Fetches api

    league_user = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}?api_key={api}").json()
    ranked_stats = requests.get(f"https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{league_user['id']}?api_key={api}").json()

    if len(ranked_stats) > 0: # If ranked stats exist
        for i in range(len(ranked_stats)): # Loops through all different rank modes f.ex Soloq/TFT/Flex
            if ranked_stats[i]['queueType'] == 'RANKED_SOLO_5x5': # If the user has a soloQ ranking
                rank = f"{ranked_stats[i]['tier'].capitalize()} {ranked_stats[i]['rank']}" # f.ex "Diamond I"
                db.update_user("rank", rank, id)
                return True