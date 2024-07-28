import json
from datetime import datetime, timedelta

USER_DATA_FILE = "USER_DATA.json"


def load_user_data():
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_user_data(user_data):
    with open(USER_DATA_FILE, "w", encoding="utf-8-sig") as f:
        json.dump(user_data, f, default=str)


def get_user_data(user_id):
    user_data = load_user_data()
    return user_data.get(str(user_id), None)


def set_user_data(user_id, full_name):
    user_data = load_user_data()
    user_data[str(user_id)] = {
        "full_name": full_name,
        "last_login": datetime.now().isoformat()
    }
    save_user_data(user_data)


def is_user_logged_in_today(user_id):
    user_data = load_user_data()
    if str(user_id) in user_data:
        last_login = datetime.fromisoformat(user_data[str(user_id)]["last_login"])
        if last_login.date() == datetime.now().date():
            return True
    return False


def clear_user_data(user_id):
    user_data = load_user_data()
    if str(user_id) in user_data:
        del user_data[str(user_id)]
        save_user_data(user_data)
