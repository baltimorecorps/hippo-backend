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

INSERT INTO program (
    name
)
VALUES (
    'Place for Purpose'
);

INSERT INTO question (
    program_id,
    question_text,
    limit_word
)
VALUES (
    1,
    'Racial Equity & Baltimore: Why is racial equity work in Baltimore important to you?',
    200
);

INSERT INTO question (
    program_id,
    question_text,
    limit_word
)
VALUES (
    1,
    'Sector Effectiveness: How has your background and experiences prepared you for today’s work in Baltimore’s social impact sector?',
    300
);

INSERT INTO cycle (
    program_id,
    date_start,
    date_end,
    intake_talent_board_id,
    intake_org_board_id,
    match_talent_board_id,
    match_opp_board_id,
    review_talent_board_id
)
VALUES (
    1,
    '2020-01-01',
    '2020-03-30',
    '5e37744114d9d01a03ddbcfe',
    'intake_org',
    'match_talent',
    'match_opp',
    '5e3753cdaea77d37fce3496a'
);
