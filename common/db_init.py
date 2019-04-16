import os
import psycopg2

_init_sql_path = os.path.join(os.path.dirname(__file__), 'init.sql')
with open(_init_sql_path, 'rb') as f:
    _init_sql = f.read().decode('utf8')

conn = psycopg2.connect(user="newuser",
                        password="password",
                        host="127.0.0.1",
                        port="5432",
                        database="mydb")
cursor = conn.cursor()
print(_init_sql)
cursor.execute(_init_sql)
conn.commit()
conn.close()
cursor.close()
