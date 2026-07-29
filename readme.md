# Lernsituation: LetsMeet-Datenmigration

Die **Let’s Meet GmbH** wechselt nach einer schwierigen Trennung den IT-Dienstleister. Statt einer
laufenden Datenbank liegen nur schrittweise freigegebene Datenstände vor. Euer
Team rekonstruiert daraus eine PostgreSQL-Datenbank, die eine
Anzeige-App der Kundin wieder versorgen kann.

![Ausschnitt aus „Tea with friends, and one must wear one's finest hat!“ (Public Domain)](./images/tea-with-friends.png)

## Euer Arbeitsauftrag

Ihr arbeitet in drei Akten. Akt 1 und Akt 2 sind unten vollständig beschrieben. Für jeden aktuell
freigegebenen Akt erzeugt ihr einen **reproduzierbaren Import aus einer leeren Datenbank** und
prüft ihn gegen die dort genannten Anforderungen. Die Tabellen hinter den geforderten Views dürft
ihr selbst entwerfen.

- Versioniert SQL, Importcode, eigene Datenprüfungen und kurze Markdown-Dokumentationen mit Git.
- Erstellt physische Modelle beziehungsweise DDL für die aufgenommenen Quelldaten und das
  PostgreSQL-Zielsystem.
- Dokumentiert Annahmen, Transformationsregeln, Konfliktentscheidungen und nicht übernommene
  Datensätze nachvollziehbar.
- Der Browser-Prüfstand gibt formatives Feedback. Für ein Akt-Gate zählt ausschließlich der
  CLI-Repro-Lauf aus einer leeren Datenbank.
- Haltet ihr ein rotes Ergebnis für fachlich falsch, eskaliert es mit Quelle, betroffenem
  Datensatz und Begründung an die Lehrkraft.

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

Die Kundinnen-App startet mit Vertragsversion V1. Wenn ein späterer Akt eine neue Vertragsversion
freigibt, startet ihr nur diesen Service mit der dort genannten Version neu. Beispiel für V2:

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

PowerShell:

```powershell
$env:LETSMEET_CONTRACT_VERSION="V2"
docker compose up -d --force-recreate kundinnen_app
```

Die Check-Historie und technische Gate-Artefakte liegen im Volume
`lf8_lets_meet_check_history` und bleiben beim Container-Neustart erhalten.

---

# Akt 1 — Walking Skeleton aus Excel

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

## Migrationsvertrag V1

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
- Textvergleich nach Unicode-NFC und in V1 quelltreu einschließlich äußerer Leerzeichen;
- `city` enthält den vollständigen Ortsnamen aus der Quelle, auch wenn darin ein Komma vorkommt.

## V1-Repro-Gate

Reproduziert euren Excel-Import in einer leeren Datenbank und führt aus:

```bash
docker compose run --rm -e CONTRACT_VERSION=V1 kundinnen_app \
  node server/dist/cli.js
```

Nur Exit-Code `0` ist ein grünes V1-Gate. Erklärt V1 anschließend in der Begleit-Website als grün;
dort öffnet sich Akt 2.

---

# Akt 2 — Zielmodell und MongoDB

## Modellierungsauftrag

Bearbeitet zuerst die in der Begleit-Website angezeigten ERD-Trainingsfälle. Öffnet danach dort die
LetsMeet-Modellierungsstation, entwickelt ER-Diagramm und relationales Schema und registriert eure
vollständige Share-URL. Sichert dieselbe URL zusätzlich in eurer Projektdokumentation.

Berücksichtigt dabei:

- Transformation ins Relationenmodell und dritte Normalform; siehe
  [`normalization.md`](./normalization.md);
- priorisierte und ausdrücklich nicht gemochte Hobbys (`-100` bis `100`);
- Freundeslisten;
- ein direkt gespeichertes Profilbild sowie weitere hochgeladene oder verlinkte Fotos;
- Datenschutz: Datenarten, Rechtsgrundlage, Schutzbedarf und technische/organisatorische
  Maßnahmen;
- je Anwendungsfall eine beispielhafte SQL-Abfrage;
- physische Modelle und SQL-DDL sowohl für die aufgenommenen Quelldaten als auch für das
  PostgreSQL-Zielsystem;
- eigene Tests für Mengen, Eindeutigkeit, Referenzen und zentrale Transformationsregeln — der
  Kundinnen-Checker ergänzt diese, ersetzt sie aber nicht.

![Anwendungsfalldiagramm für die LetsMeet-Datenbank](./images/use-case.png)

## MongoDB-Quelle

Das Backup läuft bereits im Compose-Service `mongodb_for_lf8`. Die Sammlung `users` enthält
ergänzende Profildaten sowie gerichtete Likes und Nachrichten. Analysiert insbesondere
verschachtelte Datensätze, Referenzen, Mehrfachwerte und Widersprüche zur Excel-Quelle. Holt für
offene fachliche Konflikte eine Kundinnenentscheidung ein und dokumentiert die angewandte Regel.

## Migrationsvertrag V2

V2 ersetzt den V1-Spaltensatz und gilt kumulativ:

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
- Vergleichssemantik wie in V1; Zeitpunkte werden typisiert und auf die Sekunde genau verglichen.

Startet die Anzeige-App für Akt 2 neu:

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

## V2-Repro-Gate

Reproduziert Excel- und MongoDB-Import gemeinsam in einer leeren Datenbank:

```bash
docker compose run --rm -e CONTRACT_VERSION=V2 kundinnen_app \
  node server/dist/cli.js
```

Nur Exit-Code `0` ist ein grünes V2-Gate. Registriert vorher eure ERD-Share-URL und erklärt V2
dann in der Begleit-Website als grün. Danach folgt die nächste Anweisung.

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

Verbindlich ist nicht der Dateiname, sondern dass ein anderes Team eure Datenbank aus einer leeren
PostgreSQL-Instanz reproduzieren, eure Entscheidungen nachvollziehen und die Akt-Gates erneut
ausführen kann.

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

**Achtung:** Dieser Befehl löscht PostgreSQL, MongoDB, Check-Historie und Gate-Artefakte lokal. Nutzt
ihn nur, wenn ihr wirklich wieder bei einer leeren Infrastruktur beginnen möchtet. Euer Git-Stand
bleibt erhalten.

---

**Qualitätshinweis:** Die Lernumgebung wurde technisch, automatisiert und mit simulierten Personas
geprüft. Vor dem erstmaligen Einsatz in einer Lerngruppe ist weiterhin ein One-to-One-Pilot mit
2–3 Auszubildenden vorgesehen.
