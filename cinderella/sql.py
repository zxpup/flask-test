import MySQLdb

class Sql:
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    def __del__(self):
        self.conn.close()

    def exec_sql(self, sql):
        try:
            self.conn.ping(True)
        except MySQLdb.Error as e:
            print(e)
        self.cur.execute(sql)
        self.conn.commit()

    def query_sql(self, sql):
        try:
            self.conn.ping(True)
        except MySQLdb.Error as e:
            print(e)
        self.cur.execute(sql)
        return self.cur.rowcount, self.cur.fetchall()

    def connect_sql(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.pwd, database=self.db, charset="utf8")
        self.cur = self.conn.cursor()
        if not self.cur:
            raise(NameError, "连接数据库失败")

    def disconnect_sql(self):
        self.conn.close()
