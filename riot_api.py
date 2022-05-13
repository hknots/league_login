import os
from dotenv import load_dotenv
import requests
from database import Database

load_dotenv()
api = os.getenv("API")
db = Database()

def refresh_rank(rowid, ign, server):
    user = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}?api_key={api}").json()
    ranked_stats = requests.get(f"https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{user['id']}?api_key={api}").json()

    if len(ranked_stats) > 0:
        for i in range(len(ranked_stats)):
            if ranked_stats[i]['queueType'] == 'RANKED_SOLO_5x5':
                rank = f"{ranked_stats[i]['tier'].capitalize()} {ranked_stats[i]['rank']}"
                return db.update("rank", rank, rowid)
                
    # If user has no soloQ Rank
    rank = "Unranked"
    return db.update("rank", rank, rowid)