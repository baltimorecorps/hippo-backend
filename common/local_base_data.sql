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


