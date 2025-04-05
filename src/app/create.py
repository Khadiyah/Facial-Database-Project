import streamlit as st
import uuid
import os


from database.db_manager import DatabaseManager

db = DatabaseManager("/Users/thohirahhusaini/Downloads/Project-Database-/table.sql")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'faces')
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Add student")

with st.form(key='user_form'):
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    user_type = st.selectbox("User Type", ["Student", "Teacher", "TA", "Secretary", "Boss"])
    options = st.multiselect(
        "Allow to access room",
        ["KDAI", "Coworking 714", "Coworking 102", "Room 108"],
    )
    uploaded_image = st.file_uploader("Upload Face Image", type=["jpg", "jpeg"])
    submit_button = st.form_submit_button("Submit")

if submit_button:
    # Map user_type to ID (example mapping — match your DB entries!)
    user_type_map = {
        "Student": "type_01",
        "TA": "type_02",
        "Teacher": "type_03",
        "Secretary": "type_04",
        "Boss": "type_05",
    }
    user_type_id = user_type_map.get(user_type)

    # Add user
    user_id = db.add_user(name, email, phone, user_type_id)

    if user_id:
        # Add default face path (if needed)
        from os.path import abspath, join, dirname
        BASE_DIR = abspath(join(dirname(__file__), '..'))
        image_path = join(BASE_DIR, "images", "default_face.jpg")

        db.add_face(user_id, image_path)

        # Map room to device_id (you can customize this mapping!)
        room_map = {
            "KDAI": "device_001",
            "Coworking 714": "device_002",
            "Coworking 102": "device_003",
            "Room 108": "device_004",
        }

        for room in options:
            device_id = room_map.get(room)
            if device_id:
                db.allow_access(user_id, device_id)

        st.success(f"✅ Added user: {name}")
    else:
        st.error("❌ User already exists (duplicate email or phone)")

