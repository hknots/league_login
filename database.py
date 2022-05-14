import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.try_make_table

    @property
    def try_make_table(self):
        try:
            # Attempts to make table 'users'
            self.cursor.execute("CREATE TABLE users (id integer, username text, password text, ign text, rank text, server text)")
            self.cursor.execute("CREATE TABLE lolpath (path text)")
            self.cursor.execute("INSERT INTO lolpath (path) VALUES ('C:/Riot Games/Riot Client/')")
            self.cursor.execute("CREATE TABLE riotapi (api text)")
            self.cursor.execute("INSERT INTO riotapi (api) VALUES ('None')")
            self.conn.commit()
        except:
            pass
    
    @property
    def get_path(self):
        self.cursor.execute("SELECT path FROM lolpath")
        row = self.cursor.fetchall()
        return row[0][0] # returns "C:/Riot Games/Riot Client/"
    
    @property
    def get_column_widths(self):
        self.cursor.execute("SELECT ign, rank, server FROM users")
        rows = self.cursor.fetchall() # Fetches all rows from sql string
        column_widths = []
        for i in range(len(self.cursor.description)): # For every column selected
            column_widths.append(len(self.cursor.description[i][0])) # Sets Default value to the length of the column title
            for row in rows: # Checks all rows for the biggest length of each column
                if len(row[i]) > column_widths[i]:
                    column_widths[i] = len(row[i])
        return column_widths # Returns list of column widths
    
    @property
    def api(self):
        self.cursor.execute("SELECT api FROM riotapi")
        row = self.cursor.fetchall()
        return row[0][0]

    @property
    def ids(self):
        self.cursor.execute("SELECT id FROM users")
        rows = self.cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(str(row[0]))
        return ids # Returns ids strings as a list
    
    @property
    def igns(self):
        self.cursor.execute("SELECT ign FROM users")
        rows = self.cursor.fetchall()
        igns = []
        for row in rows:
            igns.append(row[0])
        return igns # Returns igns as a list
    
    @property
    def ranks(self):
        self.cursor.execute("SELECT rank FROM users")
        rows = self.cursor.fetchall()
        ranks = []
        for row in rows:
            ranks.append(row[0])
        return ranks # Returns ranks as a list

    @property
    def servers(self):
        self.cursor.execute("SELECT server FROM users")
        rows = self.cursor.fetchall()
        servers = []
        for row in rows:
            servers.append(row[0])
        return servers # Returns servers as a list

    def update(self, column, value, id):
        self.execute_commit(f"UPDATE users SET {column}='{value}' WHERE id='{id}'")

    def add(self, username, password, ign, server):
        if len(self.igns) < 1:
            self.execute_commit(f"INSERT INTO users (id, username, password, ign, rank, server) VALUES (1, '{username}', '{password}', '{ign}', 'Unranked', '{server}')")
        else:
            ids = [int(i) for i in self.ids]
            id = max(ids) + 1
            self.execute_commit(f"INSERT INTO users (id, username, password, ign, rank, server) VALUES ({id}, '{username}', '{password}', '{ign}', 'Unranked', '{server}')")
    
    def remove(self, id):
        self.execute_commit(f"DELETE FROM users WHERE id={id}")
        self.execute_commit(f"UPDATE users SET id=(id - 1) WHERE id > {id}")
    
    def execute_commit(self, sql): # Executes and commits it to database (saves it)
        self.cursor.execute(f"{sql}")
        self.conn.commit()
    
    def login_info(self, id):
        self.cursor.execute(f"SELECT username, password from users WHERE id={int(id)}")
        rows = self.cursor.fetchall()
        login_info = []
        login_info.append(rows[0][0])
        login_info.append(rows[0][1])
        return login_info # Returns username and password for login ['bob', 'superpassword']