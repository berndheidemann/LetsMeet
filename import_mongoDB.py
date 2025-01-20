import psycopg2
from pymongo import MongoClient
import random
import string

# PostgreSQL connection setup
DB_HOST = "localhost"
DB_NAME = "lf8_lets_meet_db"
DB_USER = "user"
DB_PASS = "secret"

# MongoDB connection setup
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["LetsMeet"]  # Hier den Namen der MongoDB-Datenbank angeben
mongo_collection = mongo_db["users"]  # Hier den Namen der MongoDB-Collection angeben

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# Function to generate a random string for password_hash
def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Iterate over MongoDB users and process data
for mongo_user in mongo_collection.find():
    user_email = mongo_user["_id"]
    user_name = mongo_user["name"]
    created_at = mongo_user["createdAt"]
    updated_at = mongo_user["updatedAt"]

    # Insert into the 'users' table
    cursor.execute("""
        INSERT INTO users (vorname, nachname, created_at, updated_at)
        VALUES (%s, %s, %s, %s) RETURNING user_id
    """, (user_name.split(", ")[1], user_name.split(", ")[0], created_at, updated_at))

    user_id = cursor.fetchone()[0]

    # Insert into 'anmeldedaten' table with a placeholder for password_hash
    cursor.execute("""
        INSERT INTO anmeldedaten (user_id, email, password_hash)
        VALUES (%s, %s, %s)
    """, (user_id, user_email, generate_random_string()))  # Placeholder for password_hash

    # Process likes and insert into 'likes' table
    for like in mongo_user.get("likes", []):
        liked_email = like["liked_email"]
        status = like["status"]
        timestamp = like["timestamp"]

        # Get the user_id of the liked user from the email
        cursor.execute("SELECT user_id FROM anmeldedaten WHERE email = %s", (liked_email,))
        liked_user_id = cursor.fetchone()

        if liked_user_id:
            liked_user_id = liked_user_id[0]
            liker_user_id = user_id if user_id < liked_user_id else liked_user_id
            liked_user_id = liked_user_id if user_id < liked_user_id else user_id

            cursor.execute("""
                INSERT INTO likes (liker_user_id, liked_user_id, timestamp, status)
                VALUES (%s, %s, %s, %s)
            """, (liker_user_id, liked_user_id, timestamp, status))

            # Check for mutual likes and insert into 'freunde' table
            if status == "mutual":
                if liker_user_id < liked_user_id:
                    cursor.execute("""
                        INSERT INTO freunde (user_id1, user_id2)
                        VALUES (%s, %s)
                    """, (liker_user_id, liked_user_id))
                else:
                    cursor.execute("""
                        INSERT INTO freunde (user_id1, user_id2)
                        VALUES (%s, %s)
                    """, (liked_user_id, liker_user_id))

    # Process messages and insert into 'nachrichten' table
    for message in mongo_user.get("messages", []):
        receiver_email = message["receiver_email"]
        message_content = message["message"]
        timestamp = message["timestamp"]

        # Get the user_id of the receiver from the email
        cursor.execute("SELECT user_id FROM anmeldedaten WHERE email = %s", (receiver_email,))
        receiver_user_id = cursor.fetchone()

        if receiver_user_id:
            receiver_user_id = receiver_user_id[0]
            cursor.execute("""
                INSERT INTO nachrichten (sender_user_id, receiver_user_id, message_content, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (user_id, receiver_user_id, message_content, timestamp))

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()