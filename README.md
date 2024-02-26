# TUS: open protocol for resumable file upload

this is a toy project for practicing tdd and maby other things
using flask to implement tus protocol

## install & run

### requirements
- python==3.12.2
- Flask==3.0.2
- flask-restx==1.3.0

### install python packages
- `make install`

### run in dev mode
- `make dev-run`

### install testing libary & run test
- `make test`

### run python static typing check (mypy)
- `make mypy`

### run all checks
- `make check`


## TODO

### backend
- [x] using [application factories](https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/) to organize project
- [ ] refactor flask config
- [ ] logging

- Entities
    - Chunk
    - TUS extension
    - TUS version
- Repository

### frontend
- React.js? or Vue.js?

### infra
- [ ] aws
    - terraform? pulumi?
    - ec2
    - app deploy?
    - rds?
