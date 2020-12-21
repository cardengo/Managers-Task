import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


FAKE_USERS_DB = [
        # example: {'user_id': '15', 'password': 'admin'}
        {'': '', '': ''}
]


security = HTTPBasic()


def get_current_username(
    credentials: HTTPBasicCredentials = Depends(security)
):
    for data in FAKE_USERS_DB:
        correct_username = secrets.compare_digest(
            credentials.username, data['user_id'])
        correct_password = secrets.compare_digest(
            credentials.password, data['password'])

        if (correct_username and correct_password):
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )
