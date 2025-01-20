import pandas as pd
import psycopg2
from datetime import datetime

# Configuración de la conexión a PostgreSQL
DB_HOST = "localhost"
DB_NAME = "lf8_lets_meet_db"
DB_USER = "user"
DB_PASS = "secret"

# Ruta al archivo Excel
EXCEL_FILE_PATH = "/workspace/LetsMeet/Lets Meet DB Dump.xlsx"

def parse_name(full_name):
    """
    Asegura que 'Nachname, Vorname' tenga la coma necesaria.
    Devuelve (apellido, nombre) o (None, None) si es inválido.
    """
    if not full_name or not isinstance(full_name, str):
        return (None, None)
    if ',' not in full_name:
        return (None, None)
    try:
        last_name, first_name = map(str.strip, full_name.split(',', 1))
        return (last_name, first_name)
    except:
        return (None, None)

def parse_gender(gender):
    """
    'Geschlecht': puede ser 'm', 'w', 'd' o nulo.
    Si no coincide con esos valores, lo ponemos en None.
    """
    if not gender or not isinstance(gender, str):
        return None
    gender = gender.lower().strip()
    if gender in ['m', 'w', 'd']:
        return gender
    return None

def parse_birthday(birthday):
    """
    Convierte la fecha. Si no es válida, devuelve None.
    """
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
    Espera cadenas separadas por ';', cada una en formato 'Hobby%17%' (por ejemplo).
    Devuelve lista de (hobby, prioridad). Ignora entradas mal formadas.
    """
    if not hobbies_str or not isinstance(hobbies_str, str):
        return []
    items = hobbies_str.split(';')
    result = []
    for item in items:
        parts = item.split('%')
        if len(parts) < 2:
            continue
        hobby_name = parts[0].strip()
        try:
            prio_raw = parts[1].strip()
            prio = int(prio_raw)
        except:
            prio = 0
        if hobby_name:
            result.append((hobby_name, prio))
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
        # Para que cada fila sea una transacción independiente
        conn.autocommit = False
        cursor = conn.cursor()
        print("Conexión a PostgreSQL exitosa.")

        # Leer el archivo Excel con pandas
        df = pd.read_excel(EXCEL_FILE_PATH)
        print("Archivo Excel leído exitosamente.")

        for index, row in df.iterrows():
            try:
                # ========== NOMBRE ==========
                full_name = row.get('Nachname, Vorname')
                last_name, first_name = parse_name(full_name)
                if not last_name or not first_name:
                    print(f"Fila {index}: 'Nachname, Vorname' no válido => se omite.")
                    continue

                # ========== GÉNERO ==========
                gender = parse_gender(row.get('Geschlecht'))

                # ========== FECHA DE NACIMIENTO ==========
                birthday = parse_birthday(row.get('Geburtsdatum'))

                # INSERT en tabla users (SIN teléfono ni dirección)
                insert_user_sql = """
                    INSERT INTO users (vorname, nachname, gender, birthday)
                    VALUES (%s, %s, %s, %s)
                    RETURNING user_id
                """
                cursor.execute(insert_user_sql, (first_name, last_name, gender, birthday))
                user_id = cursor.fetchone()[0]

                # ========== HOBBIES ==========
                hobbies_str = row.get('Hobbys')
                hobbies = parse_hobbies(hobbies_str)

                for hobby_name, priority in hobbies:
                    # Verificamos si existe el hobby
                    cursor.execute("SELECT hobby_id FROM hobbys WHERE name = %s", (hobby_name,))
                    result = cursor.fetchone()
                    if result:
                        hobby_id = result[0]
                    else:
                        cursor.execute("INSERT INTO hobbys (name) VALUES (%s) RETURNING hobby_id", (hobby_name,))
                        hobby_id = cursor.fetchone()[0]

                    # Insertamos en la tabla intermedia user_hobbys
                    insert_user_hobby_sql = """
                        INSERT INTO user_hobbys (user_id, hobby_id, prio)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_user_hobby_sql, (user_id, hobby_id, priority))

                # Confirmamos esta fila
                conn.commit()

            except Exception as e:
                # Si algo falla en esta fila, revertimos solo esta transacción
                conn.rollback()
                print(f"Fila {index} dio error: {e}")

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
