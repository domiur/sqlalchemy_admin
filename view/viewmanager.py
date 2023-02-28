from view.tables import TableList
from view.notebook import AdminNotebook
from view.menu import AdminMenu
from dbase.dbmanager import Singleton
from dbase.dbmanager import DBManager
#from sqlalchemy import URL
from tkinter import messagebox,Text,Button,StringVar,Entry
import os
from view.create_table import CreateTableButtons

import json
class ViewManager(metaclass=Singleton):
    def __init__(self,win):
        self.DB=DBManager()

        self.current_table=None

        self.win=win
        #self.win.resizable(0, 0)
        self.menu=AdminMenu(self.win,self)

        self.tablelist=TableList(self.win,self)
        #self.tablelist.pack(side=LEFT)
        self.tablelist.grid(column=0,row=0,sticky='news')

        self.note=AdminNotebook(win,self)
        #self.note.pack(side=RIGHT,fill=Y)
        self.note.grid(column=1,row=0,sticky='nw')

        self.win.columnconfigure(0, weight=1)
        self.win.columnconfigure(1, weight=1)
        self.win.rowconfigure(0, weight=1)

        self.read_config("config.json")

    def read_config(self,file_name):
        with open(file_name,'r') as f:
            self.config=json.load(f)

    def select_table(self,event):
        self.current_table = self.tablelist.get_selected_item()
        self.update_note()

    def open_sqlite_DB(self, filename):
        db_uri = 'sqlite:///' + filename
        DBManager().open(db_uri)
        self.current_table=None

    def open_mysql_DB(self, host,user,passwrd,dbname):
        """url_object = URL.create(
            "mysql",
            username=user,
            password=passwrd,
            host=host,
            database=dbname,
        )"""
        url_object = f"mysql+pymysql://{user}:{passwrd}@{host}/{dbname}"

        print(url_object)
        DBManager().open(url_object)
        self.current_table=None
        self.tablelist.update(DBManager().get_table_list())
        self.update_note()

    def open_postgresql_DB(self, host, user, passwrd, dbname):
        """url_object = URL.create(
            "mysql",
            username=user,
            password=passwrd,
            host=host,
            database=dbname,
        )"""
        url_object = f"postgresql+pg8000://{user}:{passwrd}@{host}/{dbname}"

        print(url_object)
        DBManager().open(url_object)
        self.current_table = None
        self.tablelist.update(DBManager().get_table_list())
        self.update_note()
    def update(self,name):
        if name:
            self.open_sqlite_DB(name)
        else:
            DBManager().close()
            self.current_table = None
        self.tablelist.update(DBManager().get_table_list())
        self.update_note()

    def update_note(self):
        sqltable = DBManager().get_table(self.current_table)

        names = None
        types = None
        primary_keys = None
        foreign_keys = []
        result = None
        if sqltable is not None:
            names = [x.name for x in sqltable.columns]
            types = [x.type for x in sqltable.columns]
            primary_keys = [x.primary_key for x in sqltable.columns]
            for key in [c.foreign_keys for c in sqltable.columns]:
                f = [i.column for i in key] if len(key) > 0 else []
                foreign_keys.append(f)
            s = sqltable.select()
            result = DBManager().run_sql(s)
        self.note.update(names, types, primary_keys, foreign_keys,result)

    def set_create_table_status(self):
        self.note.schema_clear()
        self.note.data_clear()
        self.note.schema_select()
        self.tablelist.clear_selection()
        self.create_table_buttos=CreateTableButtons(self.win,self)
        self.create_table_buttos.grid(column=0,row=0,sticky='news')


    ######################################################
    ## set listeners
    ######################################################
    def set_ConnectToServerDBDialog_listener(self, dialog, dbtype):
        def cancel_listener():
            dialog.close()
        dialog.bind_button_cancel_listener(cancel_listener)
        def ok_listener():
            host,user,passwrd,dbname=dialog.get_all_fields()
            if host == "" or user == "" or passwrd == "" or dbname == "":
                return
            try:
                if dbtype==1:
                    self.open_mysql_DB(host, user, passwrd, dbname)
                else:
                    self.open_postgresql_DB(host, user, passwrd, dbname)
            except :
                messagebox.showerror("Error", "Can't connect to DB. Please check inputs.")
            else:
                dialog.close()
        dialog.bind_button_ok_listener(ok_listener)

    def set_OpenFileDialog_listener(self,dialog):
        def cancel_listener():
            dialog.close()
        dialog.set_btn_cancel_listener(cancel_listener)
        def apply_listener():
            dialog.update_listbox_files()
        dialog.set_btn_apply_listener(apply_listener)
        def create_listener():
            dialog.close()
        dialog.set_btn_create_listener(create_listener)
        def open_listener():
            file = dialog.get_selected_file()
            if file:
                path = dialog.get_selected_path()
                path_with_file = os.path.join(path, file)
                if os.path.isfile(path_with_file):
                    self.update(path_with_file)
                    dialog.close()
        dialog.set_btn_open_listener(open_listener)

        def onClick_dir(event):
            dialog.update_listbox_files()
            dialog.set_pathvar(dialog.get_selected_path())
            dialog.set_filenamevar("")
        dialog.set_listbox_dir_listener('<<ListboxSelect>>', onClick_dir)


        def onClick_file(event):
            dialog.set_filenamevar( dialog.get_selected_file() )
        dialog.set_listbox_files_listener('<<ListboxSelect>>', onClick_file)

        def onDoubleClick_dir(event):
            dir = dialog.get_selected_dir()
            if dir is None:
                pass
            elif dir=="..":
                dialog.current_dir_remove_last_dir()
            else:
                dialog.current_dir_add_dir(dir)


            dialog.update_listbox_dirs()
            dialog.set_pathvar()
            dialog.set_filenamevar()
        dialog.set_listbox_dir_listener('<Double-1>', onDoubleClick_dir)

    def set_TableList_listener(self,table):
        table.bind_listbox_event_listener('<<ListboxSelect>>', self.select_table)

    def set_SchemaListener(self,schema):
        def onDoubleClick(event):
            column = schema.schema_table.identify_column(event.x)
            row = schema.schema_table.identify_row(event.y)
            print(column,row,event)
            if schema.schema_table.identify_region(event.x,event.y)=="cell" and column and row:
                cn = int(column[1:])-1
                box=schema.schema_table.bbox(row,cn)

                selected_id=schema.schema_table.focus()
                items=schema.schema_table.item(selected_id)
                if column =="#0":
                    selected_text=items.get("text")
                else:
                    selected_text=items.get("values")[cn]
                entryedit = Entry(schema)
                entryedit.place(x=box[0],y=box[1],width=box[2],height=box[3])
                entryedit.column_ind=cn
                entryedit.item_id=selected_id
                entryedit.select_range(0,'end')
                entryedit.focus()
                def on_return(ev):
                    new_txt=ev.widget.get()
                    if ev.widget.column_ind==-1:
                        schema.schema_table.item(ev.widget.item_id,text=new_txt)
                    else:
                        v=schema.schema_table.item(ev.widget.item_id).get("values")
                        v[ev.widget.column_ind]=new_txt
                        schema.schema_table.item(ev.widget.item_id, values=v)
                    ev.widget.destroy()
                entryedit.bind('<FocusOut>',lambda x:x.widget.destroy())
                entryedit.bind('<Return>',on_return)
        schema.set_event_listener('<Double-1>',onDoubleClick)

    def set_CreateTableButtons_listener(self,btns):
        def cancel():
            btns.destroy()
            self.note.schema_clear()
        btns.bind_btn_cancel_event_listener(cancel)
        def create():
            pass
        btns.bind_btn_create_event_listener(create)

        def delete():
            self.note.schema_delete_selected_item()
        btns.bind_btn_del_event_listener(delete)
        def new():
            self.note.schema_add_item()
        btns.bind_btn_new_event_listener(new)