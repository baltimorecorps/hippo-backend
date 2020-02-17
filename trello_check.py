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
    'local': '5e3753cdaea77d37fce3496a',
    'dev': '5e39bb0daf879105b1c24462',
    'production': '',
}

OPP_BOARDS = {
    'local': '5e4acd35a35ee523c71f9e25',
    'dev': '',
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

def check_opportunity_board_custom_fields(env):
    board_id = OPP_BOARDS[env]
    board = Board(query_board_data(board_id))
    gdoc_id = board.custom_fields['name'].get('Google Doc ID')
    assert gdoc_id is not None
    assert gdoc_id.type == 'text'

    opp_id = board.custom_fields['name'].get('Opp ID')
    assert opp_id is not None
    assert opp_id.type == 'text'

def check_opportunity_board_lists(env):
    board_id = OPP_BOARDS[env]
    board = Board(query_board_data(board_id))
    BOARD_NAMES = [ 
        'Started',
        'Submitted',
        'Approved',
        'Posted',
        'Interviewing',
        'Filled',
    ]
    for stage, name in enumerate(BOARD_NAMES):
        list_ = board.lists['stage'][stage]
        assert list_.name == name, f'At stage {stage}, {list_.name} != {name}'


def main(env):
    app = create_app(env)
    with app.app_context():
        check_review_options(env)
        check_opportunity_board_custom_fields(env)
        check_opportunity_board_lists(env)

if __name__ == '__main__':
    import sys
    main_argv = sys.argv[1]
    main(main_argv)
