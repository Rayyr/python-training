# Git Branching Strategy & Milestones

## Branches

### `main`
Stable branch. Only tested, reviewed work should be merged here.

### `dev`
Integration branch for the current development cycle.

### `feature/*`
Short-lived branches for individual features.

Examples:

- `feature/role-based-users`
- `feature/student-course-relationship`
- `feature/profile-picture-upload`
- `feature/course-enrollment-api`
- `feature/student-search-pagination`

## Workflow

```text
main
  │
  └── dev
       ├── feature/role-based-users
       ├── feature/student-course-relationship
       ├── feature/profile-picture-upload
       ├── feature/course-enrollment-api
       └── feature/student-search-pagination
```

## Milestones

### Milestone 1 — Architecture
- [x] Review Day 3 repository
- [x] Define requirements
- [x] Define branch strategy
- [x] Define database schema
- [x] Document API

### Milestone 2 — Data model
- [x] Add user roles
- [x] Link User to Student
- [x] Add Student-Course many-to-many relationship

### Milestone 3 — Application features
- [x] Profile picture upload
- [x] Course enrollment API
- [x] Student search
- [x] Student pagination

### Milestone 4 — Verification
- [ ] Run the app
- [ ] Seed demo data
- [ ] Test all roles
- [ ] Test profile upload
- [ ] Test enrollment endpoint
- [ ] Test search and pagination
- [ ] Merge feature branches into `dev`
- [ ] Review and merge `dev` into `main`

## Commit examples

```text
feat: add user role support
feat: add student course many-to-many relationship
feat: add profile picture upload
feat: add course enrollment endpoint
feat: add student search and pagination
docs: add database schema and API specification
```
