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
│   ├── images               # Face images of user
│   │   ├── aum_face.jpg
│   │   ├── biw_face.jpg
│   │   └── ...              # More student images
│   └── initial_table.sql    # SQL to initialize DB
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

--

## All logic in `DatabaseManager`
### Set Up the Database

To set up the database, you can initialize it using the `DatabaseManager` class:

```python
db = DatabaseManager("your_database_name.sql")
```

This will automatically create the required tables if they don't already exist.

### Example Usage

- **Add a user**:

```python
user_id = db.add_user("Dr.Big", "akadej.ud@kmitl.ac.th", "061-890-1234", "type_05")
```

- **Add a face for the user**:

```python
db.add_face(user_id, "src/images/dr.big_face.jpg")
```

- **Add devices**:

```python
db.add_device("device_001", "KDAI")
db.add_device("device_002", "Coworking 714")
```

- **Allow user access to devices**:

```python
db.allow_access(user_id, "device_001")
```

### Database Management Functions

The `DatabaseManager` class provides various methods for interacting with the database:

- **Add a new user**: `add_user(name, email, phone, user_type_id)`
- **Add a face for a user**: `add_face(user_id, image_path)`
- **Add a new user type**: `add_user_type(type_id, typename)`
- **Add a new device**: `add_device(device_id, location)`
- **Grant access to a device**: `allow_access(user_id, device_id)`
- **Get all users**: `get_users()`
- **Get all devices**: `get_devices()`
- **Get all access permissions**: `get_access_list()`
- **Delete a user**: `delete_user_by_id(user_id)`
- **Delete a device**: `delete_device(device_id)`
- **Reset the database**: `reset_database()`
- **Count the number of faces**: `count_faces()`

### Queries and Aggregation

- **Get users along with their face data**:

```python
users_with_faces = db.get_users_with_faces()
```

- **Get users accessing devices**:

```python
users_accessing_devices = db.get_users_accessing_devices()
```

- **Get users with their user type**:

```python
users_with_type = db.get_users_with_type()
```

- **Rank devices based on location**:

```python
ranked_devices = db.get_ranked_devices()
```

---

## Features

- Upload and recognize user faces
- User image and data management
- SQLite integration using `initial_table.sql`
- Images stored in `src/images/`
