## Staging branch `staging-get-contacts-update`
Combines `GET api/contacts/` and `GET api/contacts/short` and allows filtering of that list based on `status`


### Branch `feature-combine-contact-endpoints`
Updates `GET api/contacts` to point to the same resource as `GET api/contacts/short`

#### Changes

- Removes `get()` method from `ContactsAll` resource class in `resources/Contacts.py`
- adds `/api/contacts` as a route which maps to `ContactShort` resource class

### Branch `feature-branch-two`
{{overview of functionality added in this feature branch}}

#### Changes

- {{change 1}}
- {{change 2}}

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
