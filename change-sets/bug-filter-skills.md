## Staging branch `bug-filter-skills`
Contacts with deleted skills are still be returned by the filter.

#### Changes

- Creates test to check for exclusion of deleted skills from search
- Adds `filter(is_deleted=False)` to the skills subquery

### Branch `feature-branch-two`
{{overview of functionality added in this feature branch}}

#### Changes

- {{change 1}}
- {{change 2}}

### Deployment Considerations

- **Heroku Variables:** No
- **DB Migrations:** No
- **AuthZ/N Changes:** No
- **Deployment Sequence:** Backend First
