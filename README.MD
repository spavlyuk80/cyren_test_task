# Cyren test task

## Requirements

This code has been tested on Ubuntu 20.4 with Python 3.8.
Requires additional packages: pipenv, which could be installed with `pip install pipenv`

## Installation

1. Clone this repo
2. Create virtual environment with `pipenv shell` and install dependencies with 
`pipenv install`
3. run the `python task_runner.py -p /path/to/eml_message.eml`. If you do not specify
the path to eml file, it will default to `./test-mail.eml` or raises an error if there
is no such file

## Run

`python task_runner.py -p test-mail.eml`

The results are output into terminal

Use `task_runner.py -h` for some help on cli args

## Notes
- I did not run tests and some solutions are not generic enough (e.g. hardcoded paths or no fallback 
solutions for missing args)
- I did not add eml file for security reasons, since it is a public repository
