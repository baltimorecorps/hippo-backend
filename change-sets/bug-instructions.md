### Branch `bug-instructions-add-experiences-instructions`
Fixes bug in the `GET api/contacts/<contact_id>/instructions` endpoint

#### Changes

- Checks for `add_experience_complete['is_complete'] == True` instead of just `add_experience_complete == True` which was causing `profile_complete` to be returned as True even if there weren't any experiences


### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend independent of frontend
