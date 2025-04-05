import streamlit as st

st.set_page_config(page_title="Facial Database")


pg = st.navigation([
    st.Page("users.py", title="All User"), 
    st.Page("create.py", title="Add User")
])

pg.run()