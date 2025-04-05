# Project-Database-Facial

# 📌 Overview
This project is a face database designed to manage and identify people's faces in K-dai. The system allows administrators to: 

Register users with their information and facial images

Store and manage face images securely

Assign access permissions to specific devices

Retrieve and display user face images through a web interface



## Project Structure

```
.
├── README.md
├── requirements.txt
├── table.sql
├── src
│   ├── app
│   │   ├── __init__.py
│   │   ├── app.py           # Main Streamlit app
│   │   ├── create.py        # Database creation logic
│   │   ├── database         # DB connection or models
│   │   └── users.py         # User logic
│   ├── images               # Face images of students
│   │   ├── aum_face.jpg
│   │   ├── biw_face.jpg
│   │   └── ...              # More student images
│   ├── initial_table.sql    # SQL to initialize DB
│   └── test.py              # Test script
```

---

## Getting Started


### 1. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

Navigate into the `src` directory and run:

```bash
cd src
streamlit run app/app.py
```

---

## Features

- Upload and recognize user faces
- User image and data management
- SQLite integration using `initial_table.sql`
- Images stored in `src/images/`
