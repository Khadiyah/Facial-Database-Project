import streamlit as st
from database.db_manager import DatabaseManager
import os
import uuid
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = BASE_DIR + "/table.sql"
db = DatabaseManager(DB_PATH)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("Add student")

with st.form(key='user_form'):
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    user_type = st.selectbox("User Type", ["Student", "Teacher", "Teaching Assistant", "Secretary", "Boss"])
    options = st.multiselect(
        "Allow to access room",
        ["KDAI", "Coworking 714", "Coworking 102", "Room 108"],
    )
    uploaded_image = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button("Submit")

if submit_button:
    user_type_map = {
        "Student": "type_01",
        "Teaching Assistant": "type_02",
        "Teacher": "type_03",
        "Secretary": "type_04",
        "Boss": "type_05",
    }
    user_type_id = user_type_map.get(user_type)

    user_id = db.add_user(name, email, phone, user_type_id)

    if user_id:
        if uploaded_image is not None:
            ext = uploaded_image.name.split('.')[-1]
            filename = f"user_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
            image_path = os.path.join(UPLOAD_DIR, filename)

            with open(image_path, "wb") as f:
                f.write(uploaded_image.read())

            image_path_db = "src/images/" + filename 
        else:
            st.error("Image is required!")

        db.add_face(user_id, image_path_db)

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

        st.success(f"Added user: {name}")
    else:
        st.error("User already exists (duplicate email or phone)")
