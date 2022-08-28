import psycopg2

def main():
    createTables()

def createTables():
    conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
    dbcursor = conn.cursor()
    dbcursor.execute("DROP TABLE IF EXISTS genshin.public.tasks ")

    dbcursor.execute("CREATE TABLE genshin.public.tasks (task TEXT, charachter TEXT, goal TEXT, selected INTEGER )")
    dbcursor.execute("INSERT INTO genshin.public.test VALUES (%s,%s)",(2,"random"))
    dbcursor.execute("SELECT * FROM genshin.public.test ")
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()