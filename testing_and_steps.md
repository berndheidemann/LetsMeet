# Dokumentation der Schritte und Tests

Diese Datei beschreibt die durchgeführten Zwischenschritte und wie die Konsistenz und Integrität der Daten validiert wurde.

## 1. Erstellung und Bereinigung von Tabellen
- Die `CREATE TABLE`-Skripte wurden ausgeführt (siehe Datei `create_tables.sql`).
- Um eine saubere Umgebung sicherzustellen, wurde `DROP TABLE IF EXISTS ... CASCADE` verwendet.

## 2. Datenimport
- **Excel**: Das Skript `import_excel.py` wurde verwendet.
  - Überprüfung mit `SELECT COUNT(*) FROM users;` und Abgleich, ob die Anzahl der Zeilen wie erwartet ist.
  - Einige Fälle wurden manuell überprüft, um das Parsen von Namen und Hobbys zu validieren.
- **MongoDB**: Das Skript `import_mongodb.py` wurde verwendet.
  - Überprüfung, ob Likes und Nachrichten in den Tabellen `likes` und `nachrichten` existieren.
  - Sicherstellung, dass die E-Mails in `mongo_user["_id"]` mit der Tabelle `anmeldedaten` übereinstimmen.
- **XML**: Das Skript `import_xml.py` wurde verwendet.
  - Überprüfung der Tabelle `user_hobbys`, um sicherzustellen, dass die Hobbys eingefügt wurden.
  - Überprüfung, dass neue Benutzer erstellt wurden, falls sie nicht existierten.

## 3. Ausführung von Validierungsabfragen
- Beispielabfragen wurden getestet (siehe `consultas_sql_ejemplos.md` oder vorheriger Abschnitt).
- Überprüft wurde, dass:
  - Vor- und Nachnamen mit denen aus der Excel-Datei übereinstimmen.
  - Likes korrekt als pending, mutual usw. angezeigt werden.
  - Nachrichten mit dem richtigen Inhalt erscheinen.

## 4. Überprüfung von Einschränkungen und Beziehungen
- Es wurde geprüft, ob die FK `user_id` in `anmeldedaten` tatsächlich auf `users` verweist.
- Die FKs `liker_user_id` und `liked_user_id` in `likes` wurden validiert.
- Unerlaubte Inserts (z. B. ein nicht existierendes `user_id`) wurden getestet, und es wurde bestätigt, dass ein referenzieller Integritätsfehler auftritt.

## 5. Fazit
- Mit diesen Tests wurde bestätigt, dass die Datenmigration funktioniert und die Datenbank die Konsistenzanforderungen erfüllt.

---
