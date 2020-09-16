## Staging branch `staging-filter-and-search`
Creates an endpoint to filter candidates based on their profile and skills


### Branch `feature-filter-endpoint-setup`
Sets up basic structure for filtering and searching

#### Changes

- Adds Filter.py and creates input and output schema for filter endpoint
- Creates endpoint `POST api/contacts/filter`
- Creates test_filter.py to test the filter endpoint
- Adds `program_name` to ProgramAppSchema
- Removes stray `print()` statements from the Resources

### Branch `feature-add-profile-filters`
Adds filter for the fields stored in tables related to the `profile` table

#### Changes

- Adds `gender` to the response body for `POST api/contacts/filter`
- Accepts fields stored directly on the `profile` as filter criteria:
    - `years_exp`
    - `job_search_status`
    - `current_job_status`
    - `current_edu_status`
    - `previous_bcorps_program`
    - `hear_about_us`

### Branch `feature-add-profile-related-criteria`
Adds filter for the fields stored directly in the `profile` table

#### Changes

- Adds `city` and `state` to the response body for `POST api/contacts/filter`
- Accepts fields stored on tables related to the `profile` as filter criteria:
    - `programs_completed`
    - `roles`

### Branch `feature-add-program-apps-filter`
Adds filter for the `program-apps` associated with a contact

#### Changes

- Accepts `program_apps` as a filter criteria
- Removes the `name` as a required field for `ProgramSchema`

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend first
