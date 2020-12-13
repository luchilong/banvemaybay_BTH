from flask_login import UserMixin
from enum import Enum as UserEnum
from mainmb import mainmb
import json
import hashlib, os


def add_user(name, email, username, password):
    users = read_user()
    user = {
        "id": len(users) + 1,
        "name": name.strip(),
        "email": email.strip(),
        "username": username.strip(),
        "password": str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    }
    users.append(user)

    with open(os.path.join(mainmb.root_path, "data/user.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return user


def read_user():
    with open(os.path.join(mainmb.root_path, "data/user.json"), encoding="utf-8") as f:
        return json.load(f)


def validate_user(username, password):
    users = read_user()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    for user in users:
        if user["username"].strip() == username.strip() and user["password"] == password:
            return user

    return None


# if __name__ == "__main__":
#     print()