import requests
from database import Database
from menu import clear_terminal
import time

def refresh_ranks():
    db = Database()

    api = db.api
    rowid = db.rowids
    ign = db.igns
    server = db.servers

    if len(ign) < 1:
        return clear_terminal(), print("There must be at least 1 user in the database to update rankings."), input("Press ENTER to continue...")

    print(ign[0], server[0], api)
    input()
    if not valid_api(ign[0], server[0], api): # Checks if API is valid
        clear_terminal()
        print("Invalid API\nGet your personal API at https://developer.riotgames.com/ if you want to use this function.")
        confirm = input("Want to add new API? (Yes/No): ").capitalize()
        confirm = confirm in ("Yes", "Ye", "Y")
        if confirm:
            clear_terminal()
            print("Get your own personal API from https://developer.riotgames.com/")
            new_api = input("API: ") # Lets user paste new API
            db.execute_commit(f"UPDATE riotapi SET api='{new_api}'")
            return clear_terminal(), print("Trying again..."), time.sleep(1), refresh_ranks() # Go back and try API again
        else:
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