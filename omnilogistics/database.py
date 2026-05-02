import sqlite3

def get_db_connection():
    conn = sqlite3.connect('logistics.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = sqlite3.connect('logistics.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trucks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT UNIQUE NOT NULL,
            model_name TEXT NOT NULL,
            max_load_capacity REAL NOT NULL,
            current_mileage REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Healthy'
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            license_category TEXT NOT NULL,
            contact_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            role TEXT DEFAULT 'Driver'
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT DEFAULT 'Prishtina',
            destination TEXT NOT NULL,
            cargo_weight REAL NOT NULL,
            truck_id INTEGER,
            driver_id INTEGER,
            status TEXT DEFAULT 'Scheduled',
            FOREIGN KEY (truck_id) REFERENCES trucks(id),
            FOREIGN KEY (driver_id) REFERENCES drivers(id)
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            actor_id INTEGER,
            action_type TEXT NOT NULL,
            affected_entity TEXT NOT NULL,
            before_value TEXT,
            after_value TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def init_db():
    conn, cursor = create_database()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("OmniLogistics Database Initialized.")