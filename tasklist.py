import pandas as pd
import psycopg2
def main():
    conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
    cursor = conn.cursor()
    close = False
    """main function for the adding/removing/prioritizing of tasks"""
    options = ['add','remove','priority','close','view'] 
    while(close == False):
        sampletask = ''
        while sampletask not in options:
            sampletask = input("pick: add, remove, priority, close, view\n")
        print(sampletask + " chosen")
        if(sampletask == 'add'):
            addingtask = input("what task are you adding?: ")
            addItem(addingtask,cursor)
            conn.commit()
        if(sampletask == 'close'):
            close == True   
        if(sampletask== 'remove'):
            cursor.execute("SELECT id,task from genshin.public.tasks")
            print("current tasks:")
            for i in cursor.fetchall() :
                print("id number:"+str(i[0])+", task:"+str(i[1]))
            getid = input("what task do you want to delete? (enter id number):  ")
            removeItem(getid,cursor)
            conn.commit()
        if(sampletask== 'view'):
             cursor.execute("SELECT task, priority from genshin.public.tasks")
             for i in cursor.fetchall() :
                printpriority = ''
                prioritypull =i[1]
                if prioritypull == 0:
                    printpriority = 'Low priority'
                else:
                    printpriority = 'High priority'
                print(printpriority+" task: "+i[0])
        if( sampletask == 'priority'):
            setPriority(cursor)
            conn.commit()
    conn.commit()
    conn.close() 

def addItem (userInput,dbcursor):
    dbcursor.execute("SELECT name FROM genshin.public.charachters")
    tupledcharName =  dbcursor.fetchall()
    clean=[]
    foundchara = ""
    for i in tupledcharName:
        clean.append(i[0])
    lower = userInput.lower()
    for chara in clean:
        if chara.lower() in lower.split():
            foundchara = chara
    print("found "+ foundchara)
    dbcursor.execute("INSERT INTO genshin.public.tasks (id,task,charachter,priority) VALUES (DEFAULT, %s,%s,%s)",(userInput,foundchara,0))
    
def removeItem(removeId, dbcursor):
    dbcursor.execute("DELETE FROM genshin.public.tasks WHERE id= %s",(removeId,))

def setPriority(dbcursor):
    dbcursor.execute("SELECT id, task, priority from genshin.public.tasks")
    for i in dbcursor.fetchall() :
        printpriority = ''
        prioritypull =i[2]
        if prioritypull == 0:
            printpriority = 'Low priority'
        else:
            printpriority = 'High priority'
        print("id:"+str(i[0])+", "+printpriority+" task: "+i[1])
        uin= input("Select a task to change priority: ")
        dbcursor.execute("SELECT priority from genshin.public.tasks WHERE id =%s",(uin,))
        gotprior = dbcursor.fetchall()
        if gotprior[0][0] == 0:
            dbcursor.execute("UPDATE genshin.public.tasks SET priority = %s WHERE id = %s ",(1,uin))
        else:
            dbcursor.execute("UPDATE genshin.public.tasks SET priority = %s WHERE id = %s ",(0,uin))



if __name__ == "__main__":
    main()