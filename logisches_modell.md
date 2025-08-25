# Logisches Modell (Relationales Modell)

In diesem Dokument wird das **logische Modell** präsentiert, das aus der Transformation des ER-Diagramms in das relationale Modell hervorgegangen ist. Es zeigt die Haupttabellen, ihre Attribute, Primärschlüssel (PK), Fremdschlüssel (FK) und Beziehungen:

## Tabellen und Attributdefinitionen

1. **Users**
   - **user_id** (PK, SERIAL)
   - vorname (VARCHAR)
   - nachname (VARCHAR)
   - geschlecht (VARCHAR)
   - interessiert_an (VARCHAR)
   - geburtsdatum (DATE)
   - created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
   - updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

2. **Anmeldedaten**
   - **user_id** (PK, FK → Users.user_id)
   - email (VARCHAR) [UNIQUE NOT NULL]
   - password_hash (VARCHAR)
   - timestamp_last_login (TIMESTAMP)
   - status (VARCHAR)

3. **Hobbys**
   - **hobby_id** (PK, SERIAL)
   - name (VARCHAR)

4. **User_Hobbys** (Zwischentabelle N:N zwischen Users und Hobbys)
   - **user_id** (PK, FK → Users.user_id)
   - **hobby_id** (PK, FK → Hobbys.hobby_id)
   - prio (INT)

5. **User_Bilder**
   - **bild_id** (PK, SERIAL)
   - user_id (FK → Users.user_id)
   - image (BYTEA)
   - is_profilepicture (BOOLEAN)
   - timestamp_upload (TIMESTAMP)

6. **Likes**
   - **liker_user_id** (PK, FK → Users.user_id)
   - **liked_user_id** (PK, FK → Users.user_id)
   - created_at (TIMESTAMP)
   - status (VARCHAR)

7. **Nachrichten** (Messages)
   - **message_id** (PK, SERIAL)
   - sender_user_id (FK → Users.user_id)
   - receiver_user_id (FK → Users.user_id)
   - message_content (TEXT)
   - created_at (TIMESTAMP)
   - status (VARCHAR)

8. **Freunde** (Tabelle für die Beziehung „Freunde“)
   - **friendship_id** (PK, SERIAL)
   - user_id1 (FK → Users.user_id)
   - user_id2 (FK → Users.user_id)
   - created_at (TIMESTAMP)

## Begründung der Normalisierung (3NF)

- Jede Tabelle beschreibt eine spezifische Entität oder Beziehung.
- Informationen wurden in separate Tabellen aufgeteilt, um Redundanzen zu vermeiden (z. B. `Users` und `Anmeldedaten`).
- Funktionale Abhängigkeiten werden innerhalb jeder Tabelle eingehalten, um doppelte Daten zu vermeiden.
- Das Schema entspricht der dritten Normalform (3NF), da:
  - Nicht-Schlüsselfelder hängen direkt vom Primärschlüssel ab.
  - Es gibt keine transitiven Abhängigkeiten, die die Normalisierung verletzen.

## Beziehungen zwischen Tabellen (Zusammenfassung)

- `Users (1) — (1) Anmeldedaten`
- `Users (1) — (N) User_Bilder`
- `Users (1) — (N) Nachrichten` (über sender_user_id oder receiver_user_id)
- `Users (N) — (N) Hobbys` (über User_Hobbys)
- `Users (N) — (N) Users` (über Likes oder Freunde)
- usw.

---
