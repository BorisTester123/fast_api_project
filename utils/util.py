import bcrypt

# создаем функцию для хэширования пароля
def hash_password(password: str) -> str:
    # Автоматически обрезаем до 72 байт (bcrypt теперь требует этого явно)
    safe_password = password[:72].encode("utf-8")
    hashed = bcrypt.hashpw(safe_password, bcrypt.gensalt())
    return hashed.decode("utf-8")

# верифицируем хэшированный пароль
def verify_password(plain_password: str, password_hash: str) -> bool:
    safe_password = plain_password[:72].encode("utf-8")
    return bcrypt.checkpw(safe_password, password_hash.encode("utf-8"))