import sqlite3

from h11 import Data

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.cursor = self.conn.cursor()
    
    @property
    def get_column_widths(self):
        self.cursor.execute("SELECT username, ign, rank FROM users")
        rows = self.cursor.fetchall()
        column_widths = []
        for i in range(len(self.cursor.description)):
            column_widths.append(len(self.cursor.description[i][0])) # Sets Default value to the length of the column title
            for row in rows: # Checks all rows for the biggest length of each column
                if isinstance(row[i], str):
                    if len(row[i]) > column_widths[i]:
                        column_widths[i] = len(row[i])
        return column_widths # Returns list of column widths
    
    @property
    def get_rows(self):
        self.cursor.execute("SELECT username, ign, rank FROM users")
        rows = self.cursor.fetchall()
        for row in rows:
            row = list(row)
            for i in range(len(row)):
                if isinstance(row[i], type(None)):
                    row[i] = "XD"
        return rows
    
    @property
    def users(self):
        self.cursor.execute("SELECT username, ign, rank FROM users")
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            row = list(row)
            for i in range(len(row)):
                if isinstance(row[i], type(None)):
                    row[i] = "None"
            row = tuple(row)
            users.append(row)
        return users

    @property
    def rowids(self):
        self.cursor.execute("SELECT rowid FROM users")
        rows = self.cursor.fetchall()
        rowids = []
        for row in rows:
            rowids.append(str(row[0]))
        return rowids
    
    @property
    def igns(self):
        self.cursor.execute("SELECT ign FROM users")
        rows = self.cursor.fetchall()
        igns = []
        for row in rows:
            igns.append(row[0])
        return igns

    @property
    def servers(self):
        self.cursor.execute("SELECT server FROM users")
        rows = self.cursor.fetchall()
        servers = []
        for row in rows:
            servers.append(row[0])
        return servers

    def update(self, column, value, rowid):
        self.execute_commit(f"UPDATE users SET {column}='{value}' WHERE Rowid='{rowid}'")

    def add(self, username, password, ign, server):
        self.execute_commit(f"INSERT INTO users (username, password, ign, server) VALUES ('{username}', '{password}', '{ign}', '{server}')")
    
    def remove(self, rowid):
        self.execute_commit(f"DELETE FROM users WHERE Rowid='{rowid}'")
    
    def execute(self, sql):
        self.cursor.execute(f"{sql}")
    
    def execute_commit(self, sql):
        self.cursor.execute(f"{sql}")
        self.conn.commit()
    
    def login_info(self, rowid):
        self.cursor.execute(f"SELECT username, password from users WHERE Rowid={int(rowid)}")
        rows = self.cursor.fetchall()
        login_info = []
        login_info.append(rows[0][0])
        login_info.append(rows[0][1])
        return login_info

db = Database()
db.rowids