CREATE TYPE contact_gender AS ENUM ('Male', 'Female', 'Non-binary', 'Not Listed');
CREATE TYPE contact_race AS ENUM ('Asian', 'White', 'Black', 'Hispanic/Latinx');
CREATE TYPE contact_salutation AS ENUM ('Ms.', 'Miss', 'Mr.', 'Mrs.', 'Dr.');

CREATE TABLE contact (
     id            SERIAL PRIMARY KEY NOT NULL,
     first_name    VARCHAR(100) NOT NULL,
     last_name     VARCHAR(100) NOT NULL,
     phone_primary VARCHAR (25),
     gender        contact_gender,
     race_all      contact_race,
     birthdate     DATE,
     salutation    contact_salutation
  );

CREATE TYPE email_type AS ENUM ('Personal', 'Work');

CREATE TABLE email
  (
     id         SERIAL PRIMARY KEY NOT NULL,
     contact_id INTEGER NOT NULL,
     is_primary BOOL DEFAULT false,
     email      VARCHAR(100) NOT NULL,
     type       email_type DEFAULT 'Work',
     FOREIGN KEY(contact_id) REFERENCES contact(id)
  );

CREATE TYPE address_type AS ENUM ('Home', 'Work');
CREATE TYPE address_status AS ENUM ('Active', 'Inactive');

CREATE TABLE address
  (
     id          SERIAL PRIMARY KEY NOT NULL,
     contact_id  INTEGER NOT NULL,
     is_primary  BOOL DEFAULT false,
     street1     VARCHAR(200) NOT NULL,
     street2     VARCHAR(200),
     city        VARCHAR(100) NOT NULL,
     state       VARCHAR(100) NOT NULL,
     country     VARCHAR(100) NOT NULL,
     postal_code VARCHAR(10) NOT NULL,
     type        address_type DEFAULT 'Home',
     status      address_status DEFAULT 'Active',
     FOREIGN KEY(contact_id) REFERENCES contact(id)
  ); 

CREATE TYPE exp_type AS ENUM ('Work', 'Education', 'Service', 'Accomplishment');
CREATE TYPE exp_type_host AS ENUM ('Nonprofit', 'Education', 'Government', 'Corporate');
CREATE TYPE exp_status AS ENUM ('Active', 'Inactive');
CREATE TYPE exp_stage AS ENUM ('Current', 'Former');
CREATE TYPE exp_degree AS ENUM ('High School','Associates','Undergraduate','Masters','Doctoral');

CREATE TABLE experience
  (
     id           SERIAL PRIMARY KEY NOT NULL,
     contact_id   INTEGER NOT NULL,
     address_id   INTEGER,
     host         VARCHAR(100) NOT NULL,
     title        VARCHAR(100) NOT NULL,
     date_start   DATE NOT NULL,
     date_end     DATE,
     date_length  INTEGER,
     type         exp_type NOT NULL,
     type_host    exp_type_host,
     description  VARCHAR(500),
     hours_weekly INTEGER,
     hours_total  INTEGER,
     status       exp_status,
     stage        exp_stage,
     score        DECIMAL,
     degree       exp_degree,
     FOREIGN KEY(contact_id) REFERENCES contact(id),
     FOREIGN KEY(address_id) REFERENCES address(id)
  );

CREATE TABLE achievement
  (
     id                SERIAL PRIMARY KEY NOT NULL,
     exp_id            INTEGER,
     contact_id        INTEGER NOT NULL,
     description       VARCHAR(500) NOT NULL,
     achievement_order INTEGER NOT NULL,
     FOREIGN KEY(exp_id) REFERENCES experience(id),
     FOREIGN KEY(contact_id) REFERENCES contact(id)
  ); 

CREATE TYPE tag_type AS ENUM ('Function', 'Skill', 'Topic');
CREATE TYPE tag_status AS ENUM ('Active', 'Inactive');

CREATE TABLE tag
  (
     id     SERIAL PRIMARY KEY NOT NULL,
     name   VARCHAR(100) NOT NULL,
     type   tag_type NOT NULL,
     status tag_status
  ); 

CREATE TABLE tag_item
  (
     id             SERIAL PRIMARY KEY NOT NULL,
     contact_id     INTEGER NOT NULL,
     tag_id         INTEGER NOT NULL,
     score          DECIMAL,
     tag_item_order INTEGER NOT NULL,
     FOREIGN KEY(contact_id) REFERENCES contact(id),
     FOREIGN KEY(tag_id) REFERENCES tag(id)
  ); 

CREATE TABLE templates
  (
     id           SERIAL PRIMARY KEY NOT NULL,
     name         VARCHAR(100) NOT NULL,
     template_url VARCHAR(500) NOT NULL,
     json         VARCHAR(500) NOT NULL
  ); 

CREATE TABLE resume
  (
     id           SERIAL PRIMARY KEY NOT NULL,
     contact_id   INTEGER NOT NULL,
     name         VARCHAR(100) NOT NULL,
     template_id  INTEGER NOT NULL,
     date_created DATE NOT NULL,
     FOREIGN KEY(contact_id) REFERENCES contact(id),
     FOREIGN KEY(template_id) REFERENCES templates(id)
  );

CREATE TABLE resumesection
  (
     id               SERIAL PRIMARY KEY NOT NULL,
     resume_id        INTEGER NOT NULL,
     name             VARCHAR(100) NOT NULL,
     min_count        INTEGER,
     max_count        INTEGER,
     FOREIGN KEY(resume_id) REFERENCES resume(id)
  );

CREATE TABLE resumeitem
  (

     section_id       INTEGER NOT NULL,
     resume_order     SERIAL NOT NULL,
     exp_id           INTEGER NOT NULL,
     tag_id           INTEGER NOT NULL,
     achievement_id   INTEGER NOT NULL,
     indented         BOOL DEFAULT false,
     FOREIGN KEY(section_id) REFERENCES resumesection(id),
     FOREIGN KEY(exp_id) REFERENCES experience(id),
     FOREIGN KEY(tag_id) REFERENCES tag_item(id),
     PRIMARY KEY(section_id, resume_order)
  );



