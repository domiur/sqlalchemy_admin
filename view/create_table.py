from tkinter import Frame,Button,Label,Entry,StringVar
class CreateTableButtons(Frame):
    def __init__(self,parent,viewmanager):
        super().__init__(parent)
        self.viewmanager=viewmanager
        self.create()

    def create(self):
        Label(text="Table name:",master=self).pack(side='top',fill='x')
        self.tablenamevar=StringVar("")
        Entry(master=self,textvariable=self.tablenamevar).pack(side='top',fill='x')
        self.btn_new=Button(text='New item',master=self)
        self.btn_new.pack(side='top',fill='x')
        self.btn_del=Button(text='Delete item',master=self)
        self.btn_del.pack(side='top',fill='x')
        self.btn_create=Button(text='Create table',master=self)
        self.btn_create.pack(side='top',fill='x')
        self.btn_cancel=Button(text='Cancel',master=self)
        self.btn_cancel.pack(side='top',fill='x')

        self.viewmanager.set_CreateTableButtons_listener(self)


    def bind_btn_new_event_listener(self, fun):
        self.btn_new.config(command=fun)
    def bind_btn_del_event_listener(self, fun):
        self.btn_del.config(command=fun)
    def bind_btn_create_event_listener(self, fun):
        self.btn_create.config(command=fun)
    def bind_btn_cancel_event_listener(self, fun):
        self.btn_cancel.config(command=fun)
