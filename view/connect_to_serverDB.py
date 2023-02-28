from tkinter import Frame,Toplevel,Label,Entry,Button,StringVar
from tkinter.simpledialog import _setup_dialog
from tkinter import messagebox


class ConnectToServerDBDialog(Frame):
    def __init__(self,parent,viewmanager,dbtype,host=None,user=None,passw=None,db=None):
        self.viewmanager=viewmanager

        self.dialog= Toplevel(parent)
        self.dialog.title("MySQL" if dbtype==1 else "PostgreSQL")
        _setup_dialog(self.dialog)

        topframe=Frame(self.dialog)
        topframe.pack(side='top',fill='x')

        topframe1 = self.add_labels(topframe)
        topframe1.pack(side='left', fill='x')

        topframe2, self.hostvar, self.uservar, self.passwrdvar, self.dbnamevar = self.add_entry_fields(topframe)
        topframe2.pack(side='left', fill='x')
        self.hostvar.set(host)
        self.uservar.set(user)
        self.passwrdvar.set(passw)
        self.dbnamevar.set(db)


        bottomframe, self.btn_ok, self.btn_cancel = self.add_buttons( self.dialog)
        bottomframe.pack(side='top',fill='x')

        self.viewmanager.set_ConnectToServerDBDialog_listener(self, dbtype)

    def add_labels(self, masterframe):
        frame = Frame(masterframe)
        l11 = Label(text="Hostname:", master=frame)
        l12 = Label(text="User:", master=frame)
        l13 = Label(text="password:", master=frame)
        l14 = Label(text="DB name:", master=frame)
        l11.pack(side='top',fill='x')
        l12.pack(side='top',fill='x')
        l13.pack(side='top',fill='x')
        l14.pack(side='top',fill='x')
        return frame


    def add_entry_fields(self, masterframe):
        frame = Frame(masterframe)

        hostvar = StringVar(value="")
        en_host = Entry(master=frame, textvariable=hostvar)
        en_host.pack(side='top', fill='x')

        uservar = StringVar(value="")
        en_user = Entry(master=frame, textvariable=uservar)
        en_user.pack(side='top', fill='x')

        passwrdvar = StringVar(value="")
        en_passw = Entry(master=frame, show="*", textvariable=passwrdvar)
        en_passw.pack(side='top', fill='x')

        dbnamevar = StringVar(value="")
        en_dbname = Entry(master=frame, textvariable=dbnamevar)
        en_dbname.pack(side='top', fill='x')

        return frame,hostvar,uservar,passwrdvar,dbnamevar

    def add_buttons(self, masterframe):
        frame = Frame(masterframe)
        btn_ok = Button(text="Ok", master=frame)
        btn_cancel = Button(text="Cancel", master=frame)
        btn_ok.pack(side='top', fill='x')
        btn_cancel.pack(side='top', fill='x')
        return frame,btn_ok,btn_cancel

    def bind_button_ok_listener(self, fun):
        self.btn_ok.config(command=fun)

    def bind_button_cancel_listener(self, fun):
        self.btn_cancel.config(command=fun)

    def close(self):
        self.dialog.destroy()

    def get_all_fields(self):
        return (self.hostvar.get(),
                self.uservar.get(),
                self.passwrdvar.get(),
                self.dbnamevar.get())


