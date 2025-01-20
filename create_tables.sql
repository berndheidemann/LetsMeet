-- Tabla: Anmeldedaten
CREATE TABLE Anmeldedaten (
    User_ID INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    timestamp_last_login TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

-- Tabla: User
CREATE TABLE User (
    User_ID SERIAL PRIMARY KEY,
    Vorname VARCHAR(50),
    Nachname VARCHAR(50),
    Phone VARCHAR(20),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Address VARCHAR(255),
    Gender VARCHAR(20),
    Birthday DATE
);

-- Tabla: User_Bilder
CREATE TABLE User_Bilder (
    Bild_ID SERIAL PRIMARY KEY,
    User_ID INT NOT NULL,
    Image BYTEA, -- Para guardar imágenes en formato binario (BLOB)
    is_profilepicture BOOLEAN DEFAULT FALSE,
    timestamp_upload TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

-- Tabla: User_Hobbys
CREATE TABLE User_Hobbys (
    User_ID INT NOT NULL,
    Hobby_ID INT NOT NULL,
    Prio INT, -- Prioridad del hobby (puede ser negativa, de -100 a 100)
    PRIMARY KEY (User_ID, Hobby_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Hobby_ID) REFERENCES Hobbys(Hobby_ID)
);

-- Tabla: Hobbys
CREATE TABLE Hobbys (
    Hobby_ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- Tabla: Likes
CREATE TABLE Likes (
    liker_User_ID INT NOT NULL,
    liked_User_ID INT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    PRIMARY KEY (liker_User_ID, liked_User_ID),
    FOREIGN KEY (liker_User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (liked_User_ID) REFERENCES User(User_ID)
);

-- Tabla: Nachrichten
CREATE TABLE Nachrichten (
    Message_ID SERIAL PRIMARY KEY,
    Sender_User_ID INT NOT NULL,
    Receiver_User_ID INT NOT NULL,
    Message_Content TEXT NOT NULL,
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50),
    FOREIGN KEY (Sender_User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (Receiver_User_ID) REFERENCES User(User_ID)
);

-- Tabla: Freunde
CREATE TABLE Freunde (
    Friendship_ID SERIAL PRIMARY KEY,
    User_ID1 INT NOT NULL,
    User_ID2 INT NOT NULL,
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID1) REFERENCES User(User_ID),
    FOREIGN KEY (User_ID2) REFERENCES User(User_ID)
);
