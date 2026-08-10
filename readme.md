# Lernsituation: LetsMeet-Datenmigration

Die **Let’s Meet GmbH** wechselt nach einer schwierigen Trennung den IT-Dienstleister. Statt einer
laufenden Datenbank liegen nur schrittweise freigegebene Datenstände vor. Euer
Team rekonstruiert daraus eine PostgreSQL-Datenbank, die eine
Anzeige-App der Kundin (im Folgenden: Kundinnen-App) wieder versorgen kann.

![Ausschnitt aus „Tea with friends, and one must wear one's finest hat!“ (Public Domain)](./images/tea-with-friends.png)

## Euer Arbeitsauftrag

Ihr arbeitet in drei Akten. Akt 1 und Akt 2 sind unten vollständig beschrieben; die Begleit-Website
gibt Akt 2 erst frei, wenn ihr Akt 1 abgeschlossen habt. Für jeden aktuell
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

Alle `docker compose`-Befehle laufen im Wurzelverzeichnis eures geklonten Projekts — dort, wo
`compose.yml` liegt. Danach sind erreichbar:

- PostgreSQL: `localhost:5432`, Datenbank `lf8_lets_meet_db`
- MongoDB: `localhost:27017`, Datenbank `LetsMeet`
- Kundinnen-App und Prüfstand: [http://localhost:3611](http://localhost:3611)

PostgreSQL-Zugang: Benutzer `user`, Passwort `secret`.

Startet etwas nicht, hilft der Abschnitt [Wenn etwas nicht funktioniert](#wenn-etwas-nicht-funktioniert)
am Ende dieser Datei.

Die Kürzel V1, V2 und V3 bezeichnen die technischen Datenverträge für Akt 1, Akt 2 und Akt 3: die
Datenbankansichten, die ihr je Akt verbindlich bereitstellt (ausformuliert unten unter „Datenvertrag
für Akt 1“.
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

---

# Akt 1 — Erste Daten aus Excel bis zur Kundinnen-App bringen

## Ausgangslage

Quelle ist [`Lets Meet DB Dump.xlsx`](./Lets%20Meet%20DB%20Dump.xlsx). Darin stehen Name,
Adresse, Telefon, fünf priorisierte Hobbys, E-Mail-Adresse, Geschlecht, Interessen und
Geburtsdatum in teilweise zusammengesetzten Feldern.

Für Akt 1 ist die Excel-Datei eure einzige Quelle. Die ebenfalls im Repository liegende Datei
`Lets_Meet_Hobbies.xml` gehört zu einer späteren Nachlieferung und bleibt vorerst unberührt; die
MongoDB kommt in Akt 2 dazu.

## Auftrag

1. Profiliert die Quelle und haltet auffällige Formate, Mehrfachwerte und offene Fragen fest.
2. Erstellt das minimale physische Modell — die Tabellen, die ihr für die geforderte View wirklich
   braucht, mit Spalten, Datentypen und Schlüsseln — und einen Import aus einer **leeren** Datenbank.
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
- vor dem Textvergleich vereinheitlicht der Prüfstand Texte automatisch auf Unicode-NFC — dafür
  müsst ihr nichts tun; in Akt 1 bleiben die Inhalte einschließlich äußerer Leerzeichen ansonsten
  genau wie in der Quelle;
- in den zusammengesetzten Spalten `Nachname, Vorname` und `Straße Nr, PLZ Ort` trennt „Komma +
  genau ein Leerzeichen“; jedes weitere Leerzeichen gehört zum Wert. Aus `Stanislav , Petrov` wird
  der Nachname `Stanislav ` — mit Leerzeichen. Andere Spalten haben andere Trennzeichen, die ihr
  beim Profilieren selbst bestimmt;
- die Adresszelle besteht aus **genau drei komma-getrennten Teilen** in dieser Reihenfolge: Straße
  mit Hausnummer, Postleitzahl, Ort. Der Ort ist alles nach dem zweiten Komma — ein Komma im
  Ortsnamen gehört also zum Ort: `Demmin, Hansestadt`.

## Abschluss von Akt 1: Neuaufbau prüfen

Für den Abschluss zählt nicht der Zustand eurer Datenbank, sondern dass eure Skripte ihn aus dem
Nichts erzeugen können. Der Ablauf ist deshalb immer derselbe: **leeren, importieren, prüfen.**

**1. Leeren** — alle Tabellen und Views im Schema `public` löschen:

```bash
docker compose exec postgres_for_lf8_starter psql -U user -d lf8_lets_meet_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

**2. Importieren** — eure eigenen Importskripte ausführen, so wie ein anderes Team es auch tun
würde.

**3. Prüfen:**

```bash
docker compose run --rm -e CONTRACT_VERSION=V1 kundinnen_app node server/dist/cli.js
```

Endet der Befehl mit Exit-Code `0` — also ohne Fehler —, ist die Abschlussprüfung für Akt 1
bestanden. Setzt danach in der Begleit-Website den Haken für Akt 1; dort öffnet sich Akt 2.

---

# Erwartete Repository-Artefakte

Diese Struktur gilt ab Akt 1. Eine mögliche Form:

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

Verbindlich ist nicht der Dateiname, sondern dass ein anderes Team eure Entscheidungen
nachvollziehen und die Prüfbefehle nach einem eigenen Neuaufbau erneut ausführen kann.

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
- priorisierte und ausdrücklich nicht gemochte Hobbys (`-100` bis `100`). Der Wertebereich ist
  fachlich mit der Kundin vereinbart; die aktuelle Datenlieferung schöpft ihn nicht aus. Modelliert
  den vereinbarten Bereich, nicht den in der Stichprobe vorgefundenen;
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
- `interest_code` und `gender` übernehmen den Wert aus der Quelle unverändert. Übersetzt sie nicht
  in ausgeschriebene Bezeichnungen und legt keine eigene Codetabelle an. Die Spaltenüberschriften
  der Excel-Datei sind Beschriftungen, keine Wertespezifikation — welche Werte tatsächlich
  vorkommen, ergibt eure Quellenanalyse.
- Likes und Nachrichten sind gerichtet: Absender beziehungsweise auslösende Person stehen links.
- Bei widersprüchlichen Angaben zur selben Person gilt die eingeholte und dokumentierte
  Kundinnenentscheidung. Das betrifft nicht nur Kontaktdaten, sondern jedes Feld, in dem sich die
  Quellen widersprechen.
- Die E-Mail-Adresse verbindet die beiden Quellen. Sie ist quellenübergreifend eindeutig, wobei
  Groß- und Kleinschreibung keinen Unterschied macht: `Martin.Forster@web.ork` und
  `martin.forster@web.ork` bezeichnen dieselbe Person. In den Views erscheint die Schreibweise aus
  der Excel-Quelle.
- Textvergleich wie in Akt 1; Zeitpunkte werden als Zeitwerte und auf die Sekunde genau verglichen.

Startet die Anzeige-App für Akt 2 neu:

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

## Abschluss von Akt 2: Gemeinsamen Neuaufbau prüfen

Leert die Datenbank wie in Akt 1 beschrieben, baut Excel- und MongoDB-Import gemeinsam neu auf und
führt danach diesen Prüfbefehl im Terminal aus:

```bash
docker compose run --rm -e CONTRACT_VERSION=V2 kundinnen_app node server/dist/cli.js
```

Endet der Befehl mit Exit-Code `0`, ist die Abschlussprüfung für Akt 2 bestanden. Registriert
vorher eure ERD-Share-URL und setzt anschließend in der Begleit-Website den Haken für Akt 2.
Danach folgt die nächste Anweisung.

---

# Akt 3 — Fortsetzung

Beginnt Akt 3 erst, wenn euch der nächste Auftrag angezeigt wird. Bis dahin sind ausschließlich
Akt 1 und Akt 2 verbindlich.

---

# Werkzeuge und Betrieb

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

Der Verlauf eurer Prüfläufe liegt im Volume `lf8_lets_meet_check_history` und bleibt beim
Container-Neustart erhalten.

## Alles zurücksetzen, auch MongoDB und Prüfverlauf

```bash
docker compose down -v
```

**Achtung:** Dieser Befehl löscht eure lokalen PostgreSQL- und MongoDB-Daten sowie den Verlauf der
Prüfläufe. Euer Git-Stand bleibt erhalten. Für den normalen Neuaufbau vor einem Prüflauf braucht
ihr ihn **nicht** — dafür genügt das Leeren des Schemas aus „Abschluss von Akt 1". Gegen einen
belegten Port hilft er ebenfalls nicht; das löst der Abschnitt
[Wenn etwas nicht funktioniert](#wenn-etwas-nicht-funktioniert).

Nicht zu verwechseln mit dem Knopf „Lokalen Stand zurücksetzen" auf der Begleit-Website: Der
löscht nur eure dort gesetzten Haken im Browser und rührt keine Datenbank an.

---

# Wenn etwas nicht funktioniert

## `no configuration file provided`

Ihr seid im falschen Verzeichnis. Alle `docker compose`-Befehle laufen dort, wo `compose.yml`
liegt — im Wurzelverzeichnis eures geklonten Projekts.

## `port is already allocated` oder `address already in use`

Auf eurem Rechner läuft bereits ein anderes Programm auf Port `5432` (PostgreSQL) oder `27017`
(MongoDB). Ihr müsst nichts deinstallieren: Legt neben `compose.yml` eine Datei `.env` an und
tragt dort einen freien Port ein. Docker Compose liest sie automatisch.

```bash
LETSMEET_PG_PORT=55432
LETSMEET_MONGO_PORT=57017
```

Prüft das Ergebnis vor dem Start mit `docker compose config` — dort muss der neue Port stehen und
der alte verschwunden sein. Die `.env` gilt nur für euren Rechner; nehmt sie nicht mit ins
Git-Repository, sonst erben eure Teamkolleginnen und -kollegen fremde Ports.

Ihr verbindet euch danach von außen über den neuen Port, also `localhost:55432` statt
`localhost:5432` — auch in DBeaver, SQLTools oder Compass. Innerhalb des Docker-Netzes bleibt
alles unverändert; der Prüfstand ist von der Änderung nicht betroffen.

Der Konflikt entsteht durch ein anderes Programm, nicht durch eure Daten — `docker compose down -v`
hilft dagegen nicht.

## Das Werkzeug zeigt alles grün, der Prüfstand meldet `Keine View migration_users`

Ihr seid vermutlich auf dem alten Port verbunden und arbeitet in der bereits laufenden Datenbank
eures Rechners. Eure Tabellen und Views entstehen dann dort statt im Container.
