import psycopg2
class postgres:
    def __init__(self,host = "localhost",db = "anime"):
        self.host = host
        self.db = db
        self.user = "azulito"
        self.pwd = "1234"
        self.custom("call inizializar();")
    def custom(self,query = "SELECT * FROM anime;"):
        conn = psycopg2.connect(
            host = self.host,dbname= self.db,
            user= self.user,password=self.pwd,port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()
        #print("Query: \n",query)
        cur.execute(query)

        try:
            res = cur.fetchall()
        except:
            res = []
        #print(res)
        cur.close()
        conn.close()

        return res
    def get_usuario(self, user_id = 0):
        if user_id==0:
            extra = ";"
        else:
            extra = f"where id = {user_id};"
        return self.custom("select * from usuarios_distribuido "+extra)
    def get_anime(self, anime_id = 0):
        if anime_id==0:
            extra = ";"
        else:
            extra = f"where id = {anime_id};"
        return self.custom("select * from anime"+extra)

    def join(self, user_id = 0, anime_id = 0):
        donde = ""
        if anime_id != 0 or user_id != 0:
            donde += "where "
        if user_id != 0:
            donde += f"u.id = {user_id} "
        if user_id != 0 and anime_id != 0:
            donde += f"and "
        if anime_id != 0:
            donde += f"a.id = {anime_id} "
        donde += ";"

        query = """
        select 
        u.nombre as usuario, 
        v.time as fecha,
        a.anime as anime
        from 
        usuarios_distribuido u 
        join 
        tiempo_distribuido v on u.id = v.id
        join
        anime a on v.anime_id = a.id
        """
        return self.custom(query+donde)
 