import xml.etree.ElementTree as ET
import psycopg2
import random

DB_HOST = "localhost"
DB_NAME = "lf8_lets_meet_db"
DB_USER = "user"
DB_PASS = "secret"

def get_or_create_user(email, full_name, conn):
    with conn.cursor() as cur:
        # Prüfen, ob der Nutzer bereits existiert
        cur.execute("SELECT user_id FROM anmeldedaten WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            return user[0]

        # Name trennen
        if "," in full_name:
            nachname, vorname = map(str.strip, full_name.split(",", 1))
        else:
            vorname = full_name.strip()
            nachname = "Platzhalter"

        # Neuen Nutzer anlegen
        cur.execute(
            """
            INSERT INTO users (vorname, nachname, phone, address, gender, birthday)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id
            """,
            (vorname, nachname, "000000", "Platzhalterstraße", "Unbekannt", "2000-01-01"),
        )
        user_id = cur.fetchone()[0]

        # In anmeldedaten einfügen
        cur.execute(
            """
            INSERT INTO anmeldedaten (user_id, email, password_hash, status)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, email, "hashed_password", "active"),
        )

        conn.commit()
        return user_id

def insert_hobby_if_not_exists(hobby_name, conn):
    with conn.cursor() as cur:
        # Prüfen, ob das Hobby existiert
        cur.execute("SELECT hobby_id FROM hobbys WHERE name = %s", (hobby_name,))
        hobby = cur.fetchone()

        if hobby:
            return hobby[0]

        # Neues Hobby hinzufügen
        cur.execute("INSERT INTO hobbys (name) VALUES (%s) RETURNING hobby_id", (hobby_name,))
        hobby_id = cur.fetchone()[0]

        conn.commit()
        return hobby_id

def insert_user_hobbies(user_id, hobbies, conn):
    with conn.cursor() as cur:
        for hobby_name in hobbies:
            hobby_id = insert_hobby_if_not_exists(hobby_name, conn)

            # Prüfen, ob die Kombination aus user_id und hobby_id existiert
            cur.execute(
                "SELECT 1 FROM user_hobbys WHERE user_id = %s AND hobby_id = %s",
                (user_id, hobby_id),
            )
            if not cur.fetchone():
                prio = random.randint(1, 10)
                cur.execute(
                    "INSERT INTO user_hobbys (user_id, hobby_id, prio) VALUES (%s, %s, %s)",
                    (user_id, hobby_id, prio),
                )

        conn.commit()

def process_xml():
    tree = ET.parse("Lets_Meet_Hobbies.xml")
    root = tree.getroot()

    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

    for user in root.findall("user"):
        email = user.find("email").text
        full_name = user.find("name").text
        hobbies = [hobby.text for hobby in user.findall("hobbies/hobby")]

        user_id = get_or_create_user(email, full_name, conn)
        insert_user_hobbies(user_id, hobbies, conn)

    conn.close()

if __name__ == "__main__":
    process_xml()
