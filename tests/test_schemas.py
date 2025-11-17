# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from app.schemas import UserCreate


def test_user_create_valid():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }
    obj = UserCreate(**data)
    assert obj.username == "testuser"
    assert obj.email == "test@example.com"


def test_user_create_invalid_email():
    data = {
        "username": "testuser",
        "email": "not-an-email",
        "password": "password123",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_create_short_password():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "short",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)
