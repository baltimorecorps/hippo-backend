## Staging branch `staging-submit-profile`
Creates the framework to track the completion status of a applicant's profile and creates an endpoint that replaces the role of the FormAssembly form in enabling an applicant to submit their profile


### Branch `feature-dynamic-instructions`
Creates the framework for tracking and reporting which sections of the profile an applicant has completed

#### Changes

- Creates endpoint `GET api/contacts/<contact_id>/instructions`
- Creates a set of `hybrid_property` fields to calculate the completeness of each section of the profile

### Branch `feature-submit-endpoint`
Creates the functionality for applicants to submit their profile, moving the card in Trello to the submitted stage

#### Changes

- Creates endpoint `POST contacts/<contact_id>/submit` which checks to make sure all of the sections are complete then submits the profile
- When the profile is submitted, the status is updated to `submitted` and the Trello card associated with that contact is moved to the "Application Submitted" list
- Adds `card_id` to the `contact` table to store the id of the trello card
- Sets the `card_id` field when a contact is created

### Branch `bug-dynamic-instructions`
Fixes issues with how the instructions were calculated

#### Changes

- Changes the logic of how the completeness of the `about_me` section is calculated to remain consistent with the required fields on each section of the form
- Fixes a bug in how the completeness of the `add_skills` section is calculated so that skills that were added and then later deleted don't count toward the minimum 3

### Branch `feature-full-profile-endpoint`
Adds a new endpoint to return all of the data needed to populate the profile

#### Changes

- Creates `GET api/contacts/<contact_id>/profile` which returns all of the data needed to populate the profile
- Updates `GET api/contacts/<contact_id>/submit` to `GET api/contacts/<contact_id>/profile/submit` to standardize naming conventions

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** Yes
    - Adds `card_id` to `contact` table
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend First
