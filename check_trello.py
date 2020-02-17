from pprint import pprint
from app import create_app

# This only works because the script is at the top level
from resources.trello_utils import (
    query_board_data,
    Board,
    BoardList,
    Card,
)

REVIEW_BOARDS = {
    'local': '',
    'dev': '5e39bb0daf879105b1c24462',
    'production': '',
}

def check_review_options(env):
    """Check that the review options are set correctly
    (including spelling, etc.)
    """
    board_id = REVIEW_BOARDS[env]
    board = Board(query_board_data(board_id))
    options = board.custom_fields['name']['Reviewer Decision'].options
    opt_values = sorted(options['val'].keys())

    pprint(opt_values)
    assert opt_values == [
        'Approved', 
        'Approved with reservations',
        'Not a Fit',
    ]


def main(env):
    app = create_app(env)
    with app.app_context():
        check_review_options(env)

if __name__ == '__main__':
    main('dev')

