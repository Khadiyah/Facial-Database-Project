import streamlit as st
from PIL import Image

import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
from database.db_manager import DatabaseManager

st.title("Facial Database")

@st.dialog("User information")
def user_detail(item):
    st.write(f"Name: {item['name']}")
    st.write(f"Phone: {item['phone']}")
    st.write(f"Email: {item['email']}")
    st.write(f"User Type: {item['user_type']}")
    st.write(f"Allow Access room: {item['allowed_room']}")

DB_PATH = BASE_DIR + "/table.sql"
db = DatabaseManager(DB_PATH)
users = db.get_users()
students = []
for user in users:
    user_id, name, email, phone, user_type_id, created_at = user

    db.cursor.execute("SELECT typename FROM UserType WHERE type_id = ?", (user_type_id,))
    result = db.cursor.fetchone()
    user_type = result[0] if result else "Unknown"

    db.cursor.execute('''
        SELECT Device.location
        FROM Allow
        JOIN Device ON Allow.device_id = Device.device_id
        WHERE Allow.user_id = ?
    ''', (user_id,))
    allowed_rooms = [row[0] for row in db.cursor.fetchall()]
    allowed_room = ", ".join(allowed_rooms)

    # Get image path (just the first face image for display)
    db.cursor.execute("SELECT image_path FROM Faces WHERE user_id = ?", (user_id,))
    result = db.cursor.fetchone()
    image_path = BASE_DIR + "/" + result[0]

    # Append to student list
    students.append({
        "id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "user_type": user_type,
        "allowed_room": allowed_room,
        "image_path": image_path
    })

col_count = 3
row_count = (len(students) // col_count) + (1 if len(students) % col_count != 0 else 0)

for i in range(row_count):
    cols = st.columns(col_count)
    for j in range(col_count):
        index = i * col_count + j
        if index < len(students):
            student = students[index]
            img = Image.open(student["image_path"])

            with cols[j]:
                st.image(img, use_container_width=True)
                if st.button("View user information", key=f"btn-{student['id']}", use_container_width=True):
                    user_detail(student)
