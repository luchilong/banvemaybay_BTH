from flask_login import UserMixin
from enum import Enum as UserEnum
from mainmb import app
import json
import hashlib, os

def read_user():
    with open(os.path.join(app.root_path, "data/user.json"), encoding="utf-8") as f:
        return json.load(f)

def validate_user(username, password):
    users = read_user()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    for user in users:
        if user["username"].strip() == username.strip() and user["password"] == password:
            return user

    return None


if __name__ == "__main__":
    print()