import sqlite3 as sql

db_uri = "main_db.db"

def createDB():
    conn = sql.connect(db_uri)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE users (
                   ID int PRIMARY KEY,
                   email varchar(120) NOT NULL,
                   password varchar(120) NOT NULL
                    );
    """)

def addValues():
    conn = sql.connect(db_uri)
    cursor = conn.cursor()
    data = [(0,"1@gmail.com","asdf")]
    cursor.executemany("""INSERT INTO users VALUES (?, ?, ?)""",data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()
    addValues()
