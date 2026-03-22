from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Функция, которая запрашивает авторизацию с помощью BasicAuth, и сравнивает креды для входа.
def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "test"

    is_correct_username = secrets.compare_digest(
        credentials.username, correct_username
    )
    is_correct_password = secrets.compare_digest(
        credentials.password, correct_password
    )
    # Если логин и пароль не соответствуют введенным данным, возвращается ошибка
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username



