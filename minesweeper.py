__author__ = 'Александр'

from tkinter import *
#импорт функций для диалогового окна выбора файла
from tkinter.filedialog import *
#импорт функций для отображения информационных сообщений
from tkinter.messagebox import *
from random import randrange
from time import *
curr_time = 0
status_map = []
flag_map = []

hgt_glob = 22

def canv_init():
    global status_map,hgt_glob, hgt2_glob, bomb_array,point_mas
    canv.delete('all')
    hgt_glob = int(entr1.get())
    hgt2_glob = int(entr2.get())
    #обнулить status_map
    status_map = []
    point_mas = []
    #отрисовка поля
    for i in range(hgt2_glob):
        #j - строка
        for j in range(hgt_glob):
            xn = i*20+(i+1)*2
            yn = j*20+(j+1)*2
            xk = xn+20
            yk = yn+20
            #добавление прямоугольника
            canv.create_rectangle(xn,yn,xk,yk,fill="lightblue",tag=str(i)+"_"+str(j))
            point_mas.append(str(i)+"_"+str(j))
    #количество бомб, в зависимости от выбранной сложности
    if int(level_sel.get() == 0):
        bomb_count = int((hgt_glob*hgt2_glob)/10)
    else:
        bomb_count = int((hgt_glob*hgt2_glob)/3)
    #генерация бомб
    bomb_array = []
    for i in range(bomb_count):
        status = 0
        while status == 0:
            bi = randrange(hgt2_glob)
            bj = randrange(hgt_glob)
            if str(bi)+"_"+str(bj) in bomb_array:
                status = 0
            else:
                bomb_array.append(str(bi)+"_"+str(bj))
                status_map.append([str(bi)+"_"+str(bj),9])
                #canv.itemconfig(str(bi)+"_"+str(bj),fill="red")
                status = 1
    #проход всех точек и определение статусов
    for i in range(hgt2_glob):
        #j - строка
        for j in range(hgt_glob):
            #просмотр точки, если она не бомба
            if not(str(i)+"_"+str(j) in bomb_array):
                #количество бомб вокруг
                bomb_vokrug = 0
                for k in range(i-1,i+2):
                    for l in range(j-1,j+2):
                        #исключаем ситуации просмотра самой себя
                        if not(i==k and l==j):
                            if str(k)+"_"+str(l) in bomb_array:
                                bomb_vokrug += 1
                status_map.append([str(i)+"_"+str(j),bomb_vokrug])
                xn = i*20+(i+1)*2+10
                yn = j*20+(j+1)*2+10
                #canv.create_text(xn,yn,text=str(bomb_vokrug))


    return 1






    
def stat():
    canv.delete("lv","sp")
    canv.create_text(650,100,text = "Количество бомб:\n" +str(len(bomb_array)-len(flag_map)),font="Arial 20",tag="lv")
#функция проигрыша
def print_map():
    for item in status_map:
        #бомбы рядом нет
        if item[1] == 0:
            canv.itemconfig(item[0],fill="white")
        elif item[1] == 9:
            canv.itemconfig(item[0],fill="red")
        else:
            canv.itemconfig(item[0],fill="white")
            i = int(item[0].split("_")[0])
            j = int(item[0].split("_")[1])
            xn = i*20+(i+1)*2
            yn = j*20+(j+1)*2
            canv.create_text(xn+10,yn+10,text=str(item[1]))
    stat()

#реакция на нажатие
def player(e):
    global bomb_array
    
    for i in range(hgt2_glob):
        
        #j - строка
        for j in range(hgt_glob):
            g = int(hgt_glob*hgt2_glob)
            xn = i*20+(i+1)*2
            yn = j*20+(j+1)*2
            xk = xn+20
            yk = yn+20
            if e.x >= xn and e.x <= xk and e.y >= yn and e.y<=yk:
                if not(str(i)+"_"+str(j) in flag_map):
                    #проверка, есть ли этот прямоугольник в массиве с уровнем
                    for item in status_map:
                        if item[0] == str(i)+"_"+str(j):
                            #бомбы рядом нет
                            if item[1] == 0:
                                canv.itemconfig(str(i)+"_"+str(j),fill="white")
                                point_mas.remove(str(i)+"_"+str(j))
                                for f in range(i-1,i+2):
                                    for g in range(j-1,j+2):
                                        for item in status_map:
                                            if item[1] ==0:
                                                canv.itemconfig(str(f)+"_"+str(g),fill="white")
                                            elif item[1]==9:
                                                canv.itemconfig(str(f)+"_"+str(g),fill="gray")                                                
                                            else:
                                                canv.itemconfig(item[0],fill="white")
                                                f = int(item[0].split("_")[0])
                                                g = int(item[0].split("_")[1])
                                                xn = f*20+(f+1)*2
                                                yn = g*20+(g+1)*2
                                                canv.create_text(xn+10,yn+10,text=str(item[1]))
                                                
                            elif item[1] == 9:
                                canv.itemconfig(str(i)+"_"+str(j),fill="red")
                                #отрисовать всё поле целиком по status_map
                                print_map()
                            else:
                                canv.itemconfig(str(i)+"_"+str(j),fill="white")
                                canv.create_text(xn+10,yn+10,text=str(item[1]))
                                point_mas.remove(str(i)+"_"+str(j))
        
                            print(len(bomb_array))
                            print(len(flag_map))
                            print(len(point_mas))
                            stat()
                       
                            if  len(bomb_array)==len(point_mas):
                                showinfo("Вы выыиграли!","Поздравляем!!!")
                            
                        g -=1
                        
        
        
   

def flag(e):
    global flag_map
    for i in range(22):
        #j - строка
        for j in range(hgt_glob):
            xn = i*20+(i+1)*2
            yn = j*20+(j+1)*2
            xk = xn+20
            yk = yn+20
            if e.x >= xn and e.x <= xk and e.y >= yn and e.y<=yk:
                if str(i)+"_"+str(j) in flag_map:
                     canv.itemconfig(str(i)+"_"+str(j),fill="gray")
                     flag_map.remove(str(i)+"_"+str(j))
                else:
                    canv.itemconfig(str(i)+"_"+str(j),fill="green")
                    flag_map.append(str(i)+"_"+str(j))

#инициализация окна
root = Tk()
root.geometry("550x800+100+100")
root.title("MINESWEEPER")

#инициализация меню
m = Menu(root)
root.config(menu = m)

casc = Menu(m)
edit = Menu(m)
m.add_cascade(label="Игра",menu = casc)
m.add_cascade(label="Настройки",menu = edit)

#casc.add_command(label="Открыть...",command=open_file)
casc.add_command(label="Новая игра",command=canv_init)

level_sel = IntVar()
edit.add_radiobutton(label="Новичок",value=0,variable=level_sel)
edit.add_radiobutton(label="Профи",value=1,variable=level_sel)

canv = Canvas(root,height=600,width=800)
canv.pack()

entr1 = Entry(root)
hgt = IntVar()
entr1["textvariable"] = hgt
entr1.pack()
entr2 = Entry(root)
hgt2 = IntVar()
entr2["textvariable"] = hgt2
entr2.pack()

#бинд на щелчок мыши
root.bind("<Button-1>",player)
root.bind("<Button-3>",flag)

root.mainloop()
