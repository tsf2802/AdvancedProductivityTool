#importing packages 
from  tkinter import * 
import tkinter.messagebox
from time import strftime
from tasklist import *
conn = psycopg2.connect(host="localhost",database="genshin",user="postgres",password="dbpass")
cursor = conn.cursor()
listindex= []
window=Tk()
window.geometry("1200x800")
window.resizable(0,0)
window.title("Genshin To-Do List")
bg = PhotoImage(file = "images\inazumabg.png")
label1 = Label( window, image = bg)
label1.place(x = 0, y = 0)
frame_task=Frame(window)
frame_task.pack(side=LEFT, padx= 15)
listbox_task=Listbox(frame_task,bg="white",fg="black",height=25,width=80,font = "Helvetica")  
scrollbar_task=Scrollbar(frame_task)
scrollbar_task.pack(side=tkinter.RIGHT,fill=tkinter.Y)
listbox_task.config(yscrollcommand=scrollbar_task.set)
scrollbar_task.config(command=listbox_task.yview)
timelabel=Label(window,fg= '#d8d0bd', font="Arial 51",bg='#4987a6')
timelabel.place(x=15,y=140,anchor ='sw')

def main():
    loaditems()
    time_string = strftime('%H:%M %p  %A') # time format 
    timelabel.config(text=time_string)

    buttonframes = Frame(window)
    listbox_task.pack(side=tkinter.LEFT)
    entry_button=Button(buttonframes,text="Add task",width=50,command=entertask)
    entry_button.pack(pady=3)
    delete_button=Button(buttonframes,text="Delete selected task",width=50,command=deletetask)
    delete_button.pack(pady=3)
    mark_button=Button(buttonframes,text="Switch priority ",width=50,command=setPriority)
    mark_button.pack(pady=3)
    buttonframes.pack(side = RIGHT, padx = 15)
    timer()
    window.mainloop()

def timer():
    timer_tick = strftime('%H:%M %p  %A')
    timelabel.configure(text=timer_tick)
    timelabel.after(1000, timer)

def entertask():
    #A new window to pop up to take input
    input_text=""
    def add():
        input_text=entry_task.get(1.0, "end-1c")
        if input_text=="":
            tkinter.messagebox.showwarning(title="Warning!",message="Please Enter some Text")
        else:
            listbox_task.insert(END,input_text+ " [Low priority]")
            addItem(input_text,cursor)
            conn.commit()
            cursor.execute("SELECT id from genshin.public.tasks WHERE task = %s",(input_text,))
            fetched= cursor.fetchall()
            listindex.append(fetched[0][0])
            print(listindex)
            root1.destroy()
    root1=Tk()
    root1.title("Add task")
    entry_task=Text(root1,width=40,height=4)
    entry_task.pack()
    button_temp=Button(root1,text="Add task",command=add)
    button_temp.pack()
    root1.mainloop()
    
#function to facilitate the delete task from the Listbox
def loaditems():
    cursor.execute("SELECT task, priority,id from genshin.public.tasks")
    for i in cursor.fetchall() :
        printpriority = ''
        prioritypull =i[1]
        if prioritypull == 0:
            printpriority = ' [Low priority]'
        else:
            printpriority = ' [High priority]'
        listbox_task.insert(END,i[0]+ printpriority)
        
        listindex.append(i[2])
        


def deletetask():
    #selects the selected item and then deletes it 
    selected=listbox_task.curselection()
    removeItem(listindex[selected[0]],cursor)
    listindex.pop(selected[0])
    listbox_task.delete(selected[0])
    conn.commit()

#Executes this to mark completed 
def setPriority():
    selected=listbox_task.curselection()
    temp=selected[0]
    flipPriority(cursor, listindex[temp])
    cursor.execute("SELECT task, priority from genshin.public.tasks WHERE id= %s",(listindex[temp],))
    returned = cursor.fetchall()
    first = returned[0]
    secondword= ""
    if(first[1] == 1):
        secondword = "[High Priority]"
    else:
        secondword = "[Low Priority]"
    temp_marked =  str(first[0])+" "+secondword
    #delete it then insert it 
    listbox_task.delete(temp)
    listbox_task.insert(temp,temp_marked)
    conn.commit()


if __name__ == "__main__":
    main()