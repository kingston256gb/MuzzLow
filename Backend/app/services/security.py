import bcrypt

SECRET_KEY = None
ALGORITHM = 'HS256'

class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(entered_password: str, db_password: str) -> bool:
        return bcrypt.checkpw(entered_password.encode(), db_password.encode())