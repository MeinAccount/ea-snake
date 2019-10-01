import collections
import multiprocessing
import threading
from tkinter import *
import evolution_render
from ea.store import Store
from game.simulation import dnn_to_handler
from render import App

load_cromosomes = []
ins_cromosomes = []
max_generation = 10
global curr_case
curr_case = 1


def CurSelect(evt):
    value = str(listNodes.get(listNodes.curselection()))
    if curr_case == 0:
        handler = dnn_to_handler(load_cromosomes[int(value.replace("Generation ", "")) - 1][-1])
    else:
        handler = ins_cromosomes[int(value.replace("Generation ", "")) - 1]
    app = App(handler)
    app.on_execute()


def insert(chromo):
    ins_cromosomes.append(chromo)
    if curr_case == 1:
        listNodes.insert(END, "Generation " + str(len(ins_cromosomes) - 1))


window = Tk()  # create window
window.configure(bg='lightgrey')
window.title("Snake Evolution Simulator")
window.geometry("200x400")

lbl1 = Label(window, text="Generation List:", fg='black', font=("Helvetica", 16, "bold"))
scrollbar = Scrollbar(window, orient="vertical")
scrollbar.pack(side=RIGHT, fill=Y)

listNodes = Listbox(window, yscrollcommand=scrollbar.set, font=("Helvetica", 12), selectmode=SINGLE)
listNodes.pack(expand=True, fill=Y)
listNodes.bind('<<ListboxSelect>>', CurSelect)
scrollbar.config(command=listNodes.yview)


def load_generations():
    global curr_case
    curr_case = 0
    listNodes.delete(0, END)
    for i in range(1, max_generation):
        test = Store.loadGen(i)
        load_cromosomes.append(test)
        listNodes.insert(END, "Generation " + str(i))


b = Button(window, text="Load Generations", command=load_generations)
b.pack()



def test(Updater):
    while True:
        window.update()
        Updater()


if __name__ == '__main__':
    test(lambda: None)
