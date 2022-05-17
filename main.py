from menu import Menu
from window import Window

if __name__ == "__main__":
    menu = Menu()
    window = Window()

    # Adjust menu
    window.adjust
    window.look_for_login()
    window.move_top(window.name)

    # Menu
    main_menu = True
    while main_menu:
        menu.main()
        nav = input("Number: ")

        if nav == str(menu.options.index('Login') + 1):
            menu.login()

        elif nav == str(menu.options.index('Add user') + 1):
            menu.add_user() # Finished
        
        elif nav == str(menu.options.index('Remove user') + 1):
            menu.remove_user() # Finished
        
        elif nav == str(menu.options.index('Modify user') + 1):
            menu.modify_user()
        
        elif nav == str(menu.options.index('Update rank') + 1):
            menu.update_rank()
        
        elif nav == str(menu.options.index('Exit') + 1):
            main_menu = False
        