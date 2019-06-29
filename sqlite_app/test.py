import sqlite3

# connection address to the db
URI = 'src/data.db'
connection = sqlite3.connect(URI)

cursor = connection.cursor()

# query to create a table
create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'user1', '1234')
insert_query = "INSERT INTO users VALUES(?, ?, ?)"  # insert query

cursor.execute(insert_query, user)
users = [
    (2, 'user2', '1234'),
    (3, 'user3', '1234')
    ]


# execute many queries
cursor.executemany(insert_query, users)

# select query
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
