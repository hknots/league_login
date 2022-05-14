import os
from dotenv import load_dotenv
import requests
from database import Database
from menu import clear_terminal
import time

db = Database()

def refresh_ranks():
    load_dotenv()
    api = os.getenv("API")
    rowid = db.rowids
    ign = db.igns
    server = db.servers

    if not valid_api(ign[0], server[0], api): # Checks if API is valid
        clear_terminal()
        print("Invalid API\nGet your personal API at https://developer.riotgames.com/ if you want to use this function.")
        print("If you got an API key, paste it below.")

        new_api = input("API: ") # Lets user paste new API
        with open('.env', 'w') as env:
            env.write(f"API={new_api}")
        return clear_terminal(), print("Returning to main menu..."), time.sleep(1)

    for i in range(len(ign)):
        user = requests.get(f"https://{server[i]}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign[i]}?api_key={api}").json()
        ranked_stats = requests.get(f"https://{server[i]}.api.riotgames.com/lol/league/v4/entries/by-summoner/{user['id']}?api_key={api}").json()

        if len(ranked_stats) > 0:
            for x in range(len(ranked_stats)):
                if ranked_stats[x]['queueType'] == 'RANKED_SOLO_5x5': # If the user has a rank
                    rank = f"{ranked_stats[x]['tier'].capitalize()} {ranked_stats[x]['rank']}" # f.ex "Diamond I"
                    db.update("rank", rank, rowid[i]) # Updates the users rank in database
    
    return clear_terminal(), print("Rankings updated!"), time.sleep(1)

def valid_api(ign, server, api):
    user = requests.get(f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}?api_key={api}").json()
    try:
        if user['status']['status_code'] == 403: # If invalid API
            return False
    except KeyError: # If api valid
        return True