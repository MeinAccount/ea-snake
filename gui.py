from tkinter import *

generation_apps = []


def CurSelect(evt):
    value = str(listNodes.get(listNodes.curselection()))
    generation_apps[int(value.replace("Generation ", "")) - 1].on_execute()


def insert(app):
    listNodes.insert(END, "Generation " + str(listNodes.size()))
    generation_apps.append(app)


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


def test(QueueHandler):
    while True:
        window.update()
        QueueHandler.update()
