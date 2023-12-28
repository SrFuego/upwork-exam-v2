# Upwork - Entry Exam

## Goal
Working FastAPI API with a User and Profile models and schemas.

## Instructions
1. Fork this repository
2. Complete the tasks below adhering to the requirements
3. Submit a pull request with your solution in your forked repository
4. Deliver a GitHub repository with your solution (it can be private, just give access to @arielaco)

## Tasks
- [x] Create a [User](###User) and [Profile](###Profile) models and schemas 
- [x] Develop a REST API exposing CRUD endpoints for both models
- [x] Test at least 2 endpoints using pytest (with fixtures)
- [x] Point docs to root path
- [x] Create requirements file
- [x] Add a section on `README.md` with setup (venv), install (pip), run and testing instructions

### User
- Email as username
- Can have multiple profiles
- Can have a list of favorite profiles

### Profile
- It has a name and a description
- Belongs to a user

## Requirements
- Use English for all code, comments, commit messages, and documentation
- Delete dead code (unrelated to tasks)
- All responses must be JSON
- Implement proper folder structure
- Validation must be done using Pydantic
- Use multiple commits (when possible, use conventional commit messages)

## Index of commands:

- [Index of commands:](#index-of-commands)
  - [Run the project](#run-the-project)
  - [Connect to the API container](#connect-to-the-api-container)
  - [Generate updated dependencies](#generate-updated-dependencies)

### Run the project

You must have Docker installed:

https://docs.docker.com/engine/install/

Set up the development environment:

`docker compose -f dockerfiles/docker-compose.yml up --build`


### Connect to the API container

`docker exec -it fastapi bash`


### Generate updated dependencies

In the container:

`bash scripts/update_requirements.sh`


### Generate BPMN diagram

Paste code from `docs/app.tree` to

https://www.bpmn-sketch-miner.ai/


### Generate coverage report

In the container:

`coverage run -m pytest`
`coverage html`