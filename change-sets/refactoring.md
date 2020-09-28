## Staging branch `staging-refactoring`
This branch refactors the code base, beginning with tests


### Branch `feature-refactor-tests`
Moves test data out of `test_api.py` and populates the db using that test data rather than through explicit init statements in `populate_db.py`

#### Changes

- Removes everything but `POSTS` and `CONTACTS` from `test_api.py`
- Creates a `tests/data/` folder with a file for each group of related resources

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend independent of frontend
