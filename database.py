from sqlite3 import connect

class Database:
    def __init__(self):
        self.conn = connect('database.db')
        self.cursor = self.conn.cursor()
        self.try_make_table


    @property
    def try_make_table(self):
        try:
            # Attempts to make and insert all tables and their default data
            self.cursor.execute("CREATE TABLE users (id integer, username text, password text, ign text, rank text, server text)")
            self.cursor.execute("CREATE TABLE lolpath (path text)")
            self.cursor.execute("INSERT INTO lolpath (path) VALUES ('C:/Riot Games/Riot Client/')")
            self.cursor.execute("CREATE TABLE riotapi (api text)")
            self.cursor.execute("INSERT INTO riotapi (api) VALUES ('None')")
            self.conn.commit()
        except:
            pass
    

    @property
    def users_exist(self):
        return len(self.get_igns) > 0
    

    def id_exist(self, id):
        return str(id) in self.get_ids
    

    def get_user(self, id=0):
        if id == 0: # If id isnt specified
            self.cursor.execute("SELECT id, username, password, ign, rank, server FROM users ORDER BY id ASC")
        else:
            if self.id_exist(id): # If id exists
                self.cursor.execute(f"SELECT id, username, password, ign, rank, server FROM users WHERE id = {id}")
            else:
                return
        
        rows = self.cursor.fetchall()
        user = {"id": [], "username": [], "password": [], "ign": [], "rank": [], "server": []}

        for i, key in enumerate(user):
            for row in rows:
                user[key].append(row[i])
        return user


    @property
    def get_igns(self):
        self.cursor.execute(f"SELECT ign FROM users ORDER BY id ASC")
        rows = self.cursor.fetchall()
        data = []
        for row in rows:
            data.append(row[0])
        return data
    

    @property
    def get_ids(self):
        self.cursor.execute(f"SELECT id FROM users ORDER BY id ASC")
        rows = self.cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(str(row[0])) # turns id int -> str
        return ids
    

    @property
    def get_api(self):
        self.cursor.execute(f"SELECT api FROM riotapi")
        api = self.cursor.fetchall()[0][0]
        return api
    

    @property
    def get_path(self):
        self.cursor.execute("SELECT path FROM lolpath")
        path = self.cursor.fetchall()[0][0]
        return path # returns "C:/Riot Games/Riot Client/"  


    @property
    def get_columns(self):
        self.cursor.execute(f"SELECT * FROM users ORDER BY id ASC")
        rows = self.cursor.description
        columns = []
        for row in rows:
            columns.append(str(row[0])) # turns id int -> str
        return columns
    
    
    def get_column_width(self, id=0):
        if id == 0: # If id isnt specified
            self.cursor.execute("SELECT username, password, ign, rank, server FROM users ORDER BY id ASC")
        else:
            if self.id_exist(id):
                self.cursor.execute(f"SELECT username, password, ign, rank, server FROM users WHERE id = {id}")
            else:
                return
        
        rows = self.cursor.fetchall()
        column_width = {"username": '', "password": '', "ign": '', "rank": '', "server": ''}
        for i, key in enumerate(column_width):
            column_width[key] = len(self.cursor.description[i][0]) # Sets Default value to the length of the column title
            for row in rows:
                if len(row[i]) > column_width[key]:
                    column_width[key] = len(row[i])
        return column_width


    def add_user(self, username, password, ign, server):
        if self.users_exist: # If there is more than 0 users in the database
            ids = [int(i) for i in self.get_ids]
            id = max(ids) + 1
            self.execute_commit(f"INSERT INTO users (id, username, password, ign, rank, server) VALUES ({id}, '{username}', '{password}', '{ign}', 'Unranked', '{server}')")
        else:
            self.execute_commit(f"INSERT INTO users (id, username, password, ign, rank, server) VALUES (1, '{username}', '{password}', '{ign}', 'Unranked', '{server}')")


    def remove(self, id):
        self.execute_commit(f"DELETE FROM users WHERE id={id}")
        self.execute_commit(f"UPDATE users SET id=(id - 1) WHERE id > {id}")
    

    def update_user(self, column, change, id):
        self.execute_commit(f"UPDATE users SET {column}='{change}' WHERE id={id}")
    

    def update_id(self, current_id, change_id):
        if change_id in self.get_ids:
            self.cursor.execute(f"UPDATE users SET id=0 WHERE id={current_id}") # Temporary value
            self.cursor.execute(f"UPDATE users SET id={current_id} WHERE id ={change_id}")
            self.cursor.execute(f"UPDATE users SET id={change_id} WHERE id=0")
            self.conn.commit()


    def update_api(self, api):
        self.execute_commit(f"UPDATE riotapi SET api='{api}'")


    def execute_commit(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

