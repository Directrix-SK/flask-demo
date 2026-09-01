# db.py - HAND THIS TO ME pls

def init_db():
    # code here to create tables if they don't exist.
    pass

def register_user(username, password_hash):
    
    # Input: string username, string password
    # Output: Return True if inserted successfully, False if username exists.
    # Can Write SQL HERE
    return True

def verify_user(username):
    
    # Input: string username
    # Output: Return password string if user exists, or None if user not found.
    # Can Write SQL HERE
    return "hashed_password_from_sql"

def get_user_profile(username):

    # Input: string username
    # Output: Return a dictionary with user details (e.g., {'name': 'Shaurya', 'role': 'Admin'})
    # Can Write SQL HERE
    return {"username": username, "role": "Student"}