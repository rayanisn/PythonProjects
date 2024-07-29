# Liste des imports
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from  tkinter import ttk

# Déclaration des variables (ERROR est celle pouvant changer)
ERROR = 5

INDEX = 1
NAME = 2
X = 5
Y = 6
data_dead = ""
data_live = ""


# Déclaration des fonctions
def helpMe():
    
    helper = tk.Toplevel(parent)
    helper.title("Helper")
    
    canvas = tk.Canvas(helper,bg = 'white', width= 750, height= 500)

    Fact = """\nEoL - End of Life Software\n_____________________\n\nThis software is intended to facilitate image analysis while using Fiji.\nSpecifically, it detects cells reaching the end of their live by processing the file of living cells with that of dead cells.\n\n
     1.    Search for the living cells file by clicking the associated button.
            Once this has been done, the button should turn green.\n
     2.    Do the same for the dead cells file.\n
     3.    The spinbox in the middle specifies a value in pixel. This value determines the "view" area 
            of each cell. If one cell can "see" another, then they will count as stacked and therefore 
            will be identified as end-of-life cells. 
            You can change this value at will but the best one is 5.
            Keep in mind that the higher the value is, the lesser the script will be efficient.\n
     4.    Once both buttons (dead and living) have turned green and you have set the desired spinbox 
            value, you can click Process to generate the table presenting end-of-life detected cells.
    """
    canvas.create_text(380, 220, text=Fact, fill="black", font=('Times New Roman','12'))
    canvas.pack()
    
    btn = tk.Button(canvas, text=' Close ', command=helper.destroy)
    btn.place(x=375, y=450)
    
    

def browseFiles():
    return filedialog.askopenfilename(initialdir = "C:",
                                          title = "Select a File",
                                          filetypes = [("CSV files",
                                                        "*.csv")])
    
def browseLiveFiles():
    filename = browseFiles()
    with open(filename) as live:
        global data_live
        data_live = live.readlines()
    if(data_live):
        livebtn.config(fg = 'green')
        

def browseDeadFiles():
    filename = browseFiles()
    with open(filename) as dead:
        global data_dead
        data_dead = dead.readlines()
    if(data_dead):
        deadbtn.config(fg = 'green')

def ok_onclick():
    
    ERROR = int(sp.get())
    print(ERROR)
    print(type(ERROR))
    
    livebtn.config(fg = 'red')
    deadbtn.config(fg = 'red')
    
    result = tk.Toplevel(parent)
    result.title("Result Table")
    
    my_game = ttk.Treeview(result)
    my_game['columns'] = ('row', 'live_id', 'live_name', 'dead_id', 'dead_name', 'average_pos')
    
    my_game.column("#0", width=0,  stretch=tk.NO)
    my_game.column("row",anchor=tk.CENTER, width=100)
    my_game.column("live_id",anchor=tk.CENTER, width=100)
    my_game.column("live_name",anchor=tk.CENTER,width=160)
    my_game.column("dead_id",anchor=tk.CENTER,width=100)
    my_game.column("dead_name",anchor=tk.CENTER,width=160)
    my_game.column("average_pos",anchor=tk.CENTER,width=200)
    
    my_game.heading("#0",text="",anchor=tk.CENTER)
    my_game.heading("row",text="Row",anchor=tk.CENTER)
    my_game.heading("live_id",text="Live Id",anchor=tk.CENTER)
    my_game.heading("live_name",text="Live Name",anchor=tk.CENTER)
    my_game.heading("dead_id",text="Dead Id",anchor=tk.CENTER)
    my_game.heading("dead_name",text="Dead Name",anchor=tk.CENTER)
    my_game.heading("average_pos",text="Average Position [x , y]",anchor=tk.CENTER)
    

    for i in range(len(data_dead)):
        data_dead[i] = data_dead[i].split(",")
    
    for i in range(len(data_live)):
        data_live[i] = data_live[i].split(",")     
        
    count = 0
    for i in range (1, len(data_live)):
        for j in range (1, len(data_dead)):
            if (int(data_live[i][X]) < int(data_dead[j][X]) + ERROR) and (int(data_live[i][X]) > int(data_dead[j][X]) - ERROR):
                if (int(data_live[i][Y]) < int(data_dead[j][Y]) + ERROR) and (int(data_live[i][Y]) > int(data_dead[j][Y]) - ERROR):
                    my_game.insert(parent='',index='end',iid=count,text='',values=(count+1, data_live[i][INDEX], data_live[i][NAME], data_dead[j][INDEX], data_dead[j][NAME], '['+str((int(data_live[i][X])+int(data_dead[j][X]))/2)+" , "+str((int(data_live[i][Y])+int(data_dead[j][Y]))/2)+']'))
                    count+=1
        
    my_game.pack()


parent = tk.Tk()
parent.title("EoL - End of Life Software")

# Ajout de l'image (remember image should be PNG and not JPG)
image = Image.open('fiji.png')
img=image.resize((100, 100))
my_img=ImageTk.PhotoImage(img)
limg = tk.Label(parent, image = my_img).grid(row = 0, column = 2, columnspan = 2, rowspan = 2, padx = 5, pady = 5)

l = tk.Label(parent, text = "\nThis software detects cells reaching the end their live\nby processing the file of living cells with that of dead cells\n")
l.config(font =("Colibri", 9))
l.grid(row = 2, column = 2, pady = 0)


photo = Image.open('help.png')
photo = photo.resize((40, 40))
my_photo = ImageTk.PhotoImage(photo)
helpBtn = tk.Button(parent, borderwidth = 0, image = my_photo, command=helpMe).grid(row = 0, column = 5)

# Ajout des boutons
livebtn = tk.Button(parent,text="Living cells file",fg = "red", command=browseLiveFiles)
livebtn.grid(row = 3, column = 0, columnspan = 2, padx = 10)


var = tk.StringVar(parent)
var.set("5")
sp = tk.Spinbox(parent, from_= 0, to = 15, width = 5, textvariable=var)
sp.grid(row = 3, column = 2)

deadbtn = tk.Button(parent,text="Dead cells file",fg = "red", command=browseDeadFiles)
deadbtn.grid(row = 3, column = 4, columnspan = 2, padx = 5)

okbtn = tk.Button(parent, text="Process", command=ok_onclick)
okbtn.grid(row = 4, column = 2, columnspan = 2, pady = 20)

me = tk.Label(parent, text = "by Pierre RAGUENEAU")
me.config(font =("Colibri", 7))
me.grid(row=4, column = 5)

parent.mainloop()