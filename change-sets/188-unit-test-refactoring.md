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


### Branch `feature-new-test-setup`
Sets up the new structure for api unit tests

#### Changes

- Reorganizes the tests into the following structure:
  - capability
    - `test_capability.py`
  - contact
    - `contact_data.py`
    - `test_contact.py`
  - experience
    - `experience_data.py`
    - `test_experience.py`
  - filter
    - `test_filter.py`
  - integrations
    - `trello_integration_test.py`
  - opportunity
    - `opportunity_data.py`
    - `test_opportunity.py`
  - opportunity_app
    - `test_opportunity_app.py`
  - profile
    - `profile_data.py`
    - `test_profile.py`
  - program
    - `program_data.py`
    - `test_program.py`
  - program_app
    - `test_program_app.py`
  - session
    -  `test_session.py`
  - skill
    - `test_skills.py`
- Copies the resource methods into each of the corresponding test files in those sub directories


### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** Yes
  - Removes `program_contact` table
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Frontend First
