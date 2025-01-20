import psycopg2
import xml.etree.ElementTree as ET

# Verbindung zur PostgreSQL-Datenbank herstellen
pg_conn = psycopg2.connect(
    host="localhost",
    database="lf8_lets_meet_db",
    user="user",
    password="secret"
)
pg_cursor = pg_conn.cursor()

# Funktion, um Hobby in die Hobbys-Tabelle einzufügen
def insert_hobby(hobby_name):
    # Überprüfen, ob das Hobby bereits existiert
    pg_cursor.execute(
        """
        SELECT Hobby_ID FROM Hobbys WHERE Name = %s;
        """,
        (hobby_name,)
    )
    hobby_id = pg_cursor.fetchone()

    if hobby_id is None:
        # Hobby einfügen, wenn es nicht existiert
        pg_cursor.execute(
            """
            INSERT INTO Hobbys (Name) VALUES (%s) RETURNING Hobby_ID;
            """,
            (hobby_name,)
        )
        hobby_id = pg_cursor.fetchone()[0]
    
    return hobby_id

# Funktion, um Benutzer und deren Hobbys zu verknüpfen
def insert_user_hobbies(user_email, hobbies):
    # Hole User_ID aus der E-Mail
    pg_cursor.execute(
        """
        SELECT User_ID FROM Anmeldedaten WHERE email = %s;
        """,
        (user_email,)
    )
    user_id = pg_cursor.fetchone()

    if user_id is None:
        print(f"Benutzer mit E-Mail {user_email} nicht gefunden.")
        return

    user_id = user_id[0]

    # Hobbys für diesen Benutzer einfügen
    for prio, hobby in enumerate(hobbies, 1):
        hobby_id = insert_hobby(hobby)  # Hole oder füge das Hobby ein
        pg_cursor.execute(
            """
            INSERT INTO User_Hobbys (User_ID, Hobby_ID, Prio)
            VALUES (%s, %s, %s);
            """,
            (user_id, hobby_id, prio)
        )

# XML-Datei einlesen und parsen
tree = ET.parse('users.xml')
root = tree.getroot()

# Benutzer und deren Hobbys in die Datenbank einfügen
for user in root.findall('user'):
    email = user.find('email').text
    name = user.find('name').text
    hobbies = [hobby.text for hobby in user.findall('hobby')]

    # Benutzer und Hobbys in die Datenbank einfügen
    insert_user_hobbies(email, hobbies)

# Änderungen speichern und Verbindungen schließen
pg_conn.commit()
pg_cursor.close()
pg_conn.close()