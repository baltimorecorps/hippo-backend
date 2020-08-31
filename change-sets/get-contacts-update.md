## Staging branch `staging-get-contacts-update`
Combines `GET api/contacts/` and `GET api/contacts/short` and allows filtering of that list based on `status`


### Branch `feature-combine-contact-endpoints`
Updates `GET api/contacts` to point to the same resource as `GET api/contacts/short`

#### Changes

- Removes `get()` method from `ContactsAll` resource class in `resources/Contacts.py`
- Adds `/api/contacts` as a route which maps to `ContactShort` resource class
- Adds filtering of contacts by `status`

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend First
