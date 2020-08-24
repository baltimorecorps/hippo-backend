## Staging branch `staging-maintenance-api`
Addresses some performance issues within the web app and some minor refactoring and also adds some missing endpoints to support frontend capabilities


### Branch `bug-contact-programs-performance`
{{overview of functionality added in this feature branch}}

#### Changes

- Changes the filtering mechanism for `GET api/contacts/programs` to improve response times
- Creates endpoint `GET api/contacts/program-apps` which returns the new format for program applications and will eventually replace `GET api/contacts/programs`

### Branch `feature-session-cleanup`
Cleans up the `GET api/session` endpoint and simplifies contact schemas

#### Changes

- Replaces `ContactSchema` with `ContactShortSchema` in the `UserSessionSchema`
- Add `status`, `account_id`, `phone_primary` to `ContactShortSchema`
- Removes `ContactProgramSchema`
- Removes `GET api/internal/applications` endpoint

### Branch `feature-email-test`
Writes a test to see if `POST api/contacts` will break if it doesn't receive `email_primary` in the payload

#### Changes

- Moves `test_post_contact` and other related tests from `trello_integration_test.py` to `test_api.py`
- Tests that passing `email` instead of `email_primary` doesn't break the `POST api/contacts` endpoint

### Deployment Considerations

- **Heroku Variables:** {{Yes/No}}
    - {{variable 1}}
    - {{variable 2}}
- **DB Migrations:** {{Yes/No}}
    - {{change 1}}
    - {{change 2}}
- **AuthZ/N Changes:** {{Yes/No}}
    - {{change 1}}
    - {{change 2}}
- **Deployment Sequence:** {{Backend/Frontend First}}
