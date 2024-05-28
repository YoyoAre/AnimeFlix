import psycopg2

def con_psql(host = "192.168.1.128",db = "anime",query = "SELECT * FROM anime;"):
    #host = "192.168.1.128"
    #db = "anime"
    user = "azulito"
    pwd = "1234"
    conn = psycopg2.connect(
    host = host,dbname= db,
    user= user,password=pwd,port="5432"
    )
    cur = conn.cursor()

    #query = "SELECT * FROM anime;"
    print("Query: \n",query)
    cur.execute(query)

    try:
        res = cur.fetchall()
        print(res)
    except:
        res = []
    conn.commit()
    cur.close()
    conn.close()

    return res

class postgres:
    def __init__(self,host = "localhost",db = "anime"):
        self.host = host
        self.db = db
        self.user = "azulito"
        self.pwd = "1234"
        self.custom("""select dblink_connect('usuarios_dblink','host=127.168.1.128 
        user=azulito password=1234 dbname=usuarios');""")
        print("A")
        #dblink a otro postgres
    def complemento(self):
        print("B")
        self.custom("""select dblink_connect('usuarios_dblink','host=127.168.1.128 
        user=azulito password=1234 dbname=usuarios');""")
        self.custom("""
        create or replace view usuarios_distribuido as                                                                                    
        select * from dblink('usuarios_dblink','select * from usuarios')
        as t1(id integer, nombre varchar);
        """)

        #mysql_fdw a mariadb
        self.custom("""
        do
        
        $$begin
        create server mariadb_server
        foreign data wrapper mysql_fdw
        options(host '192.168.1.145', port '3306');

        exception
        when duplicate_object then
        null; --ignore

        end;$$
        """)
        self.custom("""
        do
        
        $$begin
        create user mapping for postgres
        server mariadb_server
        options(username 'azulito', password '1234');

        exception
        when duplicate_object then
        null; --ignore

        end;$$
        """)
        self.custom("""
        create foreign table IF NOT EXISTS tiempo_distribuido(
            id int,
            time varchar(255),
            anime_id int
        )
        server mariadb_server
        options(dbname 'time', table_name 'time');
        """)

    def custom(self,query = "SELECT * FROM anime;"):
        conn = psycopg2.connect(
            host = self.host,dbname= self.db,
            user= self.user,password=self.pwd,port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()
        print("Query: \n",query)
        cur.execute(query)

        try:
            res = cur.fetchall()
            #print(res)
        except:
            res = []
        print(res)
        #conn.commit()
        cur.close()
        conn.close()

        return res
    
    def get_usuario(self, user_id = 0):
        if user_id==0:
            extra = ";"
        else:
            extra = f"where id = {user_id};"
        return self.custom("select * from usuarios_distribuido "+extra)
    
print("--------------------")
print("1")
con1 = postgres()
print("--------------------")
print("2")
con1.custom()
print("--------------------")
print("3")
con1.custom("call inizializar();")
print("--------------------")
print("4")
con1.custom("select current_user, session_user;")
print("--------------------")
print("5")
con1.custom("select definition from pg_views where viewname = 'usuarios_distribuidos';")
print("--------------------")


print("6")
con1.get_usuario()