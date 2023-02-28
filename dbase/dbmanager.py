from sqlalchemy import create_engine,MetaData

class Singleton(type):
    def __init__(self, name, base, attrs, **kwargs):
        super().__init__(name, base, attrs)
        self.__instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance == None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance

class DBManager(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.engine=None

    def open(self,db_uri):
        #db_uri='sqlite:////home/mdoroshenko/PycharmProjects/sqldbadmin/products.db'
        print (db_uri)
        self.engine = create_engine(db_uri)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.connection = self.engine.connect()

    def close(self):
        if self.engine:
            self.connection.close()
            self.engine.dispose()
            self.engine=None

    def get_table_list(self):
        #print(self.get_table("orders").columns.keys())
        #print(self.get_table("orders").columns.values())
        #print(self.get_table("orders").columns['id'].type)
        if self.engine:
            return self.metadata.tables.keys()
        else:
            return None

    def get_table(self,name):
        if self.engine:
            for k,v in self.metadata.tables.items():
                if k==name:
                    return v
        return None

    def run_sql(self,sql):
        if self.engine:
            r=self.connection.execute(sql)
            return r
        else:
            return None