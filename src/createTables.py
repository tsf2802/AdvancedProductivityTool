import psycopg2
import csv

def main():
    conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
    cursor = conn.cursor()
    #createTask(cursor)
    createBanner(cursor)
    createCharachters(cursor)
    conn.commit()
    conn.close() 

def createTask(dbcursor):
    dbcursor.execute("DROP TABLE IF EXISTS genshin.public.tasks ")
    dbcursor.execute("CREATE TABLE genshin.public.tasks (task TEXT, charachter TEXT, goal TEXT, selected INTEGER )")
    dbcursor.execute("INSERT INTO genshin.public.test VALUES (%s,%s)",(2,"random"))
    dbcursor.execute("SELECT * FROM genshin.public.test ")
    
def createBanner(dbcursor):
    dbcursor.execute("DROP TABLE IF EXISTS genshin.public.banner")
    dbcursor.execute("CREATE TABLE genshin.public.banner (id SERIAL PRIMARY KEY , fivestar TEXT, fourstarone TEXT, fourstartwo TEXT, fourstarthree TEXT,datestart DATE,dateend DATE)")
    csv_data = csv.reader(open('data\\banners.csv'))
    next(csv_data)
    for row in csv_data:
         dbcursor.execute("INSERT INTO genshin.public.banner (id,fivestar,fourstarone,fourstartwo,fourstarthree,datestart,dateend) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)", row) 
    print("Banner Table Created")

def createCharachters(dbcursor):
    dbcursor.execute("DROP TABLE IF EXISTS genshin.public.charachters")
    dbcursor.execute("CREATE TABLE genshin.public.charachters (name TEXT, star INTEGER)")
    dbcursor.execute("SELECT DISTINCT fivestar FROM genshin.public.banner")
    fivestars= dbcursor.fetchall()
    for row in fivestars:
        dbcursor.execute("INSERT INTO genshin.public.charachters (name, star) VALUES (%s,%s)",(row[0],5))
    #Exception 5 Star Charachters due to no banner
    exceptionList = ['Diluc','Jean','Mona','QiQi','Aloy']
    for row in exceptionList:
        dbcursor.execute("INSERT INTO genshin.public.charachters (name, star) VALUES (%s,%s)",(row,5))
    dbcursor.execute("SELECT DISTINCT fourstarone,fourstartwo,fourstarthree FROM genshin.public.banner")
    dbcursor.execute("SELECT fourstarone FROM genshin.public.banner WHERE fourstarone IS NOT NULL UNION SELECT fourstartwo FROM genshin.public.banner WHERE fourstartwo IS NOT NULL UNION SELECT fourstarthree FROM genshin.public.banner WHERE fourstarthree IS NOT NULL")
    fourstars= dbcursor.fetchall()
    for row in fourstars:
        dbcursor.execute("INSERT INTO genshin.public.charachters (name, star) VALUES (%s,%s)",(row[0],4))
    #Exception 4 Star Charachters due to no banner
    exceptionFourStar= ['Amber','Kaeya','Lisa']
    for row in exceptionFourStar:
        dbcursor.execute("INSERT INTO genshin.public.charachters (name, star) VALUES (%s,%s)",(row,4))
    print('Charachter table created')
    
if __name__ == "__main__":
    main()