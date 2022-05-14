import os
from dotenv import load_dotenv
import requests
from database import Database
from menu import clear_terminal

db = Database()

def refresh_rank(rowid, ign, server):
    load_dotenv()
    api = os.getenv("API")

    user = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}?api_key={api}").json()
    try:
        if user['status']['status_code'] == 403: # If invalid API
            clear_terminal()
            print("You tried refreshing ranks without a valid API")
            print("Get your personal API from https://developer.riotgames.com/")
            new_api = input("Paste API if you got one: ")
            with open('.env', 'w') as env:
                env.write(f"API={new_api}")
            return clear_terminal()
    except KeyError: # If valid API
        pass

    ranked_stats = requests.get(f"https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{user['id']}?api_key={api}").json()

    if len(ranked_stats) > 0:
        for i in range(len(ranked_stats)):
            if ranked_stats[i]['queueType'] == 'RANKED_SOLO_5x5': # If the user has a rank
                rank = f"{ranked_stats[i]['tier'].capitalize()} {ranked_stats[i]['rank']}"
                db.update("rank", rank, rowid) # Updates the users rank in database
                return clear_terminal(), print("Ranked refreshed!"), input("Press ANY button to continue...")
                
    # If user has no soloQ Rank
    rank = "Unranked"
    db.update("rank", rank, rowid) # Updates the users rank in database
    return clear_terminal(), print("Ranked refreshed!"), input("Press ANY button to continue...")