import pytest

from app.users.models import User
from app.db import get_session

USER_EMAIL = "test@test.com"
USER_PASSWORD = "test"

@pytest.fixture(scope="module")
def setup():
    session = get_session()
    yield session
    q=User.objects().filter(email=USER_EMAIL)
    if q.count() > 0:
        q.delete()
    session.shutdown()

def test_user_create(setup):
    User.create_user(email=USER_EMAIL, password=USER_PASSWORD)

def test_user_duplicate(setup):
    with pytest.raises(Exception):
        User.create_user(email=USER_EMAIL, password=USER_PASSWORD)

def test_user_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@t', password=USER_PASSWORD)
        
def test_user_verify_password(setup):
    q = User.objects().filter(email=USER_EMAIL)
    assert q.count() == 1
    user = q.first()
    assert user.verify_password(USER_PASSWORD) == True
    assert user.verify_password(f"{USER_PASSWORD}1") == False