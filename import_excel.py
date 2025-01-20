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

                # 2) Hobbys
                hobbies_str = row.get('Hobbys')
                hobbies = parse_hobbies(hobbies_str)

                # 3) Email
                email = row.get('E-Mail')
                if not isinstance(email, str):
                    print(f"Fila {index}: email no válido => se omite.")
                    continue
                email = email.strip()

                # Verificar si el email ya existe
                cursor.execute("SELECT user_id FROM anmeldedaten WHERE email = %s", (email,))
                existing_user = cursor.fetchone()
                if existing_user:
                    print(f"Fila {index}: email ya existe ({email}) => se omite.")
                    continue

                # 4) Género
                gender = parse_gender(row.get('Geschlecht'))

                # 5) Interessiert an
                interested_in = parse_interessiert_an(row.get('Interessiert an'))

                # 6) Fecha Nacimiento
                birthday = parse_birthday(row.get('Geburtsdatum'))

                # =====================
                # Insertar en users
                # =====================
                insert_user_sql = """
                    INSERT INTO users (vorname, nachname, gender, interessiert_an, birthday)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING user_id
                """
                cursor.execute(insert_user_sql, (
                    first_name,
                    last_name,
                    gender,
                    interested_in,
                    birthday
                ))
                user_id = cursor.fetchone()[0]

                # =====================
                # Insertar en anmeldedaten
                # =====================
                insert_anmeldedaten_sql = """
                    INSERT INTO anmeldedaten (user_id, email, password_hash, status)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_anmeldedaten_sql, (
                    user_id,
                    email,
                    "dummyhash",
                    "active"
                ))

                # =====================
                # Insertar hobbies
                # =====================
                for (hobby_name, prio) in hobbies:
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
