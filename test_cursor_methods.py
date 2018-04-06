
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

sql_insert="insert into user(userid,username) values(4,'name4')"
sql_update = "update user set username='name91' where userid=1"
sql_delete = "delete from user where userid<2"

cursor.execute(sql_insert)
print (cursor.rowcount)
cursor.execute(sql_update)
print (cursor.rowcount)
cursor.execute(sql_delete)
print (cursor.rowcount)

cursor.close()
conn.close()