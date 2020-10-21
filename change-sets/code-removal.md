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


### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Frontend first
