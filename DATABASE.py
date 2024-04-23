import sqlite3

sqliteConnection = sqlite3.connect('DB.db')

# If sqlite3 makes a connection with python
# program then it will print "Connected to SQLite"
# Otherwise it will show errors
print("Connected to SQLite")

# Getting all tables from sqlite_master
query = f"""SELECT guide_name, rank, hero, position, likes
                    FROM Items_guides"""
cursor = sqliteConnection.cursor()
response = cursor.execute(query).fetchall()
sqliteConnection.commit()
cursor.close()

print(f'Сборка: {response[0][0]}; Ранг: {response[0][1]}; Герой: {response[0][2]}; Позиция: {response[0][3]}; Понравилось: {response[0][4]}')

query = f"""SELECT likes FROM Items_guides
            WHERE guide_name = '{'gg'}'"""
cursor = sqliteConnection.cursor()
likes = cursor.execute(query).fetchone()[0] + 1
query = f"""UPDATE Items_guides
            SET likes = {likes}
            WHERE guide_name = '{'gg'}'"""
cursor.execute(query)
sqliteConnection.commit()
cursor.close()

name = 'gg'
query = f"""SELECT guide_name, rank, hero, position, items, likes
            FROM Items_guides
            WHERE guide_name = '{name}'"""
cursor = sqliteConnection.cursor()
response = cursor.execute(query).fetchone()
sqliteConnection.commit()
cursor.close()
print(f"Название: {response[0]}\n"
      f"Ранг:  {response[1]}\n"
      f"Герой: {response[2]}\n"
      f"Позиции: {response[3]}\n\n"
      f"ПРЕДМЕТЫ: {response[4]}\n\n"
      f"Понравилось: {response[5]}\n")