import pandas as pd
import psycopg2
from datetime import datetime

# Configuración de la conexión a PostgreSQL
DB_HOST = "localhost"
DB_NAME = "lf8_lets_meet_db"
DB_USER = "user"
DB_PASS = "secret"

EXCEL_FILE_PATH = "/workspace/LetsMeet/Lets Meet DB Dump.xlsx"

def parse_name(full_name):
    """
    'Nachname, Vorname' -> (apellido, nombre)
    """
    if not full_name or not isinstance(full_name, str):
        return (None, None)
    if ',' not in full_name:
        # No está en formato "Nachname, Vorname"
        return (None, None)
    try:
        last_name, first_name = map(str.strip, full_name.split(',', 1))
        return (last_name, first_name)
    except:
        return (None, None)

def parse_gender(gender_str):
    if not isinstance(gender_str, str):
        return None
    gender_str = gender_str.strip().lower()
    # Normaliza a 'm', 'w', 'd' (opcional)
    if gender_str in ['m', 'männlich']:
        return 'm'
    elif gender_str in ['w', 'weiblich']:
        return 'w'
    elif 'nicht' in gender_str or 'binär' in gender_str or gender_str == 'd':
        return 'd'
    return None

def parse_interessiert_an(value):
    # Simplemente lo devolvemos tal cual
    if not isinstance(value, str):
        return None
    return value.strip()

def parse_birthday(birthday):
    if pd.isnull(birthday):
        return None
    try:
        birthday_parsed = pd.to_datetime(birthday, dayfirst=True, errors='coerce')
        if pd.isnull(birthday_parsed):
            return None
        return birthday_parsed.date()
    except:
        return None

def parse_hobbies(hobbies_str):
    """
    Espera: "Hobby1%prio1%;Hobby2%prio2%;..."
    Devuelve lista de (hobby, prio).
    """
    if not hobbies_str or not isinstance(hobbies_str, str):
        return []
    items = hobbies_str.split(';')
    result = []
    for item in items:
        parts = item.split('%')
        # parts = ['Hobby1', 'prio1', '']
        if len(parts) < 2:
            continue
        hobby_name = parts[0].strip()
        # El prio irá en la 1 si es Hoby%123% ...
        # a veces puede haber parte final vacía
        prio_val = 0
        if len(parts) >= 2:
            try:
                prio_val = int(parts[1])
            except:
                prio_val = 0
        if hobby_name:
            result.append((hobby_name, prio_val))
    return result

def main():
    conn = None
    cursor = None

    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        conn.autocommit = False
        cursor = conn.cursor()
        print("Conexión a PostgreSQL exitosa.")

        # Leer el archivo Excel
        df = pd.read_excel(EXCEL_FILE_PATH)
        print("Archivo Excel leído exitosamente.")

        for index, row in df.iterrows():
            try:
                # 1) Nombre
                full_name = row.get('Nachname, Vorname')
                last_name, first_name = parse_name(full_name)
                if not last_name or not first_name:
                    print(f"Fila {index}: nombre no válido => se omite.")
                    continue

                # 2) Dirección
                address = row.get('Adresse')
                if not isinstance(address, str):
                    address = None

                # 3) Teléfono
                phone = row.get('Telefon')
                if isinstance(phone, str):
                    # Si hay varios separadores, tomar todo o el primero
                    # phone = phone.split(',')[0].strip()  # si solo quieres el primero
                    phone = phone.strip()
                else:
                    phone = None

                # 4) Hobbys
                hobbies_str = row.get('Hobbys')
                hobbies = parse_hobbies(hobbies_str)

                # 5) Email
                email = row.get('E-Mail')
                if not isinstance(email, str):
                    print(f"Fila {index}: email no válido => se omite.")
                    continue
                email = email.strip()

                # 6) Género
                gender = parse_gender(row.get('Geschlecht'))

                # 7) Interessiert an
                interested_in = parse_interessiert_an(row.get('Interessiert an'))

                # 8) Fecha Nacimiento
                birthday = parse_birthday(row.get('Geburtsdatum'))

                # =====================
                # Insertar en users
                # =====================
                insert_user_sql = """
                    INSERT INTO users (vorname, nachname, phone, address, gender, interessiert_an, birthday)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING user_id
                """
                cursor.execute(insert_user_sql, (
                    first_name,
                    last_name,
                    phone,
                    address,
                    gender,
                    interested_in,
                    birthday
                ))
                user_id = cursor.fetchone()[0]

                # =====================
                # Insertar en anmeldedaten
                # =====================
                # No tenemos password en Excel, creamos uno "dummy"
                insert_anmeldedaten_sql = """
                    INSERT INTO anmeldedaten (user_id, email, password_hash, status)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_anmeldedaten_sql, (
                    user_id,
                    email,
                    "dummyhash",   # en la realidad aquí usarías un hash real
                    "active"
                ))

                # =====================
                # Insertar hobbies
                # =====================
                for (hobby_name, prio) in hobbies:
                    # Ver si ya existe
                    cursor.execute("SELECT hobby_id FROM hobbys WHERE name = %s", (hobby_name,))
                    row_hobby = cursor.fetchone()
                    if row_hobby:
                        hobby_id = row_hobby[0]
                    else:
                        cursor.execute("INSERT INTO hobbys (name) VALUES (%s) RETURNING hobby_id",
                                       (hobby_name,))
                        hobby_id = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO user_hobbys (user_id, hobby_id, prio)
                        VALUES (%s, %s, %s)
                    """, (user_id, hobby_id, prio))

                conn.commit()

            except Exception as e:
                conn.rollback()
                print(f"Error en fila {index}: {e}")

        print("Importación finalizada.")

    except Exception as e:
        print(f"Error global: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Conexión a PostgreSQL cerrada.")

if __name__ == "__main__":
    main()
