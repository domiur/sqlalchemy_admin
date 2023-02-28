from tkinter import Frame,Label,Listbox,LEFT,END,Scrollbar,RIGHT,Y,TOP, ANCHOR,X

class TableList(Frame):
    def __init__(self,parent,viewmanager):
        super().__init__(parent)
        self.viewmanager=viewmanager
        self.create()
        self.place_pack()

    def create(self):
        self.txt=Label(text='Tables',master=self)

        self.frame_lbsc=Frame(self)
        self.listbox=Listbox(self.frame_lbsc,width=20,height=10)
        self.scrollbar=Scrollbar(self.frame_lbsc)

        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.viewmanager.set_TableList_listener(self)

    def bind_listbox_event_listener(self, ev, fun):
        self.listbox.bind(ev, fun)

    def get_selected_item(self):
        return self.listbox.get(ANCHOR)

    def place_pack(self):
        self.txt.pack(side=TOP)
        self.frame_lbsc.pack()
        self.listbox.pack(side=LEFT, fill=X)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def place_grid(self):
        self.txt.grid(column=0, row=0,sticky='nw')
        self.frame_lbsc.grid(column=0, row=1,sticky='nw')

        #self.rowconfigure   (0, weight=1)
        #self.rowconfigure   (1, weight=1)
        #self.columnconfigure(0, weight=1)

        self.listbox.grid(column=0,row=0,sticky='nw')
        self.scrollbar.grid(column=1,row=0,sticky="nws")

        #self.frame_lbsc.rowconfigure   (0, weight=1)
        #self.frame_lbsc.columnconfigure(0, weight=1)
        #self.frame_lbsc.columnconfigure(1, weight=1)


    def update(self,tablelist):
        self.listbox.delete(0,END)
        if tablelist:
            for t in tablelist:
                self.listbox.insert(END,t)

    def clear_selection(self):
        self.listbox.select_clear(0,END)