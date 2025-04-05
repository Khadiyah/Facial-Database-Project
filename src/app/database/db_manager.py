import sqlite3

class DatabaseManager:
    def __init__(self, db_name="table.sql"):
        """Connect to the database and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.enable_foreign_keys()
        self.create_tables()

    def enable_foreign_keys(self):
        """Enable Foreign Key constraints."""
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def create_tables(self):
        """Create all necessary tables."""
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                user_type_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_type_id) REFERENCES UserType(type_id) ON DELETE SET NULL
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



    def add_user(self, name, email, phone, user_type_id=None):
        """Add a new user."""
        try:
            self.cursor.execute("INSERT INTO Users (name, email, phone, user_type_id) VALUES (?, ?, ?, ?)", 
                                (name, email, phone, user_type_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' or Phone '{phone}' already exists.")
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
        """Grant access to a device for a user."""
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


    def delete_user_by_id(self, user_id):
        """Delete a user and all related data (Faces, Allow)."""
        self.cursor.execute("DELETE FROM Faces WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM Allow WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
        self.conn.commit()
        print(f"User ID {user_id} and all related data have been deleted.")


    def delete_device(self, device_id):
        """Delete a device and its related access permissions."""
        self.cursor.execute("DELETE FROM Device WHERE device_id = ?", (device_id,))
        self.conn.commit()


    def reset_database(self):
        """Delete all data in the database and reset auto-increment values."""
        self.cursor.execute("DELETE FROM Faces")
        self.cursor.execute("DELETE FROM Allow")
        self.cursor.execute("DELETE FROM Users")
        self.cursor.execute("DELETE FROM UserType")
        self.cursor.execute("DELETE FROM Device")
        self.cursor.execute("DELETE FROM sqlite_sequence")  # Reset auto-increment
        self.conn.commit()
        print("Database has been reset.")


    # --- Aggregation Function ---
    def count_faces(self):
        """Count the number of face records."""
        self.cursor.execute("SELECT COUNT(*) FROM Faces")
        return self.cursor.fetchone()[0]


    # --- Queries using JOIN ---
    def get_users_with_faces(self):
        """Get users along with their face data."""
        self.cursor.execute('''
            SELECT Users.user_id, Users.name, Faces.image_path
            FROM Users
            JOIN Faces ON Users.user_id = Faces.user_id
        ''')
        return self.cursor.fetchall()


    def get_users_accessing_devices(self):
        """Get users and the devices they have access to."""
        self.cursor.execute('''
            SELECT Users.name, Device.device_id, Device.location
            FROM Users
            JOIN Allow ON Users.user_id = Allow.user_id
            JOIN Device ON Allow.device_id = Device.device_id
        ''')
        return self.cursor.fetchall()


    def get_users_with_type(self):
        """Get users with their assigned type."""
        self.cursor.execute('''
            SELECT Users.name, UserType.typename
            FROM Users
            LEFT JOIN UserType ON Users.user_type_id = UserType.type_id
        ''')
        return self.cursor.fetchall()


     # --- Window Function ---
    def get_ranked_devices(self):
        """Rank devices based on location using ROW_NUMBER()."""
        self.cursor.execute('''
            SELECT device_id, location,
            ROW_NUMBER() OVER (ORDER BY location) AS rank
            FROM Device
        ''')
        return self.cursor.fetchall()


    def __del__(self):
        """Close the database connection automatically."""
        self.conn.close()



# if __name__ == "__main__":
    # db = DatabaseManager()

    #Add a user
    # user_id = db.add_user("Dr.Big", "akadej.ud@kmitl.ac.th", "061-890-1234", "type_05")
    # if user_id:
    #     print(f"User added successfully: ID = {user_id}")
    #     db.add_face(user_id, "src/images/dr.big_face.jpg")
    #     db.allow_access(user_id, "device_001")
    #     db.allow_access(user_id, "device_002")
    #     db.allow_access(user_id, "device_003")
    #     db.allow_access(user_id, "device_004")


    # #Add user types
    # db.add_user_type("type_01", "Student")
    # db.add_user_type("type_02", "Teaching Assistant")
    # db.add_user_type("type_03", "Teacher")
    # db.add_user_type("type_04", "Secretary")
    # db.add_user_type("type_05", "Boss")
    # print("User Types:")
    # for type_id, typename in db.cursor.execute("SELECT * FROM UserType").fetchall():
    #     print(f"Type ID: {type_id} | Type Name: {typename}")



    # #Add devices
    # db.add_device("device_001", "KDAI")
    # db.add_device("device_002", "Coworking 714")
    # db.add_device("device_003", "Coworking 102")
    # db.add_device("device_004", "Room 108")
    # print("Device List:")
    # for device in db.get_devices():
    #     device_id, location = device
    #     print(f"ID: {device_id} | Location: {location}")



    # #Get Access List
    # print("Access List:")
    # for allow_id, user_id, device_id in db.get_access_list():
    #     print(f"Allow ID: {allow_id} | User ID: {user_id} | Device ID: {device_id}")



    # #Get Users
    # print("User List:")
    # for user in db.get_users():
        # user_id, name, email, phone, user_type_id, created_at = user
        # print(f"ID: {user_id} | Name: {name} | Email: {email} | Phone: {phone} | Type: {user_type_id} | Created: {created_at}")



    # #Get User By ID
    # print("User Info:")
    # user = db.get_user_by_id(1)  
    # if user:
    #     user_id, name, email, phone, user_type_id, created_at = user
    #     print(f"ID: {user_id} | Name: {name} | Email: {email} | Phone: {phone} | Type: {user_type_id} | Created: {created_at}")
    # else:
    #     print("User not found.")



    # #Delete User By ID (?)
    # db.delete_user_by_id()
    # print(db.get_users())



    # #Deleted Device
    # print("Deleted Device:")
    # device_id = "device_000"  # example device_id
    # db.delete_device(device_id)
    # print(f"Device ID: {device_id} has been removed.")



    # #Reset Database
    # db.reset_database()



    # #Display data
    # print("Total Faces:")
    # total_faces = db.count_faces()
    # print(f"Total: {total_faces}")

    # print("Users with Faces:")
    # for user_id, name, image_path in db.get_users_with_faces():
    #     print(f"User ID: {user_id} | Name: {name} | Image Path: {image_path}")

    # print("Users Accessing Devices:")
    # for name, device_id, location in db.get_users_accessing_devices():
    #     print(f"User: {name} | Device ID: {device_id} | Location: {location}")

    # print("Users with Type:")
    # for name, typename in db.get_users_with_type():
    #  print(f"User: {name} | Type: {typename}")

    # print("Ranked Devices:")
    # for device_id, location, rank in db.get_ranked_devices():
    #     print(f"Rank: {rank} | Device ID: {device_id} | Location: {location}")

    

    # print("Users after deletion:", db.get_users())
    # print("Faces after deletion:", db.cursor.execute("SELECT * FROM Faces").fetchall())
    # print("Allow after deletion:", db.cursor.execute("SELECT * FROM Allow").fetchall())

    # db.cursor.execute("DELETE FROM Faces")
    # db.cursor.execute("DELETE FROM Allow")
    # db.cursor.execute("DELETE FROM Users")
    # db.cursor.execute("DELETE FROM sqlite_sequence WHERE name='Users'")
    # db.conn.commit()
    # print("All users and related data have been deleted.")
    

    
    # print("Users Table:")
    # for user in db.cursor.execute("SELECT * FROM Users").fetchall():
    #     user_id, name, email, phone, user_type_id, created_at = user
    #     print(f"ID: {user_id} | Name: {name} | Email: {email} | Phone: {phone} | Type: {user_type_id} | Created: {created_at}")

    # print("Faces Table:")
    # for face_id, user_id, image_path in db.cursor.execute("SELECT * FROM Faces").fetchall():
    #     print(f"Face ID: {face_id} | User ID: {user_id} | Image Path: {image_path}")

    # print("Allow Table:")
    # for allow_id, user_id, device_id in db.cursor.execute("SELECT * FROM Allow").fetchall():
    #     print(f"Allow ID: {allow_id} | User ID: {user_id} | Device ID: {device_id}")

    # print("UserType Table:")
    # for type_id, typename in db.cursor.execute("SELECT * FROM UserType").fetchall():
    #     print(f"Type ID: {type_id} | Type Name: {typename}")

    # print("Device Table:")
    # for device_id, location in db.cursor.execute("SELECT * FROM Device").fetchall():
    #     print(f"Device ID: {device_id} | Location: {location}")


    # db.__del__() 