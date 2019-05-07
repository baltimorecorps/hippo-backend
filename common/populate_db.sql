INSERT INTO contact (
    first_name,
    last_name,
    phone_primary,
    gender,
    race_all,
    birthdate,
    salutation
)
VALUES (
    'Billy',
    'Daly',
    '908-578-4622',
    'Male',
    'White',
    '1993-12-04',
    'Mr.'
);

INSERT INTO contact (
    first_name,
    last_name,
    phone_primary,
    gender,
    race_all,
    birthdate,
    salutation
)
VALUES (
    'Barack',
    'Obama',
    '123-456-7890',
    'Male',
    'Black',
    '1961-08-04',
    'Mr.'
);

INSERT INTO tag (
     name,
     type,
     status
  )
 VALUES (
    'Python',
    'Skill',
    'Active'
);

INSERT INTO tag (
    name,
    type,
    status
)
VALUES (
    'Web Development',
    'Function',
    'Active'
);

INSERT INTO tag (
    name,
    type,
    status
)
VALUES (
    'Public Health',
    'Topic',
    'Active'
);

INSERT INTO experience (
    contact_id,
    host,
    title,
    date_start,
    type
)
VALUES (
    1,
    'Baltimore Corps',
    'Data Analyst',
    '2015-09-01',
    'Work'
);

INSERT INTO experience (
    contact_id,
    host,
    title,
    degree,
    date_start,
    date_end,
    type
)
VALUES (
    1,
    'Goucher College',
    'Economics',
    'Undergraduate',
    '2012-09-01',
    '2016-05-20',
    'Education'
);
INSERT INTO tag_item (
    contact_id,
    tag_id,
    score
)
VALUES (
    1,
    1,
    2
);
INSERT INTO tag_item (
    contact_id,
    tag_id,
    score
)
VALUES (
    2,
    3,
    4
);
INSERT INTO tag_item (
    contact_id,
    tag_id,
    score
)
VALUES (
    1,
    2,
    3
);
