import psycopg2
import unittest
class TestStringMethods(unittest.TestCase):
    def testPGQuery(self):
        conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
        dbcursor = conn.cursor()
        dbcursor.execute("DROP TABLE IF EXISTS genshin.public.test ")
        dbcursor.execute("CREATE TABLE genshin.public.test (initial INTEGER, second TEXT)")
        dbcursor.execute("INSERT INTO genshin.public.test VALUES (%s,%s)",(2,"random"))
        dbcursor.execute("SELECT * FROM genshin.public.test ")
        self.assertEqual(dbcursor.fetchall(), [(2, 'random')])
        dbcursor.close()
        conn.commit()
        conn.close()

    
if __name__ == "__main__":
    unittest.main()