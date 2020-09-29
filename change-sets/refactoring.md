## Staging branch `staging-refactoring`
This branch refactors the code base, beginning with tests


### Branch `feature-refactor-tests`
Moves test data out of `test_api.py` and populates the db using that test data rather than through explicit init statements in `populate_db.py`

#### Changes

- Removes everything but `POSTS` and `CONTACTS` from `test_api.py`
- Creates a `tests/data/` folder with a file for each group of related resources

### Branch `feature-code-removal-notes`
Adds `# TODO: DELETE THIS` comments next to each of the sections of code that can be removed

#### Changes

- Adds comments to following endpoints:
    - `/tags/`
    - `/tags/<int:tag_id>`
    - `/contacts/<int:contact_id>/tags/`
    - `/contacts/<int:contact_id>/tags/<int:tag_id>`
    - `/contacts/<int:contact_id>/achievements/`
    - `/contacts/<int:contact_id>/resumes/`
    - `/resumes/<int:resume_id>/`
    - `/resumes/<int:resume_id>/sections/`
    - `/resumes/<int:resume_id>/sections/<int:section_id>`
    - `/contacts/<int:contact_id>/generate-resume/`
    - `/contacts/<int:contact_id>/programs`
    - `/contacts/<int:contact_id>/programs/<int:program_id>`
    - `/programs/<int:program_id>/contacts/approve-many`
- Adds comments to the following files
    - `migrate_skills_to_capabilities.py`
    - `old_skill_model.py`
    - `program_contact_model.py`
    - `resume_item_model.py`
    - `resume_model.py`
    - `resume_section_model.py`
    - `tag_item_model.py`
    - `tag_model.py`
    - `templates_model.py`
    - `Achievement.py`
    - `ProgramContacts.py`
    - `Resume.py`
    - `Tag.py`

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend independent of frontend
