import hashlib
import os
import sqlite3


class AuthManager:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        email: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

        self.salt: bytes = os.urandom(16)
        self.hashed_password: str = self.hash_password()

        self.conn = sqlite3.connect("popcorn.db")
        self.cursor = self.conn.cursor()

    def hash_password(self) -> str:
        hashed = hashlib.pbkdf2_hmac(
            "sha256", self.password.encode(), self.salt, 100_000
        )
        return self.salt.hex() + ":" + hashed.hex()

    def insert_user_table(self):
        self.cursor.execute(
            """
            INSERT INTO Users(first_name, last_name, username, hashed_password, email)
            VALUES (?, ? , ?, ?, ?)
        """,
            (
                self.first_name,
                self.last_name,
                self.username,
                self.hashed_password,
                self.email,
            ),
        )
