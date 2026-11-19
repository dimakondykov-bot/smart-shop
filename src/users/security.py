import bcrypt


# Превращаем обычный пароль в зашифрованный
def hash_password(password: str) -> str:

    # Переводим строку пароля в байты (bcrypt работает только с байтами)
    pwd_bytes = password.encode("utf-8")

    # Генерирует случайную "соль" уникальную добавку для защиты от взлома
    salt = bcrypt.gensalt()

    # Смешиваем пароль с солью, шифруем и переводим обратно в обычную строку для записи в БД
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

# Функция проверяет, подходит ли введённый пароль к тому хэшу, что лежит в базе
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )