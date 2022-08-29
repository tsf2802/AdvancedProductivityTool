import plotly.express as px
import psycopg2
import plotly.figure_factory as pff
import pandas as pd
def main():
    """
    plotly help:
    https://plotly.com/python/gantt/
    """
    conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
    dbcursor = conn.cursor()
    dbcursor.execute("SELECT * FROM genshin.public.banner")
    banners = dbcursor.fetchall()
    df = []
    for i in banners:
        
        listadd = dict(Task=i[1], Start=i[5], Finish=i[6], Charachter= i[1])
        listaddtwo = dict(Task=i[2], Start=i[5], Finish=i[6], Charachter= i[2])
        listaddthree = dict(Task=i[3], Start=i[5], Finish=i[6], Charachter= i[3])
        listaddfour = dict(Task=i[4], Start=i[5], Finish=i[6], Charachter= i[4])
        df.append(listadd)
        df.append(listaddtwo)
        df.append(listaddthree)
        df.append(listaddfour)

    print(dbcursor.fetchall())
    dbcursor.execute
    dbcursor.close()
    conn.commit()
    conn.close()
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Charachter", color="Charachter")
    fig.show()
    #future goals, chibi emoji on left hand axis 
    #https://stackoverflow.com/questions/69680720/plotly-replace-x-label-with-image, use kaggle?
    #color code charachters with element without messing up the order
    

if __name__ == "__main__":
    main()