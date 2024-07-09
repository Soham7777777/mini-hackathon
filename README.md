## Purpose of this project:
---

- To provide a minimal template with just enough file structure and code to get started with any flask project.

## Some Important steps before using this template:
---

- Remove comment for instance directory in `.gitignore` file.

- The production server "Gunicorn" does not support Windows, so make sure to use Windows compitable server in deployment.

- The Gunicorn is best to use behind a HTTP proxy server, the [documentation](https://gunicorn.org/#deployment) recommends using [nginx](https://nginx.org/en/docs/?_ga=2.159836926.2108447914.1714109557-1622351325.1714109557).

- Read [this](https://flask.palletsprojects.com/en/3.0.x/deploying/) document before deploying to production.

## How to run this Softwere:
---

### Create Virtual Environment

- Open command-line in the project directory e.g. The directory where this README.md is by default.

- run `python -m venv pyenv` to create virtual envorinment

- Activate virtual environment:
    Linux : `source pyenv/bin/activate`
    Windows: `.\Scripts\activate.bat`

- Run `pytest -v -vv -rA` to run tests. All test will run in Testing mode except the test_factory.

- Run `python debug.py` to run python on debug mode.

- Alternatively, Run `gunicorn -w 8 'run:wsgiapp'` to run in production mode. This will not work for Windows as mentioned in above section.

## Testing:
---

- `rm ./instance/*.db;coverage erase;coverage run --include='Application/**,instance/**,tests/**/test*.py' -m pytest -vv -rA;coverage report;coverage html`


## Testing guide by Soham:
---

- JUST DON'T TEST DAMM CONFIGS PARTS OF CODE BECAUSE THEY ARE THE ONLY SOURCE OF TRUTH, DON'T TEST CODE SIMPLE AS THESE:
    - field configs of schema classes, model cofigs from mapped classes, app configs from `create_app()` and instance package, and blueprint configs from Blueprint objects

- ACHIEVE 100% COVERAGE BUT IT DOES NOT MEAN BUGFREE RATHER ITS REQUIREMENT, THE COVERAGE BOUNDRY MUST INCLUDE TESTING CODE AS WELL. 

- FIRST WRITE TESTING CODE AND CONFIG CODE THEN WRITE APPLICAITON CODE
    - write testing code for code which has testcases and code that changes other things, write testing code to check if it behaves in the way you wanted. 