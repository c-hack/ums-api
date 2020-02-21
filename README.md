# UMS Api
The api for the c-hack user management system

## Prerequesits
- python 3.7
- pipenv [python 3.7]

## Preparations:
```shell

# Setup pipenv and install dependencies
pipenv install --dev
#pipenv install #when not wanting dev depedencies.
```

## Start server for development:

First start:
```shell
source "$(pipenv --venv)/bin/activate"
export FLASK_APP=ums_api
export FLASK_DEBUG=1  # to enable autoreload
export MODE=debug
# export MODE=production
# export MODE=test

flask create_db

# start server
flask run
```

Subsequent starts:
```shell
flask run
```

### Shell.nix

Instead the file shell.nix can be used with the program nix-shell:
```shell
nix-shell
```
Then everything is set up for you and you only need to start the server:
```shell
flask run
```

## Installing in a Production Environment
See flask wsgi documentation. The preparations as shown above are required.
