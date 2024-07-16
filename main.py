# ----------------------------------------------------------------------------
# One On One
# Based on the IRC game held by Gameshows.ru community
# Copyright © 2024 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from random import randint
from random import choice
from random import randrange
from threading import Timer
from enum import Enum
import pandas as pd
#import codecs
BLUE = '#0000ff'
GREEN = '#00ff00'
colors = [BLUE, GREEN]
root = tk.Tk()
root.geometry("1160x800")
root.resizable(width=False, height=False)
log = open ('log.txt', 'a')
log.write('\n')
level = 0
start_names = []
player = []
players_info = []
money = [0]
dough_amounts = open('tree.txt', 'r')
for line in dough_amounts:
    h = int(line.rstrip("\n"))
    money.append(h)
#print(money)
x2, x3 = True, True
#current_q = 0
frage = None
var_labels = []
var_buttons = [ [], [] ]
knopki23 = [ [], [] ]
shownamez = []
answer_accepted = [False, False]
def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()



def reveal():
    global level
    var_labels[frage['correct']-1]['bg'] = '#ffff9f'
    log.write("Правильный ответ: "+str(frage['correct'])+'\n')
    playerz_sets = [set(players_info[0]['answers']), set(players_info[1]['answers'])]
    if (frage['correct'] not in (playerz_sets[0]|playerz_sets[1])):
        for i in range(2):
            players_info[i]['money'] = money[0]//2
        tk.messagebox.showerror("Поражение", "Оба игрока дали неправильный ответ и покидают игру ни с чем")
        log.write("Оба игрока дали неправильный ответ и покидают игру ни с чем"+'\n')
    elif(frage['correct'] in (playerz_sets[0]&playerz_sets[1])):
        tk.messagebox.showinfo("Поздравляю!", "Оба игрока дали правильный ответ!")
        for i in range(2):
            players_info[i]['money'] = money[level] // 2
        if (level == 12):
            tk.messagebox.showinfo("ДЖЕКПОТ!", "Вы успешно прошли игру!")
            log.write('Выигрыши:\n'+players_info[0]['name']+': '+str(players_info[0]['money'])+'\n'+players_info[1]['name']+': '+str(players_info[1]['money'])+'\n')
        else:
            if tk.messagebox.askyesno(players_info[0]['name'], 'Будете ли вы продолжать игру?'):
                level+=1
                tk.messagebox.showinfo("Хорошо", "Мы продолжаем игру")
                root.preparing = root.after(2000, load_from_base)
            elif tk.messagebox.askyesno(players_info[1]['name'], 'Будете ли вы продолжать игру?'):
                level+=1
                tk.messagebox.showinfo("Хорошо", "Мы продолжаем игру")
                root.preparing = root.after(2000, load_from_base)
            else:
                tk.messagebox.showinfo("Игра окончена", "Игроки решили забрать деньги, оба получат по "+str(money[level] // 2))
                log.write("Игроки забрали деньги"+'\n')
                log.write('Выигрыши:\n' + players_info[0]['name'] + ': ' + str(players_info[0]['money']) + '\n' +
                          players_info[1]['name'] + ': ' + str(players_info[1]['money']) + '\n')
    elif (frage['correct'] in (playerz_sets[0] ^ playerz_sets[1])):
        if (frage['correct'] in playerz_sets[0]):
            u = 0
        elif (frage['correct'] in playerz_sets[1]):
            u = 1
        for i in range(2):
            if (i == u):
                players_info[i]['money'] = money[level]
            else:
                players_info[i]['money'] = 0
        tk.messagebox.showinfo('Верный ответ!', "Но его дал только "+players_info[u]['name'])
        if (level == 12):
            tk.messagebox.showinfo("ДЖЕКПОТ!", players_info[u]['name'] + " выигрывает всё!")
            log.write('Выигрыши:\n'+players_info[0]['name']+': '+str(players_info[0]['money'])+'\n'+players_info[1]['name']+': '+str(players_info[1]['money'])+'\n')
        else:
            if tk.messagebox.askyesno(players_info[u]['name'], 'Будете ли вы продолжать игру?'):
                level += 1
                tk.messagebox.showinfo("Хорошо", "Мы продолжаем игру")
                root.preparing = root.after(2000, load_from_base)
            else:
                tk.messagebox.showinfo("Игра окончена", players_info[u]['name'] + " решает забрать деньги и выигрывает "+str(players_info[u]['money']))
                log.write(players_info[u]['name']+" забирает деньги" + '\n')
                log.write('Выигрыши:\n' + players_info[0]['name'] + ': ' + str(players_info[0]['money']) + '\n' +
                          players_info[1]['name'] + ': ' + str(players_info[1]['money']) + '\n')







def answer(m):
    if ((m % len(frage['variants']))+1) in players_info[m // len(frage['variants'])]['answers']:
        pass
    else:
        global answer_accepted, colors, var_buttons
        quot = m // len(frage['variants'])
        rem = m % len(frage['variants'])
        var_buttons[quot][rem]['bg'] = colors[quot]
        players_info[quot]['answers'].append(rem+1)
        for i in range(2):
            knopki23[quot][i].place_forget()
        if len(players_info[quot]['answers'])>=players_info[quot]['hm_answers']:
            answer_accepted[quot] = True
            for j in range(len(frage['variants'])):
                var_buttons[quot][j]['state'] = 'disabled'
        if not(False in answer_accepted):
            temp = [', '.join(str(x) for x in sorted(players_info[0]['answers'])), ', '.join(str(x) for x in sorted(players_info[1]['answers']))]
            log.write("Ответы игроков:\n"+players_info[0]['name']+': '+temp[0]+'\n'+players_info[1]['name']+': '+temp[1]+'\n')
            tk.messagebox.showinfo('Принято!', 'Ответы обоих игроков зафиксированы')
            root.reveal_correct = root.after(randint(3000, 5500), reveal)




    #print(players_info[m//len(frage['variants'])]['name'] + ' выбирает ответ '+frage['variants'][m%len(frage['variants'])])

def multiple(y):
    global x2, x3
    if (y % 2 ==0):
        x2=False
        players_info[y//2]['hm_answers'] = 2
        for i in range(2):
            knopki23[i][0].place_forget()
        knopki23[y//2][1]['state'] = 'disabled'
    elif (y % 2 == 1):
        x3=False
        players_info[y//2]['hm_answers'] = 3
        for i in range(2):
            knopki23[i][1].place_forget()
        knopki23[y//2][0]['state'] = 'disabled'
    #tevirp = ['Двойной ответ', 'Тройной ответ']
    #print(players_info[y // 2]['name'] + ' использует опцию '+tevirp[y % 2])

def load_from_base():
    global frage, b, pole_voprosa, var_labels, level, knopki23, answer_accepted, var_buttons, shownamez
    root.after_cancel(root.preparing)
    var_buttons = [[], []]
    shownamez = []
    while True:
        current_q = randint(0, len(b)-1)
        if (b[current_q]['level']==level):
            frage = b[current_q].copy()
            b.pop(current_q)
            break
    log.write("Вопрос "+str(level)+' ('+str(money[level])+')\n')
    log.write(frage['question']+'\n')
    pole_voprosa['text'] = frage['question']
    pole_voprosa.place(relx=0.2, rely=0.02, width=470, height=90)
    var_labels = []
    for i in range(len(frage['variants'])):
        log.write(str(i+1)+'. '+frage['variants'][i]+'\n')
        plo = tk.Label(text=frage['variants'][i], background="#ffffff")
        var_labels.append(plo)
        var_labels[i].place(relx=0.2, rely=0.17+0.07*i, height=35, width=470)
    for i in range(2):
        for j in range(len(frage['variants'])):
            pam = tk.Button(root, text = "Выбор", width=14, height=1, command = lambda a1 = i*len(frage['variants'])+j: answer(a1))
            var_buttons[i].append(pam)
            var_buttons[i][j].place(relx=.02+0.65*i, rely=0.17+0.07*j)
    for i in range(2):
        dvigubas_atsakymas = tk.Button(root, text = players_info[i]['name']+': двойной ответ', command=lambda aaa=i*2+0: multiple(aaa), width=20, height=1)
        trigubas_atsakymas = tk.Button(root, text = players_info[i]['name']+': тройной ответ', command=lambda aaa=i*2+1: multiple(aaa), width=20, height=1)
        knopki23[i].append(dvigubas_atsakymas)
        knopki23[i].append(trigubas_atsakymas)
        knopki23[i][0].place(relx=0.02+0.65*i, rely=0.52)
        knopki23[i][1].place(relx=0.02+0.65*i, rely=0.59)
        knopki23[i][0]['state'] = 'normal'
        knopki23[i][1]['state'] = 'normal'
    if not (x2):
        for i in range(2):
            knopki23[i][0].place_forget()
    if not (x3):
        for i in range(2):
            knopki23[i][1].place_forget()
    for i in range(2):
        players_info[i]['answers'] = []
        # players_info[i]['double'], players_info[i]['triple'] = False, False
        players_info[i]['hm_answers'] = 1
    for i in range(2):
        pp = tk.Label(text=players_info[i]['name'], background="#ffffff")
        shownamez.append(pp)
        shownamez[i].place(relx=.02+0.65*i, rely=0.05, height=35, width=150)
    answer_accepted = [False, False]
    root.title("Вопрос "+str(level)+' ('+str(money[level])+')')










def kwalif():
    global level
    for a in range(len(start_names)):
        if start_names[a].get() == "":
            tk.messagebox.showwarning("Имена", "По меньшей мере у одного из игроков пустое имя. Исправьте")
            break
    else:
        rich.place_forget()
        log.write('Сегодня играют '+start_names[0].get()+' и '+start_names[1].get()+'.\n')
        for b in range(2):
            player[b].place_forget()
            info_dict = {}
            info_dict['name'] = start_names[b].get()
            info_dict['money'] = 0
            info_dict['answers'] = []
            info_dict['hm_answers'] = 1
            # info_dict['double'] = False
            # info_dict['triple'] = False
            players_info.append(info_dict)
        level = 1 #1
        # for i in range(2):
        #     options = {}
        #     options['x2'], options['x3'] = False, False
        #     lifelines.append(options) #lifelines[1]['x3']==0 значит, что игрок №2 НЕ ВОСПОЛЬЗОВАЛСЯ опцией "Тройной ответ" на этом вопросе
        tk.messagebox.showinfo("Вы представились", "Мы начинаем игру")
        root.preparing = root.after(16, load_from_base) #1600








for x in range(2):
    dummy = tk.StringVar()
    dummy.set("Игрок "+str(x+1))
    start_names.append(dummy)

for pl_field in range (2):
    nombre = ttk.Entry(root, textvariable = start_names[pl_field])
    player.append(nombre)
    player[pl_field].place(width=140, relx = 0.03, rely=0.05+pl_field*(0.18))

aa = pd.read_csv("1on1.csv", delimiter=',', names = ['level', 'question', 'variants', 'correct'], skiprows=[0])
b = aa.to_dict('records')
del aa
for c in range(len(b)):
    b[c]['level'] = int(b[c]['level'])
    b[c]['correct'] = int(b[c]['correct'])
    b[c]['variants'] = b[c]['variants'].split("$")

pole_voprosa = tk.Label(root, justify = tkinter.CENTER, bg="#cfcfcf", wraplength = 440)

rich = tk.Button(root, text="Начать игру", command=kwalif, width = 14, height = 30)
rich.place(relx = 0.5, rely=0.05)
root.protocol('WM_DELETE_WINDOW', doSomething)


root.mainloop()
