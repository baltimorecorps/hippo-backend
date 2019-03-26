import psycopg2

conn = psycopg2.connect(user="newuser",
                        password="password",
                        host="127.0.0.1",
                        port="5432",
                        database="mydb")
cursor = conn.cursor()
cursor.execute("CREATE TYPE gender AS ENUM ('Male', 'Female', 'Non-binary', 'Not Listed')")
cursor.execute("CREATE TYPE race AS ENUM ('Asian', 'White', 'Black', 'Hispanic/Latinx')")
cursor.execute("CREATE TYPE salutation AS ENUM ('Ms.', 'Miss', 'Mr.', 'Mrs.', 'Dr.')")
create_table_query = '''CREATE TABLE IF NOT EXISTS Contact (id SERIAL PRIMARY KEY NOT NULL, first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL, email_primary VARCHAR (100) NOT NULL, phone_primary
                        VARCHAR (25), current_profile INTEGER , gender gender,
                        race_all race, birthdate DATE NOT NULL, salutation salutation) ;'''
cursor.execute(create_table_query)
conn.commit()
cursor.execute("CREATE TYPE type AS ENUM ('Work', 'Education', 'Service', 'Accomplishment')")
create_exp_query = '''CREATE TABLE IF NOT EXISTS Experience (id SERIAL PRIMARY KEY NOT NULL, contact_id INTEGER NOT NULL\
                      , host VARCHAR(100) NOT NULL, title VARCHAR(100) NOT NULL, date_start DATE NOT NULL, date_end DATE\
                      , date_length INTEGER, type type NOT NULL, description VARCHAR(500), FOREIGN KEY(contact_id) \
                      REFERENCES Contact(id));'''
cursor.execute(create_exp_query)
conn.commit()
conn.close()
cursor.close()
