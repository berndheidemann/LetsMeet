import psycopg2
import pymongo
from datetime import datetime

# Verbindung zur MongoDB herstellen
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["letsmeet"]  # Name der MongoDB-Datenbank
mongo_collection = mongo_db["users"]  # Name der Collection

# Verbindung zur PostgreSQL-Datenbank herstellen
pg_conn = psycopg2.connect(
    host="localhost",
    database="lf8_lets_meet_db",
    user="user",
    password="secret"
)
pg_cursor = pg_conn.cursor()

# Funktion zum Einfügen von Benutzerdaten in PostgreSQL
def insert_user_data(user):
    try:
        # Benutzer einfügen
        pg_cursor.execute(
            """
            INSERT INTO User (Vorname, Nachname, Phone, CreatedAt, UpdatedAt)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING User_ID;
            """,
            (
                user["name"].split(", ")[1],  # Vorname
                user["name"].split(", ")[0],  # Nachname
                None,  # Telefonnummer entfernt
                datetime.strptime(user["createdAt"], "%Y-%m-%dT%H:%M:%S"),
                datetime.strptime(user["updatedAt"], "%Y-%m-%dT%H:%M:%S"),
            )
        )
        user_id = pg_cursor.fetchone()[0]

        # Anmeldedaten einfügen (E-Mail wird hier als ID verwendet)
        pg_cursor.execute(
            """
            INSERT INTO Anmeldedaten (User_ID, email, password_hash, status)
            VALUES (%s, %s, %s, %s);
            """,
            (
                user_id,  # Pseudonyme User_ID
                user["_id"],  # E-Mail als ID in MongoDB
                "<hashed_password>",  # Platzhalter für Passwort-Hash
                "active"  # Beispielstatus
            )
        )

        # Likes einfügen und gleichzeitig Freundschaften bei "Match" anlegen
        for like in user.get("likes", []):
            liker_user_id = user_id
            liked_user_id = pg_cursor.execute(
                """
                SELECT User_ID FROM Anmeldedaten WHERE email = %s;
                """,
                (like["liked_email"],)
            ).fetchone()[0]

            # Eintrag in die Likes-Tabelle (Nur User_IDs, kein liked_email mehr)
            pg_cursor.execute(
                """
                INSERT INTO Likes (liker_User_ID, liked_User_ID, timestamp, status)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    liker_user_id,
                    liked_user_id,
                    datetime.strptime(like["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    like["status"]
                )
            )

            # Wenn der Status "Match" ist, Freundschaft hinzufügen
            if like["status"] == "Match":
                pg_cursor.execute(
                    """
                    INSERT INTO Freunde (User_ID1, User_ID2, Timestamp)
                    VALUES (%s, %s, %s);
                    """,
                    (
                        liker_user_id,
                        liked_user_id,
                        datetime.strptime(like["timestamp"], "%Y-%m-%d %H:%M:%S")
                    )
                )

        # Nachrichten einfügen (keine Umkehrung der IDs mehr)
        for message in user.get("messages", []):
            sender_id = user_id
            receiver_id = pg_cursor.execute(
                """
                SELECT User_ID FROM Anmeldedaten WHERE email = %s;
                """,
                (message["receiver_email"],)
            ).fetchone()[0]

            pg_cursor.execute(
                """
                INSERT INTO Nachrichten (Sender_User_ID, Receiver_User_ID, Message_Content, Timestamp)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    sender_id,
                    receiver_id,
                    message["message"],
                    datetime.strptime(message["timestamp"], "%Y-%m-%d %H:%M:%S"),
                )
            )

        # Änderungen speichern
        pg_conn.commit()

    except Exception as e:
        pg_conn.rollback()
        print(f"Fehler beim Einfügen von Daten für Benutzer {user['_id']}: {e}")

# Alle Benutzer aus der MongoDB lesen und in PostgreSQL einfügen
for mongo_user in mongo_collection.find():
    insert_user_data(mongo_user)

# Verbindungen schließen
pg_cursor.close()
pg_conn.close()
mongo_client.close()