from window import Window
from database import Database
from menu import Menu, clear_terminal
from riot_api import refresh_ranks

if __name__ == "__main__":
    db = Database()
    window = Window()
    menu = Menu()
    window.look_for_login() # Looks for Riot login, attempts to launch and move it ontop
    window.move_ontop(window.window_name) # Moves menu on top
    
    menu_loop = True
    while menu_loop:
        menu.main()
        select = input("Number: ")
        while select not in [str(i) for i in range(1, len(menu.options)+1)]: # f.ex ['1', '2', '3']
            menu.main()
            select = input("Number: ")

        if select == '1': # Logs in
            menu.display_users()
            login_select = input("Num: ")
            ids = db.ids
            while login_select not in (ids + ['0']):
                menu.display_users()
                login_select = input("Num: ")
            if login_select in ids:
                menu_loop = False
                login_info = db.login_info(login_select)
                window.login(login_info[0], login_info[1])
                
        elif select == '2': # Add user to database
            menu.add_user()

        elif select == '3': # Removes user from database
            menu.remove_user()

        elif select == '4': # Refresh ranks
            refresh_ranks()

        elif select == '5': # Exits menu
            menu_loop = False