DROP TABLE IF EXISTS freunde CASCADE;
DROP TABLE IF EXISTS likes CASCADE;
DROP TABLE IF EXISTS nachrichten CASCADE;
DROP TABLE IF EXISTS user_bilder CASCADE;
DROP TABLE IF EXISTS user_hobbys CASCADE;
DROP TABLE IF EXISTS hobbys CASCADE;
DROP TABLE IF EXISTS anmeldedaten CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Tabla principal de usuarios
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    vorname VARCHAR(50),
    nachname VARCHAR(50),
    gender VARCHAR(20),
    interessiert_an VARCHAR(50),  
    birthday DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de datos de autenticación
CREATE TABLE anmeldedaten (
    user_id INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    timestamp_last_login TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabla de hobbys
CREATE TABLE hobbys (
    hobby_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Tabla intermedia para la relación user-hobby con prioridad
CREATE TABLE user_hobbys (
    user_id INT NOT NULL,
    hobby_id INT NOT NULL,
    prio INT,
    PRIMARY KEY (user_id, hobby_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (hobby_id) REFERENCES hobbys(hobby_id)
);

-- Tabla para las imágenes de usuario (perfil y fotos adicionales)
CREATE TABLE user_bilder (
    bild_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    image BYTEA,
    is_profilepicture BOOLEAN DEFAULT FALSE,
    timestamp_upload TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabla para "likes"
CREATE TABLE likes (
    liker_user_id INT NOT NULL,
    liked_user_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    PRIMARY KEY (liker_user_id, liked_user_id),
    FOREIGN KEY (liker_user_id) REFERENCES users(user_id),
    FOREIGN KEY (liked_user_id) REFERENCES users(user_id)
);

-- Tabla para "mensajes" (chat) entre usuarios
CREATE TABLE nachrichten (
    message_id SERIAL PRIMARY KEY,
    sender_user_id INT NOT NULL,
    receiver_user_id INT NOT NULL,
    message_content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (sender_user_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_user_id) REFERENCES users(user_id)
);

-- Tabla para "amigos"
CREATE TABLE freunde (
    friendship_id SERIAL PRIMARY KEY,
    user_id1 INT NOT NULL,
    user_id2 INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id1) REFERENCES users(user_id),
    FOREIGN KEY (user_id2) REFERENCES users(user_id)
);

