import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

USERS = {
    "admin@hrapp.com": {
        "password"   : hash_password("Admin@123"),
        "role"       : "HR Admin",
        "department" : "All",
        "name"       : "HR Admin"
    },
    "hr@hrapp.com": {
        "password"   : hash_password("HR@123"),
        "role"       : "HR Manager",
        "department" : "Human Resources",
        "name"       : "HR Manager"
    },
    "sales@hrapp.com": {
        "password"   : hash_password("Sales@123"),
        "role"       : "Sales Manager",
        "department" : "Sales",
        "name"       : "Sales Manager"
    },
    "rd@hrapp.com": {
        "password"   : hash_password("RnD@123"),
        "role"       : "R&D Manager",
        "department" : "Research & Development",
        "name"       : "R&D Manager"
    },
}

def login(email: str, password: str):
    user = USERS.get(email.strip().lower())
    if user and verify_password(password, user["password"]):
        return user
    return None
