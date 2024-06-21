import pytest
from instance import TestingConfiguration
from Application import create_app, db
from tests import nameValidationTestCases, passwordValidationTestCases
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from typing import Generator

@pytest.fixture
def app() -> Flask:
    app = create_app(configClass=TestingConfiguration)
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def database(app) -> Generator[SQLAlchemy, None, None]:
    with app.app_context():
        yield db

@pytest.fixture(params=[*nameValidationTestCases.items()])
def nameTestCase(request) -> list[tuple[str, str]]:
    return request.param

@pytest.fixture(params=[*passwordValidationTestCases.items()])
def passwordTestCase(request) -> list[tuple[str, str]]:
    return request.param