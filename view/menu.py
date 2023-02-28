from tkinter import Frame,Menu
from tkinter import filedialog
from view.open_file_dialog import OpenFileDialog
from view.connect_to_serverDB import ConnectToServerDBDialog

class  AdminMenu(Frame):
    def __init__(self,parent,viewmanager):
        super().__init__(parent)
        self.viewmanager=viewmanager
        self.init()

    def init(self):
        menubar=Menu(self.master)
        self.master.config(menu=menubar)

        db_menu=self.add_menu_database(menubar)
        menubar.add_cascade(label='DataBase',menu=db_menu)

        table_menu=self.add_menu_table(menubar)
        menubar.add_cascade(label='Table',menu=table_menu)

    def add_menu_database(self,parentmenu):
        db_menu = Menu(parentmenu, tearoff=0)
        db_menu.add_command(label='Create new', command=self.createDB)

        db_type=self.add_menu_database_connect(db_menu)
        db_menu.add_cascade(label='Connect to', menu=db_type)

        db_menu.add_command(label='Close', command=self.close)
        db_menu.add_command(label='Exit', command=self.onExit)
        return db_menu

    def add_menu_database_connect(self,parentmenu):
        db_type = Menu(parentmenu, tearoff=0)
        db_type.add_command(label='sqlite', command=self.openDB_sqlite)
        db_type.add_command(label='MySql', command=self.openDB_mysql)
        db_type.add_command(label='PostgreSQL', command=self.openDB_postgresql)
        return db_type
    def add_menu_table(self,parentmenu):
        table_menu = Menu(parentmenu, tearoff=0)
        table_menu.add_command(label='Create', command=self.createTable)
        table_menu.add_command(label='Delete', command=self.onExit)
        return table_menu

    def onExit(self):
        self.quit()

    def createDB(self):
        OpenFileDialog(self.master,self.viewmanager)

    def openDB_sqlite(self):
        filetypes = (
            ('db files', '*.db'),
            ('All files', '*')
        )

        filename = filedialog.askopenfile(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)

        if filename:
            self.viewmanager.update(filename.name)
        else:
            return None

    def close(self):
        self.viewmanager.update(None)

    def openDB_mysql(self):
        ConnectToServerDBDialog(self.master, self.viewmanager)

        #self.viewmanager.open_mysql_DB('localhost','test','Toptoptop01!','testsqlalchemy')
    def openDB_mysql(self):
        ConnectToServerDBDialog(self.master, self.viewmanager, dbtype=1,
                                host=self.viewmanager.config["mysql"]["host"],
                                user=self.viewmanager.config["mysql"]["user"],
                                passw=self.viewmanager.config["mysql"]["passw"],
                                db=self.viewmanager.config["mysql"]["db_name"])
    def openDB_postgresql(self):
        ConnectToServerDBDialog(self.master, self.viewmanager, dbtype=2,
                                host=self.viewmanager.config["postgres"]["host"],
                                user=self.viewmanager.config["postgres"]["user"],
                                passw=self.viewmanager.config["postgres"]["passw"],
                                db=self.viewmanager.config["postgres"]["db_name"])


    def createTable(self):
        self.viewmanager.set_create_table_status()
