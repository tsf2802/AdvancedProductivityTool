import psycopg2
import csv
#CreateTables is a python file that initializes all the required tables for the program to run.
#This is required to setup the databse for the other components of the program.
#It only has to be ran once and running it again will refresh all the previous data.
def main():
    confirmation = input("DO YOU WANT TO REALLY CREATE/REFRESH YOUR DATABASE? type 'yes' if you do.")
    if(confirmation == 'yes'):
        conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
        cursor = conn.cursor()
        createTask(cursor)
        createBanner(cursor)
        createCharachters(cursor) #the banner table must be created before running.
        conn.commit()
        conn.close() 

def createTask(dbcursor):
    #creates a table that user can add/delete tasks
    dbcursor.execute("DROP TABLE IF EXISTS genshin.public.tasks ")
    dbcursor.execute("CREATE TABLE genshin.public.tasks (id SERIAL PRIMARY KEY , task TEXT, charachter TEXT, priority INTEGER )")
    print("Task Table Created")

def createBanner(dbcursor):
    #creates a new table of the banners based on a csv it reads
    dbcursor.execute("DROP TABLE IF EXISTS genshin.public.banner")
    dbcursor.execute("CREATE TABLE genshin.public.banner (id SERIAL PRIMARY KEY , fivestar TEXT, fourstarone TEXT, fourstartwo TEXT, fourstarthree TEXT,datestart DATE,dateend DATE)")
    csv_data = csv.reader(open('data\\banners.csv'))
    next(csv_data)
    for row in csv_data:
         dbcursor.execute("INSERT INTO genshin.public.banner (id,fivestar,fourstarone,fourstartwo,fourstarthree,datestart,dateend) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)", row) 
    print("Banner Table Created")

def createCharachters(dbcursor):
    #creates a new tables of all the 4/5 star charachters based on the banner information
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