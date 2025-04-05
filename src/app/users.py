import streamlit as st
from PIL import Image

st.title("Facial Database")

# Define the dialog popup
@st.dialog("User information")
def user_detail(item):
    st.write(f"Name: {item['name']}")
    st.write(f"Phone: {item['phone']}")
    st.write(f"Email: {item['email']}")
    st.write(f"User Type: {item['user_type']}")
    st.write(f"Allow Access room: {item['allowed_room']}")

# Sample students data
students = [
    {
        "id": 1,
        "name": "Alice Smith",
        "phone": "+1234567890",
        "email": "alice.smith@example.com",
        "user_type": "Admin",
        "allowed_room": "Room 101",
        "image_path": "../images/biw_face.jpg"
    },
    {
        "id": 2,
        "name": "Bob Johnson",
        "phone": "+0987654321",
        "email": "bob.johnson@example.com",
        "user_type": "Editor",
        "allowed_room": "Room 102",
        "image_path": "../images/game_face.jpg"
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "phone": "+1122334455",
        "email": "charlie.brown@example.com",
        "user_type": "Viewer",
        "allowed_room": "Room 103",
        "image_path": "../images/pin_face.jpg"
    },
]

st.subheader("Student List")

col_count = 3
row_count = (len(students) // col_count) + (1 if len(students) % col_count != 0 else 0)

for i in range(row_count):
    cols = st.columns(col_count)
    for j in range(col_count):
        index = i * col_count + j
        if index < len(students):
            student = students[index]
            img = Image.open(student["image_path"])

            # Use the column to create an image and a button below it
            with cols[j]:
                st.image(img, caption=student["name"], use_container_width=True)
                if st.button("View Info", key=f"btn-{student['id']}"):
                    user_detail(student)
