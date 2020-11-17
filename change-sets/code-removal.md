## Staging branch `staging-code-removal`
Removes sections of the code that are no longer in use


### Branch `feature-endpoint-removal`
Removes endpoints from api.py and the tests that reference those endpoints in test_api.py

#### Changes

- Removes the following endpoints:
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
- Removes the following tests:
  - `test_put()` for `api/contacts/123/programs/1/`
  - `test_put_rejects_id_update()` for `/api/contacts/123/programs/1/`
  - `test_approve_many_program_contacts_new()`
  - `test_approve_many_program_contacts_existing()`
  - `test_reapprove_many_program_contacts()`
  - `test_approve_program_contact_fake_contact()`
  - `test_get()` for `/api/contacts/123/programs/1`
  - `test_get_many_unordered()` for `/api/contacts/123/achievements/`
  - `test_get_many_unordered()` for `/api/contacts/123/programs/`
  - `test_post()` for `/api/contacts/124/programs/`


### Branch `feature-file-removal`
Removes the `resources/` and `models/` files that were referenced by the endpoints deleted

#### Changes

- Removes the following files from the `resources` folder:
  - `FormAssembly.py`
  - `ProgramContacts.py`
  - `Resume.py`
  - `Tag.py`
  - `generate_resume.py`
  - `Achievement.py`
- Removes the `docs-example` folder and the constituent files
- Removes the following directory level files:
  - `migrate_skills_to_capabilities.py`
  - `get_skill_id.py`
- Removes the following files from `models` folder:
  - `old_skill_model.py`
  - `resume_item_model.py`
  - `resume_section_model.py`
  - `tag_item.py`
  - `tag_model.py`
  - `templates_model.py`
  - Model and schemas related to `Resume` in `resume_model.py`
- Comments out references to `ProgramContact` in the following files:
  - `api.py`
  - `contact_model.py`
  - `program_model.py`
  - `Contacts.py`
  - `Profile.py`
  - `ProgramApp.py`
  - `program_data.py`
  - `populate_db.py`
  - `test_api.py`


### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** Yes
  - Removes `old_skill_model` table
  - Removes `resume_item_model` table
  - Removes `resume_section` table
  - Removes `resume` table
  - Removes `tag_item` table
  - Removes `tag` table
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Frontend first
