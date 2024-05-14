import sqlite3

connection = sqlite3.connect('telegram_bot.db')

cursor = connection.cursor()

def main():
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS foydalanuvchilar_soni(
        username TEXT,
        first_name TEXT,
        last_name TEXT
)
"""
)    
connection.commit()

def create_user(*args):
    """
    args - bu funksiya qabul qilayotgan foydalanuvchi ma'lumotlar to'plami
    """
    sql = """INSERT INTO foydalanuvchilar_soni(username,first_name,last_name)
            VALUES(?,?,?)"""
    cursor.execute(sql,args)
    connection.commit()

def info_users():
    cursor.execute("SELECT username,first_name,last_name FROM foydalanuvchilar_soni")
    return cursor.fetchall()

def info_usernames():
    cursor.execute("SELECT username FROM foydalanuvchilar_soni")
    return [row[0] for row in cursor.fetchall()]
    
    

if __name__ == "__main__":
    main()