
import pymysql
conn =pymysql.connect(
                      host='127.0.0.1',
                      port=3306,
                      user='root',
                      password='root',
                      db='test',
                      charset='utf8'
                         )

cursor=conn.cursor()
print (conn)
print (cursor)

cursor.close()
conn.close()