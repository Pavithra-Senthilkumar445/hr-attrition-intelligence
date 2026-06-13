users = {
    "admin": {"password": "admin123", "role": "admin"},
    "manager": {"password": "manager123", "role": "manager"},
    "employee": {"password": "emp123", "role": "employee"}
}

def authenticate_user(username, password):
    if username in users and users[username]["password"] == password:
        return {"role": users[username]["role"]}
    return None
