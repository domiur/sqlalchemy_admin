from tkinter import Frame,NO,CENTER
from tkinter.ttk import Treeview
from tkinter.ttk import Style
from dbase.dbmanager import DBManager

class AdminData(Frame):
    def __init__(self,parent,viewmanager):
        super().__init__(parent)
        self.viewmanager=viewmanager
        self.create()

    def create(self):
        self.data_table = Treeview(self, height=30)
        self.data_table.grid(column=0, row=0,sticky='news')
        s = Style()
        s.configure('Treeview', rowheight=40)


    def update(self,keys,result):
        self.clear()
        self.data_table['columns'] = [""]
        if keys is not None:
            self.data_table['columns'] = keys

            self.data_table.column("#0", width=0, stretch=NO)
            for k in keys:
                self.data_table.column(k, anchor=CENTER, width=180)
                self.data_table.heading(k, text=k, anchor=CENTER)

            for id,c in enumerate(result):
                self.data_table.insert(parent='', index='end', iid=id, text='', values=c.values())

    def clear(self):
        self.data_table.delete(*self.data_table.get_children())
