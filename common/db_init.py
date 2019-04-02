import psycopg2

conn = psycopg2.connect(user="newuser",
                        password="password",
                        host="127.0.0.1",
                        port="5432",
                        database="mydb")
cursor = conn.cursor()

cursor.execute("CREATE TYPE contact_gender AS ENUM ('Male', 'Female', 'Non-binary', 'Not Listed')")
cursor.execute("CREATE TYPE contact_race AS ENUM ('Asian', 'White', 'Black', 'Hispanic/Latinx')")
cursor.execute("CREATE TYPE contact_salutation AS ENUM ('Ms.', 'Miss', 'Mr.', 'Mrs.', 'Dr.')")

create_table_query = '''CREATE TABLE contact (id SERIAL PRIMARY KEY NOT NULL, first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL, phone_primary
                        VARCHAR (25), gender contact_gender,
                        race_all contact_race, birthdate DATE, salutation contact_salutation) ;'''
cursor.execute(create_table_query)
conn.commit()

cursor.execute("CREATE TYPE email_type AS ENUM ('Personal', 'Work')")

create_email_query = '''CREATE TABLE email (id SERIAL PRIMARY KEY NOT NULL, contact_id INTEGER NOT NULL, is_primary
                        BOOL DEFAULT FALSE, email VARCHAR(100) NOT NULL, type email_type DEFAULT 'Work',
                        FOREIGN KEY(contact_id) REFERENCES Contact(id));'''
cursor.execute(create_email_query)
conn.commit()

cursor.execute("CREATE TYPE address_type AS ENUM ('Home', 'Work')")
cursor.execute("CREATE TYPE address_status AS ENUM ('Active', 'Inactive')")

create_address_query = '''CREATE TABLE address (id SERIAL PRIMARY KEY NOT NULL, contact_id INTEGER NOT NULL,
                          is_primary BOOL DEFAULT FALSE, street1 VARCHAR(200) NOT NULL, street2 VARCHAR(200), city
                          VARCHAR(100) NOT NULL, state VARCHAR(100) NOT NULL, country VARCHAR(100) NOT NULL,
                          postal_code VARCHAR(10) NOT NULL, type address_type DEFAULT 'Home', status address_status
                          DEFAULT 'Active', FOREIGN KEY(contact_id) REFERENCES Contact(id));'''
cursor.execute(create_address_query)
conn.commit()

cursor.execute("CREATE TYPE exp_type AS ENUM ('Work', 'Education', 'Service', 'Accomplishment')")
cursor.execute("CREATE TYPE exp_type_host AS ENUM ('Nonprofit', 'Education', 'Government', 'Corporate')")
cursor.execute("CREATE TYPE exp_status AS ENUM ('Active', 'Inactive')")
cursor.execute("CREATE TYPE exp_stage AS ENUM ('Current', 'Former')")

create_exp_query = '''CREATE TABLE experience (id SERIAL PRIMARY KEY NOT NULL, contact_id INTEGER NOT NULL, address_id
                      INTEGER, host VARCHAR(100) NOT NULL, title VARCHAR(100) NOT NULL, date_start DATE NOT NULL,
                      date_end DATE, date_length INTEGER, type exp_type NOT NULL, type_host exp_type_host, description
                      VARCHAR(500), hours_weekly INTEGER, hours_total INTEGER, status exp_status,
                      stage exp_stage, score DECIMAL, FOREIGN KEY(contact_id) REFERENCES Contact(id),
                      FOREIGN KEY(address_id) REFERENCES Address(id));'''
cursor.execute(create_exp_query)
conn.commit()

create_achievement_query= '''CREATE TABLE achievement (id SERIAL PRIMARY KEY NOT NULL, exp_id INTEGER NOT NULL,
                             description VARCHAR(500) NOT NULL, achievement_order INTEGER NOT NULL, FOREIGN KEY(exp_id)
                             REFERENCES Experience(id));'''
cursor.execute(create_achievement_query)
conn.commit()

cursor.execute("CREATE TYPE tag_type AS ENUM ('Function', 'Skill', 'Topic')")
cursor.execute("CREATE TYPE tag_status AS ENUM ('Active', 'Inactive')")

create_tag_query = '''CREATE TABLE tag (id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(100) NOT NULL,
                      status tag_status);'''
cursor.execute(create_tag_query)
conn.commit()

create_tag_item_query = '''CREATE TABLE tag_item (id SERIAL PRIMARY KEY NOT NULL, contact_id INTEGER NOT NULL, tag_id
                           INTEGER NOT NULL, score DECIMAL, tag_item_order INTEGER NOT NULL, FOREIGN KEY(contact_id)
                           REFERENCES Contact(id), FOREIGN KEY(tag_id) REFERENCES Tag(id));'''
cursor.execute(create_tag_item_query)
conn.commit()

create_resume_template_query = '''CREATE TABLE resume_template (id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(100) NOT
                                  NULL, template_url VARCHAR(500) NOT NULL, description VARCHAR(500) NOT NULL);'''
cursor.execute(create_resume_template_query)
conn.commit()

create_resume_query = '''CREATE TABLE resume (id SERIAL PRIMARY KEY NOT NULL, contact_id INTEGER NOT NULL, name
                         VARCHAR(100) NOT NULL, template_id INTEGER NOT NULL, date_created DATE NOT NULL,
                         FOREIGN KEY(contact_id) REFERENCES Contact(id), FOREIGN KEY(template_id) REFERENCES
                         Resume_Template(id));'''
cursor.execute(create_resume_query)
conn.commit()

create_resume_experience_query = '''CREATE TABLE resume_experience (id SERIAL PRIMARY KEY NOT NULL, resume_id INTEGER
                                    NOT NULL, exp_id INTEGER NOT NULL, date_start DATE NOT NULL, date_end DATE, score
                                    DECIMAL, resume_exp_order INTEGER NOT NULL, FOREIGN KEY(resume_id) REFERENCES Resume(id),
                                    FOREIGN KEY(exp_id) REFERENCES Experience(id));'''
cursor.execute(create_resume_experience_query)
conn.commit()

create_resume_tag_query = '''CREATE TABLE resume_tag (id SERIAL PRIMARY KEY NOT NULL, resume_id INTEGER NOT NULL,
                             tag_item_id INTEGER NOT NULL, score DECIMAL, resume_tag_order INTEGER NOT NULL, FOREIGN KEY(resume_id)
                             REFERENCES Resume(id), FOREIGN KEY(tag_item_id) REFERENCES Tag_Item(id));'''
cursor.execute(create_resume_tag_query)
conn.commit()

create_resume_achievement_query = '''CREATE TABLE resume_achievement (id SERIAL PRIMARY KEY NOT NULL, resume_id INTEGER
                                   NOT NULL, resume_tag_id INTEGER NOT NULL, resume_exp_id INTEGER NOT NULL,
                                   achievement_id INTEGER NOT NULL, score DECIMAL, resume_achievement_order INTEGER
                                   NOT NULL, FOREIGN KEY(resume_id) REFERENCES Resume(id), FOREIGN KEY(resume_tag_id)
                                   REFERENCES Resume_Tag(id), FOREIGN KEY(resume_exp_id) REFERENCES
                                   Resume_Experience(id), FOREIGN KEY(achievement_id) REFERENCES Achievement(id));'''
cursor.execute(create_resume_achievement_query)
conn.commit()
conn.close()
cursor.close()
