# league_login
A login menu for League of Legends.
It uses Riots API to fetch Ranked statistics about each user.
That way, you'll know what rank the account is before you sign onto it.
You can add or remove as many accounts as you like, its all stored on a local database using sqlite3.

Note if you want to refresh rankings you need to create a .env file in the directory of the project.
Inside of .env you'll need to write API=YOURAPIKEY
