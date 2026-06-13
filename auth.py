import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

USERS = {
    "admin@hrapp.com": {
        "password"  : hash_password("Admin@123"),
        "role"      : "Admin",
        "dept"      : "All",
        "name"      : "Admin User"
    },
    "manager@hrapp.com": {
        "password"  : hash_password("Manager@123"),
        "role"      : "Manager",
        "dept"      : "Sales",
        "name"      : "Sales Manager"
    },
    "analyst@hrapp.com": {
        "password"  : hash_password("Analyst@123"),
        "role"      : "Analyst",
        "dept"      : "All",
        "name"      : "HR Analyst"
    },
}

def login(email: str, password: str):
    user = USERS.get(email)
    if user and verify_password(password, user["password"]):
        return user
    return None
