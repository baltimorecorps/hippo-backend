## Staging branch `staging-submit-profile`
Creates the framework to track the completion status of a applicant's profile and creates an endpoint that replaces the role of the FormAssembly form in enabling an applicant to submit their profile


### Branch `feature-dynamic-instructions`
Creates the framework for tracking and reporting which sections of the profile an applicant has completed

#### Changes

- Creates endpoint `GET api/contacts/<contact_id>/instructions`
- {{change 2}}

### Branch `feature-submit-endpoint`
Creates the functionality for applicants to submit their profile, moving the card in Trello to the submitted stage

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
