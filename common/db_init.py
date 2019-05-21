import os
import psycopg2

_init_sql_path = os.path.join(os.path.dirname(__file__), 'init.sql')
with open(_init_sql_path, 'rb') as f:
    _init_sql = f.read().decode('utf8')

_populate_sql_path = os.path.join(os.path.dirname(__file__), 'populate_db.sql')
with open(_populate_sql_path, 'rb') as f:
    _populate_sql = f.read().decode('utf8')

conn = psycopg2.connect(user="skflpscmrdpxig",
                        password="b5d9f1887753ae2dedf55325f7253f053a46388c685fa288ff1d4469b15fabe1",
                        host="ec2-23-21-128-35.compute-1.amazonaws.com",
                        port="5432",
                        database="d8i4u0mq57b2cv")
cursor = conn.cursor()
print(_init_sql)
cursor.execute(_init_sql)
cursor.execute(_populate_sql)
conn.commit()
conn.close()
cursor.close()
