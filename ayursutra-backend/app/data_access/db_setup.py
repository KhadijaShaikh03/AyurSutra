import sqlite3
import os

# ------------------------------
# Step 0: Database Path Setup
# ------------------------------
# Get path two levels up (from data_access folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database folder
DB_FOLDER = os.path.join(BASE_DIR, "..", "database")
os.makedirs(DB_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# Full path to database file
DB_PATH = os.path.join(DB_FOLDER, "ayursutra.db")
print(f"Database path: {DB_PATH}")  # Confirmation

# ------------------------------
# Step 1: Create Tables
# ------------------------------
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact TEXT
        )
    """)

    # Therapies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS therapies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            therapy_name TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    """)

    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            appointment_date TEXT,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")  # Confirmation

# ------------------------------
# Step 2: Run Script
# ------------------------------
if __name__ == "__main__":
    create_tables()
