import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="220507",
    port="5432"
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS PhoneBook;")

cur.execute("""CREATE TABLE IF NOT EXISTS Phonebook(
            surname VARCHAR(255) ,
            name VARCHAR(255),
            number VARCHAR(50)
            );  
            """)
conn.commit()

def update(sn, mode, newv):
    query = f"UPDATE PhoneBook SET {mode} = %s WHERE surname = %s"
    cur.execute(query, (newv, sn))
    conn.commit()

def delete(sn):
    cur.execute("DELETE FROM PhoneBook WHERE surname = %s", (sn,))
    conn.commit()
def delete_by_number(phone):
    cur.execute("DELETE FROM PhoneBook WHERE number = %s", (phone,))
    conn.commit()
# INSERTING DATA--------------------------

mode = "enter"
while True:
    print("Type 'enter' if you want to add more data and type 'stop' to break")
    mode = input()
    if mode == "stop":
        break
    mytuple = []
    print("enter surname:")
    mytuple.append(input())
    print("enter name:")
    mytuple.append(input())
    print("enter number:")
    mytuple.append(input())
    mytuple = tuple(mytuple)
    cur.execute("INSERT INTO PhoneBook (surname, name, number) VALUES (%s, %s, %s)", mytuple)
    conn.commit()
while True:
    print("Want to insert data from csv file? yes/no:")
    mode = input()
    if mode == "no":
        break
    print("enter the name of the file")
    mode = input()
    with open(mode + '.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook VALUES (%s,%s,%s)", row)
            conn.commit()

# UPDATING DATA---------
while True:
    print("Type 'update' to update some data or 'stop' to break")
    mode = input()
    if mode == "stop":
        break
    cur.execute("""SELECT * FROM PhoneBook""")
    print(cur.fetchall())
    print("Enter surname")
    idtochange = input()
    print("What you want to change? name/number")
    mode = input()
    print("Enter new name/number")
    newvalue = input()
    update(idtochange, mode, newvalue)

# DELETING DATA-----------
while True:
    print("want to delete some data? yes/no")
    mode = input()
    if mode == "no":
        break
    cur.execute("""SELECT * FROM PhoneBook""")
    print(cur.fetchall())
    print("Enter surname/phone")
    idtodelete = input()
    delete(idtodelete)
    conn.commit()
    
# QUERYING DATA WITH FILTERS ---------
while True:
    print("Do you want to filter and view specific data? yes/no")
    mode = input()
    if mode == "no":
        break
    print("Enter filter:")
    filter = input()
    try:
        cur.execute(f"SELECT * FROM PhoneBook WHERE {filter}")
        results = cur.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No results found.")
    except Exception as e:
        print("Error in filter query:", e)
    conn.rollback()
cur.close()
conn.close()