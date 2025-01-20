# Verwendung von Git und Versionskontrolle

1. Ein Repository wurde in [GitHub / GitLab / etc.] erstellt.
2. Der Hauptordner enthält:
   - `create_tables.sql`
   - `import_excel.py`
   - `import_mongodb.py`
   - `import_xml.py`
   - `konzeptuelles_modell.md`
   - `logisches_modell.md`
   - `testing_and_steps.md`
   - (und weitere Skripte / Konfigurationsdateien)
3. Jede Änderung am Modell, an den Importskripten und an den Tests wurde in **separaten Commits** mit beschreibenden Nachrichten durchgeführt.
4. Jede Lieferung oder Meilenstein wurde mit einem Tag versehen, um stabile Versionen identifizieren zu können.
5. Der gesamte Prozess (Datenbank erstellen, Daten importieren, Tests ausführen) kann von Grund auf reproduziert werden.

---
