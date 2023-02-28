from tkinter import Frame,Toplevel,Label,Entry,Listbox,Scrollbar,Button,StringVar,Variable,END
from tkinter.simpledialog import _setup_dialog
from glob import glob
import os

class OpenFileDialog(Frame):
    def __init__(self,parent,viewmanager):
        self.viewmanager=viewmanager

        self.current_dir=os.path.abspath(".")

        self.dialog= Toplevel(parent)
        self.dialog.title("Open file")
        _setup_dialog(self.dialog)

        topframe, self.pathvar = self.add_path(self.dialog)
        topframe.pack(side='top',fill='x')
        self.pathvar.set(self.current_dir)

        midframe1=self.add_labels(self.dialog)
        midframe1.pack(side='top',fill='x')

        midframe,self.listboxdir,self.dirvar,self.listboxfiles, self.filevar =self.add_listboxes(self.dialog)
        midframe.pack(side='top',fill='x')

        bottomframe=Frame(self.dialog)
        bottomframe.pack(side='top')

        bottomframe1=self.add_bottom_labels(bottomframe)
        bottomframe1.pack(side='left')

        bottomframe2,self.filenamevar,self.filtervar = self.add_bottom_entries(bottomframe)
        bottomframe2.pack(side='left')
        self.filenamevar.set("")
        self.filtervar.set("*")

        bottomframe3,self.btn_create,self.btn_apply=self.add_bottom_btn1(bottomframe)
        bottomframe3.pack(side='left')

        bottomframe4,self.btn_open,self.btn_cancel=self.add_bottom_btn2(bottomframe)
        bottomframe4.pack(side='left')

        self.update_listbox_dirs()
        self.update_listbox_files()

        self.viewmanager.set_OpenFileDialog_listener(self)

    def add_path(self,masterframe):
        frame = Frame(masterframe)
        lb_path=Label(text="Path:",master=frame)
        pathvar=StringVar()
        en_path = Entry(master=frame,textvariable=pathvar)
        lb_path.grid(column=0,row=0)
        en_path.grid(column=1,row=0,sticky='we')
        frame.columnconfigure(1,weight=1)
        return frame,pathvar

    def add_labels(self,masterframe):
        frame=Frame(masterframe)
        l21=Label(text="Directories",master=frame)
        l22=Label(text="Files",master=frame)
        l21.grid(column=0,row=0)
        l22.grid(column=1,row=0)
        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        return frame

    def add_listboxes(self,masterframe):
        frame=Frame(masterframe)

        dirvar=Variable()
        listboxdir=Listbox(frame, listvariable=dirvar)
        listboxdir.configure(exportselection=False)

        filevar=Variable()
        listboxfiles=Listbox(frame, listvariable=filevar)

        sb21=Scrollbar(frame, command=listboxdir.yview)
        sb22=Scrollbar(frame, command=listboxfiles.yview)
        listboxdir["yscrollcommand"]=sb21.set
        listboxfiles["yscrollcommand"]=sb22.set

        sb21.grid(column=0,row=0,sticky='ns')
        listboxdir.grid(column=1,row=0,sticky='news')
        listboxfiles.grid(column=2, row=0, sticky='news')
        sb22.grid(column=3,row=0,sticky='ns')
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=1)

        return frame,listboxdir,dirvar,listboxfiles,filevar

    def add_bottom_labels(self,masterframe):
        frame=Frame(masterframe)
        l31=Label(text="File name:",master=frame)
        l32=Label(text="Filter:",master=frame)
        l31.pack(side='top')
        l32.pack(side='top')
        return frame

    def add_bottom_entries(self,masterframe):
        frame=Frame(masterframe)
        filenamevar=StringVar()
        filtervar=StringVar()
        e31=Entry(master=frame,textvariable=filenamevar)
        e32=Entry(master=frame,textvariable=filtervar)
        e31.pack(side='top')
        e32.pack(side='top')
        return frame,filenamevar,filtervar
    def add_bottom_btn1(self,masterframe):
        frame=Frame(masterframe)
        b32=Button(text="create",master=frame)
        b33=Button(text="apply",master=frame)
        b32.pack(side='top',fill='x')
        b33.pack(side='top',fill='x')
        return frame,b32,b33
    def add_bottom_btn2(self,masterframe):
        frame=Frame(masterframe)
        frame.pack(side='left')
        b42=Button(text="open",master=frame)
        b43=Button(text="cancel",master=frame)
        b42.pack(side='top',fill='x')
        b43.pack(side='top',fill='x')
        return frame,b42,b43



    def update_listbox_dirs(self):
        self.dirvar.set(self.get_list_dirs())
        self.listboxdir.select_clear(0, END)

    def update_listbox_files(self):
        self.filevar.set(self.get_list_files())
        self.listboxfiles.select_clear(0, END)

    def get_selected_dir(self):
        cursel = self.listboxdir.curselection()
        dir = self.listboxdir.get(cursel) if cursel else None
        return dir
    def get_selected_file(self):
        cursel = self.listboxfiles.curselection()
        file = self.listboxfiles.get(cursel) if cursel else None
        return file
    def get_selected_path(self):
        dir = self.get_selected_dir()
        path=os.path.join(self.current_dir, dir) if dir else self.current_dir
        return path

    def current_dir_add_dir(self, dir):
        if dir:
            self.current_dir = os.path.join(self.current_dir, dir)

    def current_dir_remove_last_dir(self):
        if self.current_dir=="/":
            pass
        else:
            self.current_dir = os.sep.join(self.current_dir.split(os.sep)[0:-1])
            if self.current_dir == "":
                self.current_dir = os.sep

    def get_list_dirs(self):
        dirs=[name for name in os.listdir(self.current_dir) if os.path.isdir(os.path.join(self.current_dir, name))]
        dirs.sort()
        if self.current_dir!="/":
            return [".."]+dirs
        else:
            return dirs

    def get_list_files(self):
        path=self.get_selected_path()

        filter=self.filtervar.get()
        if filter=="":
            self.filtervar.set("*")
            filter="*"
        path_with_filter=os.path.join(path, filter)

        files = [name.split(os.sep)[-1] for name in glob(path_with_filter) if os.path.isfile(name)]
        files.sort()
        return files


    def quite(self):
        self.dialog.destroy()


    #set listeners
    def set_btn_cancel_listener(self,fun):
        self.btn_cancel.config(command=fun)
    def set_btn_apply_listener(self,fun):
        self.btn_apply.config(command=fun)
    def set_btn_create_listener(self,fun):
        self.btn_create.config(command=fun)
    def set_btn_open_listener(self,fun):
        self.btn_open.config(command=fun)

    def set_listbox_dir_listener(self,ev,fun):
        self.listboxdir.bind(ev,fun)
    def set_listbox_files_listener(self,ev,fun):
        self.listboxfiles.bind(ev,fun)

    def set_pathvar(self,n=None):
        if n is None:
            n = self.current_dir
        self.pathvar.set(n)
    def set_filenamevar(self,n=None):
        if n is None:
            n=""
        self.filenamevar.set(n)

