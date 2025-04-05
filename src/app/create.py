import streamlit as st

st.title("Add student")

with st.form(key='user_form'):
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    user_type = st.selectbox("User Type", ["Student", "Teacher", "TA"])
    options = st.multiselect(
        "Allow to access room",
        ["Room 1", "Room 2", "Room 3", "Room 4"],
    )



    submit_button = st.form_submit_button("Submit")

if submit_button:
    st.write(f"Name: {name}")
    st.write(f"Phone: {phone}")
    st.write(f"Email: {email}")
    st.write(f"User Type: {user_type}")
    st.write(f"Allow Access room: {options}")
    
