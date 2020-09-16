## Staging branch `staging-race-table-update`
This branch adds a new field `race_all` to the `race` table to make it easier to report on which racial identities were selected by each candidate


### Branch `feature-add-race-text-field`
Adds `race_all` field to `race` table and sets it when the `race` table is updated

#### Changes

- Creates new test `test_put_about_me_race_all()`
- Adds `race_all` to `race`

### Branch `feature-add-race-to-filter-endpoint`
Adds the `race` field to the `POST api/contacts/filter` endpoint

#### Changes

- Adds `race` to `test_basic_filter()` in `test_filter.py`
- Updates `POST api/contacts/filter` to include `race` in the response body
- Configures `join()` for precisely in the query

### Branch `feature-bug-filter-endpoint`
Fixes a bug that caused duplicate contacts to be returned when passing multiple programs in the filter payload

#### Changes

- Adds a test to recreate the duplicate bug
- Turns the `program_app` query into a subquery to avoid duplication


### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** Yes
    - Adds `race_all` to `race` table
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend first
