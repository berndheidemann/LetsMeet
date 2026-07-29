# Lernsituation: LetsMeet-Datenmigration

Die **Let’s Meet GmbH** wechselt nach einer schwierigen Trennung den IT-Dienstleister. Statt einer
laufenden Datenbank liegen nur schrittweise freigegebene Datenstände vor. Euer
Team rekonstruiert daraus eine PostgreSQL-Datenbank, die eine
Anzeige-App der Kundin wieder versorgen kann.

![Ausschnitt aus „Tea with friends, and one must wear one's finest hat!“ (Public Domain)](./images/tea-with-friends.png)

## Euer Arbeitsauftrag

Ihr arbeitet in drei Akten. Akt 1 und Akt 2 sind unten vollständig beschrieben. Für jeden aktuell
freigegebenen Akt baut ihr die Datenbank mit euren Skripten **aus einer leeren PostgreSQL-Datenbank neu auf**
und prüft das Ergebnis. Ein anderes Team muss denselben Aufbau wiederholen können — genau das ist
mit einem reproduzierbaren Import gemeint. Die Tabellen hinter den geforderten
Datenbankansichten (Views) dürft ihr selbst entwerfen.

- Versioniert SQL, Importcode, eigene Datenprüfungen und kurze Markdown-Dokumentationen mit Git.
- Erstellt physische Modelle und die zugehörigen SQL-Anweisungen zur Definition der
  Datenbankstruktur (DDL) für die aufgenommenen Quelldaten und das PostgreSQL-Zielsystem.
- Dokumentiert Annahmen, Transformationsregeln, Konfliktentscheidungen und nicht übernommene
  Datensätze nachvollziehbar.
- Der Prüfstand in der Kundinnen-App gibt euch Hinweise zum Weiterarbeiten. Für den Abschluss eines
  Akts zählt der Prüfbefehl im Terminal nach einem frischen Datenbankaufbau.
- Haltet ihr ein rotes Ergebnis für fachlich falsch, gebt der Lehrkraft Quelle, betroffenen
  Datensatz und eure Begründung.

Die Begleit-Website führt euch durch die Übergänge:

**[LetsMeet-Projektbegleitung öffnen](https://station.heidelab.de/letsmeet/)**

Sie speichert euren Stand nur lokal im Browser. Sie ist keine Abgabe und prüft weder Datenbank noch
ER-Diagramm selbst.

## Technischer Start

```bash
docker compose up -d
```

Danach sind erreichbar:

- PostgreSQL: `localhost:5432`, Datenbank `lf8_lets_meet_db`
- MongoDB: `localhost:27017`, Datenbank `LetsMeet`
- Kundinnen-App und Prüfstand: [http://localhost:3611](http://localhost:3611)

PostgreSQL-Zugang: Benutzer `user`, Passwort `secret`.

Die Kürzel V1, V2 und V3 bezeichnen die technischen Datenverträge für Akt 1, Akt 2 und Akt 3.
In Befehlen müsst ihr diese Kürzel genau so verwenden. Die Kundinnen-App startet mit V1. Wenn ein
späterer Akt den nächsten Datenvertrag freigibt, startet ihr nur die Kundinnen-App mit der dort
genannten Version neu. Beispiel für Akt 2 mit V2:

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

PowerShell:

```powershell
$env:LETSMEET_CONTRACT_VERSION="V2"
docker compose up -d --force-recreate kundinnen_app
```

Der Verlauf eurer Prüfläufe und die dazugehörigen technischen Prüfdateien liegen im Volume
`lf8_lets_meet_check_history` und bleiben beim Container-Neustart erhalten.

---

# Akt 1 — Erste Daten aus Excel bis zur Kundinnen-App bringen

## Ausgangslage

Quelle ist [`Lets Meet DB Dump.xlsx`](./Lets%20Meet%20DB%20Dump.xlsx). Darin stehen Name,
Adresse, Telefon, fünf priorisierte Hobbys, E-Mail-Adresse, Geschlecht, Interessen und
Geburtsdatum in teilweise zusammengesetzten Feldern.

## Auftrag

1. Profiliert die Quelle und haltet auffällige Formate, Mehrfachwerte und offene Fragen fest.
2. Erstellt das minimale physische Modell und einen Import aus einer **leeren** Datenbank.
3. Stellt die folgende View bereit. Eure internen Tabellen und Joins bleiben eure Entscheidung.
4. Öffnet die Kundinnen-App und untersucht sichtbare Folgen eurer Importentscheidungen.
5. Schreibt eigene SQL-Abfragen oder automatisierte Tests für eure zentralen Importannahmen.
6. Dokumentiert Importbefehl, Testergebnisse und bekannte Grenzen.

## Datenvertrag für Akt 1 (V1)

Die View ist die vereinbarte Schnittstelle zwischen eurer Datenbank und der Kundinnen-App:

```sql
-- Pflicht-View, Spaltennamen und -typen exakt:
-- migration_users(email text, first_name text, last_name text,
--                 birth_date date, postal_code text, city text)

CREATE VIEW migration_users AS
SELECT ... FROM ...;
```

Regeln:

- eine Zeile pro migrierter Person;
- `email` eindeutig und nicht leer;
- keine Platzhalter für misslungene Zeilen — was nicht importiert ist, fehlt sichtbar;
- vor dem Textvergleich normalisiert der Prüfstand Texte auf Unicode-NFC; in Akt 1 bleiben die
  Inhalte einschließlich äußerer Leerzeichen ansonsten genau wie in der Quelle;
- `city` enthält den vollständigen Ortsnamen aus der Quelle, auch wenn darin ein Komma vorkommt.

## Abschluss von Akt 1: Neuaufbau prüfen

Baut euren Excel-Import mit euren Skripten in einer leeren Datenbank neu auf. Führt danach diesen
Prüfbefehl im Terminal aus:

```bash
docker compose run --rm -e CONTRACT_VERSION=V1 kundinnen_app \
  node server/dist/cli.js
```

Endet der Befehl mit Exit-Code `0` — also ohne Fehler —, ist die Abschlussprüfung für Akt 1
bestanden. Setzt danach in der Begleit-Website den Haken für Akt 1; dort öffnet sich Akt 2.

---

# Akt 2 — Zielmodell und MongoDB

## Modellierungsauftrag

Bearbeitet zuerst die in der Begleit-Website angezeigten Trainingsfälle für
Entity-Relationship-Diagramme (ERD). Öffnet danach dort die LetsMeet-Modellierungsstation,
entwickelt ER-Diagramm und relationales Schema und registriert die vollständige Freigabe-URL
(Share-URL) eures Modells. Sichert dieselbe URL zusätzlich in eurer Projektdokumentation.

Berücksichtigt dabei:

- Transformation ins Relationenmodell und dritte Normalform; siehe
  [`normalization.md`](./normalization.md);
- priorisierte und ausdrücklich nicht gemochte Hobbys (`-100` bis `100`);
- Freundeslisten;
- ein direkt gespeichertes Profilbild sowie weitere hochgeladene oder verlinkte Fotos;
- Datenschutz: Datenarten, Rechtsgrundlage, Schutzbedarf und technische/organisatorische
  Maßnahmen;
- je Anwendungsfall eine beispielhafte SQL-Abfrage;
- physische Modelle und die zugehörige DDL sowohl für die aufgenommenen Quelldaten als auch für
  das PostgreSQL-Zielsystem;
- eigene Tests für Mengen, Eindeutigkeit, Referenzen und zentrale Transformationsregeln — der
  Kundinnen-Checker ergänzt diese, ersetzt sie aber nicht.

![Anwendungsfalldiagramm für die LetsMeet-Datenbank](./images/use-case.png)

## MongoDB-Quelle

Das Backup läuft bereits im Compose-Service `mongodb_for_lf8`. Die Sammlung `users` enthält
ergänzende Profildaten sowie gerichtete Likes und Nachrichten. Analysiert insbesondere
verschachtelte Datensätze, Referenzen, Mehrfachwerte und Widersprüche zur Excel-Quelle. Holt für
offene fachliche Konflikte eine Kundinnenentscheidung ein und dokumentiert die angewandte Regel.

## Datenvertrag für Akt 2 (V2)

V2 erweitert den Datenvertrag aus Akt 1. Für `migration_users` gilt jetzt der neue Spaltensatz;
zusätzlich kommen vier weitere Views hinzu:

```sql
-- Pflicht-Views, Namen und Typen exakt:
-- migration_users(email text, first_name text, last_name text, birth_date date,
--                 postal_code text, city text, phone text, gender text)
-- migration_user_interests(email text, interest_code text)
-- migration_user_hobbies(email text, hobby_name text, priority integer, source text)
-- migration_likes(liker_email text, liked_email text, status text, liked_at timestamp)
-- migration_messages(sender_email text, receiver_email text, body text,
--                    sent_at timestamp, conversation_id integer)
```

Regeln:

- Eine Zeile je Sachverhalt. Mehrere Interessen ergeben mehrere Zeilen; dasselbe Hobby aus
  derselben Quelle erscheint nur einmal.
- `source` dokumentiert die Herkunft einer Hobbyzuordnung; in Akt 2 ist sie `excel`.
- Likes und Nachrichten sind gerichtet: Absender beziehungsweise auslösende Person stehen links.
- Bei widersprüchlichen Kontaktdaten gilt die eingeholte und dokumentierte Kundinnenentscheidung.
- Textvergleich wie in Akt 1; Zeitpunkte werden als Zeitwerte und auf die Sekunde genau verglichen.

Startet die Anzeige-App für Akt 2 neu:

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

## Abschluss von Akt 2: Gemeinsamen Neuaufbau prüfen

Baut Excel- und MongoDB-Import gemeinsam in einer leeren Datenbank neu auf. Führt danach diesen
Prüfbefehl im Terminal aus:

```bash
docker compose run --rm -e CONTRACT_VERSION=V2 kundinnen_app \
  node server/dist/cli.js
```

Endet der Befehl mit Exit-Code `0` — also ohne Fehler —, ist die Abschlussprüfung für Akt 2
bestanden. Registriert vorher eure ERD-Share-URL und setzt anschließend in der Begleit-Website den
Haken für Akt 2. Danach folgt die nächste Anweisung.

---

# Akt 3 — Fortsetzung

Beginnt Akt 3 erst, wenn euch der nächste Auftrag angezeigt wird. Bis dahin sind ausschließlich
Akt 1 und Akt 2 verbindlich.

---

# Erwartete Repository-Artefakte

Eine mögliche Struktur:

```text
results/
  quellenanalyse.md
  konzeptuelles_modell.md
  logisches_modell.md
  physische_modelle.md
  datenschutz.md
  konfliktentscheidungen.md
  scripts/
    create_tables.sql
    import_excel.*
    import_mongodb.*
    tests/
```

Verbindlich ist nicht der Dateiname. Ein anderes Team muss eure Datenbank mit euren Skripten aus
einer leeren PostgreSQL-Datenbank neu aufbauen, eure Entscheidungen nachvollziehen und die Prüfbefehle für
die Akte erneut ausführen können.

## Datenbankzugriff in Werkzeugen

PostgreSQL-Verbindungsdaten für DBeaver, SQLTools oder `psql`:

```text
Host: localhost
Port: 5432
Datenbank: lf8_lets_meet_db
Benutzer: user
Passwort: secret
```

MongoDB-Verbindungs-URI für Compass oder die VS-Code-Erweiterung:

```text
mongodb://localhost:27017/LetsMeet
```

## Lokalen Datenstand vollständig zurücksetzen

```bash
docker compose down -v
```

**Achtung:** Dieser Befehl löscht eure lokalen PostgreSQL- und MongoDB-Daten sowie den Verlauf der
Prüfläufe. Nutzt ihn nur, wenn ihr wirklich wieder mit leeren Datenbanken beginnen möchtet. Euer
Git-Stand bleibt erhalten.
