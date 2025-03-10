CREATE TABLE Users (
    user_id INT PRIMARY KEY ,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Faces (
    face_id INT PRIMARY KEY ,
    user_id INT,
    image_path VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE UserType (
    type_id VARCHAR(50) PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL
);

CREATE TABLE Device (
    device_id VARCHAR(50) PRIMARY KEY,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE Allow (
    allow_id INT PRIMARY KEY , 
    user_id INT, 
    device_id INT, 
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (device_id) REFERENCES Device(device_id) ON DELETE CASCADE
);


INSERT INTO Users (name, email) VALUES ('Ning', '67051281@kmitl.ac.th');

INSERT INTO Faces (user_id, image_path) 
VALUES (67051281, 'https://drive.google.com/file/d/1MDBFkJeXKZTHT9FeSrHhTvW1FUHwMHsl/view?usp=drive_link'); 
