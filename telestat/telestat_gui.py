#coding: utf-8

import subprocess
import os

from Tkinter import *
import tkFileDialog
from holter_loader import holter_folders, PATH_FILE, run


class App:
    def __init__(self,parent):
        #The frame instance is stored in a local variable 'f'.
        #After creating the widget, we immediately call the 
        #pack method to make the frame visible.

        self.f = Frame(parent)
        self.f.pack(padx = 5, pady = 10)
        
        #we then create an entry widget,pack it and then 
        #create two more button widgets as children to the frame.
    
        self.listbox = Listbox(self.f, width = 100)
        self.listbox.pack(side = LEFT, padx=10)
        for folder in holter_folders():
            self.listbox.insert(END, folder)
        
        bf = Frame(self.f)

        self.add = Button(bf, text="Добавить путь", command=self.add_folder)
        self.add.pack(fill = X, side=TOP)

        self.delete = Button(bf, text="Удалить путь", command=self.delete_folder)
        self.delete.pack(fill = X, side=TOP)

        self.go = Button(self.f, text='Запустить', command=self.run)
        self.go.pack(fill = X, side=BOTTOM)

        bf.pack(fill = BOTH, side = RIGHT)

    def add_folder(self):
        directory = tkFileDialog.askdirectory()
        self.listbox.insert(END, directory)

    def delete_folder(self):
        self.listbox.delete(self.listbox.curselection()[0])

    def run(self):
        f = open(PATH_FILE, 'wb')
        f.write(';'.join([self.listbox.get(index) for index in range(self.listbox.size())]))
        f.close()
        global root
        root.destroy()
        run()


root = Tk()
root.title('Статистика холтеров')
app = App(root)

root.mainloop()

    # if fn == '':
    #     return
    # textbox.delete('1.0', 'end') 
    # textbox.insert('1.0', open(fn, 'rt').read())