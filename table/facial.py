import sqlite3

class DatabaseManager:
    def __init__(self, db_name="table.sql"):
        """Connect to the database and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.enable_foreign_keys()
        self.create_tables()

    def enable_foreign_keys(self):
        """Enable foreign key constraints."""
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def create_tables(self):
        """Create all necessary tables if they don't exist."""
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS Faces (
                face_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS UserType (
                type_id TEXT PRIMARY KEY,
                typename TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Device (
                device_id TEXT PRIMARY KEY,
                location TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Allow (
                allow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                device_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (device_id) REFERENCES Device(device_id) ON DELETE CASCADE
            );
        ''')
        self.conn.commit()


    def add_user(self, name, email, phone):
        """Add a new user."""
        try:
            self.cursor.execute("INSERT INTO Users (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' or phone '{phone}' already exists.")
            return None


    def add_face(self, user_id, image_path):
        """Add face data for a user."""
        self.cursor.execute("INSERT INTO Faces (user_id, image_path) VALUES (?, ?)", (user_id, image_path))
        self.conn.commit()

    def add_user_type(self, type_id, typename):
        """Add a new user type."""
        try:
            self.cursor.execute("INSERT INTO UserType (type_id, typename) VALUES (?, ?)", (type_id, typename))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Type ID '{type_id}' already exists.")


    def add_device(self, device_id, location):
        """Add a new device."""
        try:
            self.cursor.execute("INSERT INTO Device (device_id, location) VALUES (?, ?)", (device_id, location))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Device ID '{device_id}' already exists.")


    def allow_access(self, user_id, device_id):
        """Grant access to a user for a specific device."""
        self.cursor.execute("INSERT INTO Allow (user_id, device_id) VALUES (?, ?)", (user_id, device_id))
        self.conn.commit()


    def get_users(self):
        """Retrieve all users."""
        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()


    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        self.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()


    def get_devices(self):
        """Retrieve all devices."""
        self.cursor.execute("SELECT * FROM Device")
        return self.cursor.fetchall()


    def get_access_list(self):
        """Retrieve all access permissions."""
        self.cursor.execute("SELECT * FROM Allow")
        return self.cursor.fetchall()


    def delete_user(self, user_id):
        """Delete a user and their related data."""
        self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
        self.conn.commit()


    def delete_device(self, device_id):
        """Delete a device and its related access permissions."""
        self.cursor.execute("DELETE FROM Device WHERE device_id = ?", (device_id,))
        self.conn.commit()


    def close(self):
        """Close the database connection."""
        self.conn.close()




if __name__ == "__main__":
    db = DatabaseManager()

    user_id = db.add_user("Indy", "67050534@kmitl.ac.th", "088-555-9999")
    if user_id:
        print(f"User added successfully : ID = {user_id}")

    
    # if user_id:
    #     db.add_face(user_id, "path/to/alice_face.jpg")

   
    # db.add_user_type("student", "Student")
    # db.add_user_type("teaching assistant", "Teaching Assistant")
    # print("User Types:")
    # for user_type in db.cursor.execute("SELECT * FROM UserType").fetchall():
    #     print(user_type)

    
    # db.add_device("device_001", "KDAI")
    # db.add_device("device_002", "Coworking 714")
    # db.add_device("device_003", "Coworking 102")
    # db.add_device("device_004", "Room 108")
    # print("Device List:")
    # for device in db.get_devices():
    #     device_id, location = device
    #     print(f"ID: {device_id} | Location: {location}")

    
    if user_id:
     db.allow_access(user_id, "device_001")
    print(f"Access granted for User ID {user_id} to Device ID 'device_001'")

print("Access List:")
for access in db.get_access_list():
    allow_id, user_id, device_id = access
    print(f"Allow ID: {allow_id} | User ID: {user_id} | Device ID: {device_id}")


# print("User List:")
# for user in db.get_users():
#     user_id, name, email, phone, created_at = user
#     print(f"ID: {user_id} | Name: {name} | Email: {email} | Phone: {phone} | Created At: {created_at}")

    # print("List of equipment : ", db.get_devices())

    # print("Access rights : ", db.get_access_list())

    db.close()