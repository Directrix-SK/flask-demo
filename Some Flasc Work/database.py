import uuid
import os
import sqlite3

# Dynamically gets the exact directory path where database.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            amount TEXT NOT NULL,
            status TEXT NOT NULL,
            certificate_signature TEXT
        )
    """)
    
    # Schema migration safeguard for existing databases
    try:
        conn.execute("ALTER TABLE milestones ADD COLUMN certificate_signature TEXT;")
        print("[DB Migration] Added missing certificate_signature column!")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def register_user(username, password_hash, role):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username):
    conn = get_db_connection()
    user = conn.execute(
        """
        SELECT password_hash
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()
    conn.close()
    
    if user:
        return user["password_hash"]
    return None


def get_user_profile(username):
    conn = get_db_connection()
    user = conn.execute(
        """
        SELECT username, role
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()
    conn.close()
    
    if user:
        return {
            "username": user["username"],
            "role": user["role"]
        }
    return None


def get_all_users():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, username, password_hash, role FROM users"
    ).fetchall()
    conn.close()
    
    return [
        {
            "id": u["id"],
            "username": u["username"],
            "password": u["password_hash"],
            "role": u["role"]
        }
        for u in users
    ]


def get_user_milestones(username):
    conn = get_db_connection()
    milestones = conn.execute(
        "SELECT id, username, title, amount, status, certificate_signature FROM milestones WHERE username = ?",
        (username,)
    ).fetchall()
    conn.close()
    return milestones


def get_milestone_by_id(milestone_id):
    conn = get_db_connection()
    milestone = conn.execute(
        "SELECT id, username, title, amount, status, certificate_signature FROM milestones WHERE id = ?",
        (milestone_id,)
    ).fetchone()
    conn.close()
    return milestone


def set_certificate_verified(milestone_id):
    conn = get_db_connection()
    unique_cert_sig = f"GOVT-VERIFIED-{str(uuid.uuid4())[:8].upper()}"
    
    conn.execute("""
        UPDATE milestones 
        SET status = 'Approved', certificate_signature = ? 
        WHERE id = ?
    """, (unique_cert_sig, milestone_id))
    
    conn.commit()
    conn.close()


def seed_test_milestones_for_user(username):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM milestones WHERE username = ?", 
        (username,)
    ).fetchall()
    
    if not existing:
        initial_sig = f"GOVT-VERIFIED-{str(uuid.uuid4())[:8].upper()}"
        
        conn.execute("""
            INSERT INTO milestones (username, title, amount, status, certificate_signature)
            VALUES (?, ?, ?, ?, ?)
        """, (username, "Milestone 1: Prototype Field Test", "₹1,50,000", "Approved", initial_sig))
        
        conn.execute("""
            INSERT INTO milestones (username, title, amount, status, certificate_signature)
            VALUES (?, ?, ?, ?, ?)
        """, (username, "Milestone 2: District Pilot Deployment", "₹3,00,000", "Pending Review", None))
        
        conn.commit()
    conn.close()


def seed_default_accounts():
    conn = get_db_connection()
    
    demo_users = [
        ("startup_alpha", "1234", "Startup"),
        ("startup_test", "1234", "Startup"),
        ("evaluator_dept", "1234", "Expert Evaluator"),
        ("gov_officer_demo", "1234", "Gov Officer")  # Ready for login
    ]
    
    for username, password, role in demo_users:
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    conn.close()
    
    # Pre-populate sample milestones
    seed_test_milestones_for_user("startup_alpha")
    seed_test_milestones_for_user("startup_test")