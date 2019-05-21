DROP TABLE IF EXISTS contact CASCADE;
DROP TABLE IF EXISTS email CASCADE;
DROP TABLE IF EXISTS address CASCADE;
DROP TABLE IF EXISTS experience CASCADE;
DROP TABLE IF EXISTS achievement CASCADE;
DROP TABLE IF EXISTS tag CASCADE;
DROP TABLE IF EXISTS tag_item CASCADE;
DROP TABLE IF EXISTS template CASCADE;
DROP TABLE IF EXISTS resume CASCADE;
DROP TABLE IF EXISTS resume_section CASCADE;
DROP TABLE IF EXISTS resume_item CASCADE;

DROP TYPE IF EXISTS contact_gender;
DROP TYPE IF EXISTS contact_race;
DROP TYPE IF EXISTS contact_salutation;
DROP TYPE IF EXISTS email_type;
DROP TYPE IF EXISTS address_type;
DROP TYPE IF EXISTS address_status;
DROP TYPE IF EXISTS exp_type;
DROP TYPE IF EXISTS exp_status;
DROP TYPE IF EXISTS exp_degree;
DROP TYPE IF EXISTS tag_type;
DROP TYPE IF EXISTS tag_status;

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
     description  VARCHAR(500),
     type         exp_type NOT NULL,
     degree       exp_degree,
     FOREIGN KEY(contact_id) REFERENCES contact(id),
     FOREIGN KEY(address_id) REFERENCES address(id)
  );

CREATE TABLE achievement
  (
     id                SERIAL PRIMARY KEY NOT NULL,
     exp_id            INTEGER NOT NULL,
     contact_id        INTEGER NOT NULL,
     description       VARCHAR(500) NOT NULL,
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
     score          INTEGER,
     FOREIGN KEY(contact_id) REFERENCES contact(id),
     FOREIGN KEY(tag_id) REFERENCES tag(id)
  );

CREATE TABLE template
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
     date_created DATE NOT NULL,
     FOREIGN KEY(contact_id) REFERENCES contact(id)
  );

CREATE TABLE resume_section
  (
     id               SERIAL PRIMARY KEY NOT NULL,
     resume_id        INTEGER NOT NULL,
     name             VARCHAR(100) NOT NULL,
     min_count        INTEGER,
     max_count        INTEGER,
     FOREIGN KEY(resume_id) REFERENCES resume(id)
  );

CREATE TABLE resume_item
  (
     resume_id        INTEGER NOT NULL,
     section_id       INTEGER NOT NULL,
     resume_order     INTEGER,
     exp_id           INTEGER,
     tag_id           INTEGER,
     achievement_id   INTEGER,
     indented         BOOL DEFAULT false,
     FOREIGN KEY(section_id) REFERENCES resume_section(id),
     FOREIGN KEY(exp_id) REFERENCES experience(id),
     FOREIGN KEY(tag_id) REFERENCES tag_item(id),
     FOREIGN KEY(resume_id) REFERENCES resume(id),
     PRIMARY KEY(section_id, resume_order)
  );
