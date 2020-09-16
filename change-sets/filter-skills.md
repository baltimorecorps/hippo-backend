## Staging branch `staging-filter-skills`
Adds skills as an optional paramater for `POST api/contacts/filter`

### Changes
- Removes `trello_check.py` from directory
- Updates `POST api/contacts/filter` to accept `skills` as part of the query payload

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend First
