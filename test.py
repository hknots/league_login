from database import Database

db = Database()
db.execute("ALTER TABLE users ADD server text")
db.conn.commit()