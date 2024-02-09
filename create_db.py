import sqlite3
def create_db():
    con=sqlite3.connect(database=r'CR.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT, contact TEXT, dob TEXT, doj TEXT, pass TEXT, utype TEXT, address TEXT, salary TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, contact TEXT, desc TEXT)")
    con.commit()


    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, Category TEXT, Supplier TEXT, name TEXT, price TEXT, qty TEXT, status TEXT)")
    con.commit()




create_db()

 