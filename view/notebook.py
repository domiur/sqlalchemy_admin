from tkinter.ttk import Notebook
from tkinter import Frame
from view.schema import AdminSchema
from view.data import AdminData
from dbase.dbmanager import DBManager

class AdminNotebook(Frame):
    def __init__(self,parent,viewmanager):
        super().__init__(parent)
        self.viewmanager=viewmanager
        self.create()
        self.place_grid()

    def create(self):
        self.nb=Notebook(self)
        self.schema=AdminSchema(self.nb,self.viewmanager)
        self.data=AdminData(self.nb,self.viewmanager)

        self.nb.add(self.schema,text="Schema")
        self.nb.add(self.data,text="Data")

    def place_pack(self):
        self.nb.pack()

    def place_grid(self):
        self.nb.grid(column=0,row=0,sticky='nw')

    def update(self,names,types,primary_keys,foreign_keys,result):
        self.schema.update(names,types,primary_keys,foreign_keys)
        self.data.update(names,result)

    def schema_add_item(self):
        self.schema.add_item()
    def schema_clear(self):
        self.schema.clear()
    def data_clear(self):
        self.data.clear()

    def schema_select(self):
        self.nb.select(0)
    def schema_get_selected_item(self):
        return self.schema.get_selected()

    def schema_delete_selected_item(self):
        self.schema.delete_selected_item()