## Staging branch `staging-race-table-update`
This branch adds a new field `race_all` to the `race` table to make it easier to report on which racial identities were selected by each candidate


### Branch `feature-add-race-text-field`
Adds `race_all` field to `race` table and sets it when the `race` table is updated

#### Changes

- Creates new test `test_put_about_me_race_all()`
- Adds `race_all` to `race`

### Branch `feature-branch-two`
{{overview of functionality added in this feature branch}}

#### Changes

- {{change 1}}
- {{change 2}}

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** Yes
    - Adds `race_all` to `race` table
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend first
