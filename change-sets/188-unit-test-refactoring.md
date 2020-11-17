## Staging branch `staging-188-unit-test-refactoring`
Refactors test_api.py file into separate unit test files. References issue #188


### Branch `feature-delete-program-contact-table`
Deletes `program_contact` table from DB and related files in the codebase.

#### Changes

- Modifies the following files with references to `program_contact`
  - `api.py`
  - `models/contact_model.py`
  - `models/program_model.py`
  - `resources/Contacts.py`
  - `resources/Profile.py`
  - `resources/ProgramApp.py`
  - `tests/populate_db.py`
  - `tests/test_api.py`
- Deletes `models/program_contact_model.py`

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** Yes
  - Removes `program_contact` table
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Frontend First
