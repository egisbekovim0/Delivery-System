import sqlite3

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

cursor.execute("""
    create table if not exists shipment (
        id integer primary key, 
        context text, 
        weight real, 
        status text)
""")

# cursor.execute("drop table shipment")
# connection.commit()

# cursor.execute("""
#     insert into shipment
#     values (12702, 'palm boxes', 9.5, 'placed')
#                """)
# connection.commit()

# cursor.execute("""
#     select * from shipment
#                where id = 12701
#                """)

id = 12701
status = "in_transit"

cursor.execute("""
    update shipment set status = ?
    where id = ?               
""", (status, id))
connection.commit()

# cursor.execute("""
#     delete from shipment
#                where id = 12702
#                """)
# connection.commit()

# result = cursor.fetchall()
# print(result)

connection.close()