# import os
# import duckdb
# from datetime import datetime
# from .... import secure_filename  # ป้องกันชื่อไฟล์ผิดพลาด
# from ... import Image  # ใช้ Pillow จัดการภาพ

# UPLOAD_FOLDER = "faces"  # โฟลเดอร์เก็บภาพ
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

# def connect_db():
#     return duckdb.connect("face_database.duckdb")


# def create_tables():
#     conn = connect_db()
#     conn.execute('''CREATE TABLE IF NOT EXISTS Users (
#                         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         name TEXT NOT NULL,
#                         email TEXT UNIQUE,
#                         phone TEXT,
#                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
#     conn.execute('''CREATE TABLE IF NOT EXISTS Faces (
#                         face_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER,
#                         image_path TEXT,
#                         FOREIGN KEY(user_id) REFERENCES Users(user_id))''')
    
#     conn.execute('''CREATE TABLE IF NOT EXISTS Devices (
#                         device_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         location TEXT NOT NULL)''')
    
#     conn.execute('''CREATE TABLE IF NOT EXISTS Allow (
#                         allow_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         user_id INTEGER,
#                         device_id INTEGER,
#                         granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                         FOREIGN KEY(user_id) REFERENCES Users(user_id),
#                         FOREIGN KEY(device_id) REFERENCES Devices(device_id))''')
    
    
#     conn.close()


# def save_face_image(user_id, image_file):
#     """ บันทึกรูปภาพใบหน้าลงโฟลเดอร์และเก็บ path ลง DB """
#     filename = f"user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
#     filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    
#     # แปลงและบันทึกภาพเป็น JPEG
#     image = Image.open(image_file)
#     image = image.convert("RGB")  # ป้องกันภาพโปร่งแสง
#     image.save(filepath, "JPEG")
    
#     # บันทึก path ลง DB
#     conn = connect_db()
#     conn.execute("INSERT INTO Faces (user_id, image_path) VALUES (?, ?)", (user_id, filepath))
#     conn.close()
    
#     return filepath


# def add_user(name, email, phone):
#     conn = connect_db()
#     conn.execute("INSERT INTO Users (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
#     conn.close()


# def add_device(location):
#     conn = connect_db()
#     conn.execute("INSERT INTO Devices (location) VALUES (?)", (location,))
#     conn.close()


# def grant_access(user_id, device_id):
#     conn = connect_db()
#     conn.execute("INSERT INTO Allow (user_id, device_id) VALUES (?, ?)", (user_id, device_id))
#     conn.close()


# def log_entry(user_id, device_id, status):
#     conn = connect_db()
#     conn.execute("INSERT INTO Logs (user_id, device_id, status) VALUES (?, ?, ?)", (user_id, device_id, status))
#     conn.close()





# if __name__ == "__main__":
#     create_tables()
#     add_user("John Doe", "john@example.com", "123456789")
#     add_device("Main Entrance")
#     grant_access(1, 1)
#     log_entry(1, 1, "GRANTED")
#     print()
