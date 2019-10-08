import hashlib
import MySQLdb

conn = MySQLdb.connect(host='192.168.8.146', port=3306, user='sa',
                        password='yq888888', database='Cinderella', charset="utf8")
cur = conn.cursor()

def hashstr(string):
    h = hashlib.md5()
    h.update(string.encode(encoding='utf-8'))
    mdstr = h.hexdigest()
    return mdstr[2:8] 

s = dict()
for i in range(2000):
    s[hashstr(str(i))] = 0

for k in s.keys():
    sql_str = "INSERT INTO promo_codes "\
              "VALUES('{}')".format(k)
    cur.execute(sql_str)
    conn.commit()
