from tkinter import Frame,NO,CENTER
from tkinter.ttk import Treeview
from tkinter.ttk import Style
from dbase.dbmanager import DBManager

class AdminSchema(Frame):
    def __init__(self,parent,viewmanager):
        super().__init__(parent)
        self.viewmanager=viewmanager
        self.create()
        self.viewmanager.set_SchemaListener(self)

    def create(self):
        self.schema_table = Treeview(self,height=40)
        self.schema_table.grid(column=0,row=0,sticky='news')
        s = Style()
        s.configure('Treeview', rowheight=40)

        self.schema_table['columns'] = ['name', 'type','primary_key','foreign_keys']

        self.schema_table.column("#0", width=0, stretch=NO)
        self.schema_table.column("name", anchor=CENTER, width=180)
        self.schema_table.column("type", anchor=CENTER, width=180)
        self.schema_table.column("primary_key", anchor=CENTER, width=180)
        self.schema_table.column("foreign_keys", anchor=CENTER, width=280)

        # self.schema_table.heading("#0",text="",anchor=CENTER)
        self.schema_table.heading("name", text="Name", anchor=CENTER)
        self.schema_table.heading("type", text="Type", anchor=CENTER)
        self.schema_table.heading("primary_key", text="PrimaryKey", anchor=CENTER)
        self.schema_table.heading("foreign_keys", text="ForeignKeys", anchor=CENTER)

    def set_event_listener(self,event,fun):
        self.schema_table.bind(event,fun)
    def update(self,names,types,primary_keys,foreign_keys):
        self.schema_table.delete(*self.schema_table.get_children())
        if names is not None:
            for id,(name,type,primary_key,foreign_key) in enumerate(zip(names,types,primary_keys,foreign_keys)):
                self.schema_table.insert(parent='',index='end',iid=id,text='',values=(name,type,primary_key,foreign_key))

    def clear(self):
        self.schema_table.delete(*self.schema_table.get_children())

    def add_item(self):
        self.schema_table.insert(parent='', index='end', text='', values=("new_item", "INTEGER","",""))

    def get_selected(self):
        return self.schema_table.focus()
    def delete_selected_item(self):
        item=self.get_selected()
        if item:
            self.schema_table.delete(item)