# Technischer Einstieg

Die Arbeitsumgebung lässt sich auf zwei Wegen starten. **Eure Lehrkraft sagt euch, welcher für
euch gilt.** An den Aufgaben ändert das nichts: Ports, Zugangsdaten und alle Inhalte sind in
beiden Varianten gleich. Wo sich Befehle unterscheiden, stehen sie im Folgenden nebeneinander.

## Start und Stopp

### Variante A — lokal mit Docker

```bash
docker compose up -d
```

Alle `docker compose`-Befehle laufen im Wurzelverzeichnis eures geklonten Projekts — dort, wo
`compose.yml` liegt.

### Variante B — auf dem Schulserver, ohne Docker

Im Terminal eurer JupyterLab-Umgebung:

```bash
letsmeet up
```

Damit laufen dieselben drei Dienste als gewöhnliche Programme in eurem eigenen Arbeitsbereich.
`letsmeet status` zeigt, was gerade läuft; `letsmeet down` stoppt alles wieder, ohne eure Daten
zu löschen. `letsmeet zugang` zeigt euch jederzeit alle Verbindungsdaten.

Als Einstieg im Browser liegt `notebooks/00-zugriff.ipynb` bereit: Es prüft, ob die Dienste
laufen, und stellt je eine Verbindung zu MongoDB und PostgreSQL her. Mehr macht es nicht — die
Analyse ist eure Arbeit.

## In beiden Varianten erreichbar

- PostgreSQL: `localhost:5432`, Datenbank `lf8_lets_meet_db`
- MongoDB: `localhost:27017`, Datenbank `LetsMeet`
- Kundinnen-App und Prüfstand: [http://localhost:3611](http://localhost:3611) — auf dem
  Schulserver über die Adresse, die euch `letsmeet up` anzeigt

PostgreSQL-Zugang: Benutzer `user`, Passwort `secret`.

## Datenverträge umstellen (V1/V2/V3)

Die Kürzel V1, V2 und V3 bezeichnen die technischen Datenverträge für Akt 1, Akt 2 und Akt 3: die
Datenbankansichten, die ihr je Akt verbindlich bereitstellt (siehe die jeweilige Akt-Datei). In
Befehlen müsst ihr diese Kürzel genau so verwenden. Die Kundinnen-App startet mit V1. Wenn ein
späterer Akt den nächsten Datenvertrag freigibt, startet ihr nur die Kundinnen-App mit der dort
genannten Version neu. Beispiel für Akt 2 mit V2:

**Variante A — Docker:**

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

PowerShell:

```powershell
$env:LETSMEET_CONTRACT_VERSION="V2"
docker compose up -d --force-recreate kundinnen_app
```

**Variante B — Schulserver:**

```bash
letsmeet contract V2
```

## Neuaufbau vor jedem Prüflauf: leeren, importieren, prüfen

Für den Abschluss eines Akts zählt nicht der Zustand eurer Datenbank, sondern dass eure Skripte
ihn aus dem Nichts erzeugen können. Der Ablauf ist deshalb immer derselbe.

**1. Leeren** — alle Tabellen und Views im Schema `public` löschen:

Variante A — Docker:

```bash
docker compose exec postgres_for_lf8_starter psql -U user -d lf8_lets_meet_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

Variante B — Schulserver:

```bash
letsmeet leeren
```

**2. Importieren** — eure eigenen Importskripte ausführen, so wie ein anderes Team es auch tun
würde.

**3. Prüfen** — der Befehl unterscheidet sich je Akt nur in der Vertragsversion; die genauen
Befehle stehen in der jeweiligen Akt-Datei ([Akt 1](./akt-1.md), [Akt 2](./akt-2.md),
[Akt 3](./akt-3.md)).

Verwendet die vollständigen Befehle aus eurem aktuellen Akt. Für Akt 1 und Akt 2 schließt ein
Exit-Code `0` nach dem frischen Import die Datenbankprüfung ab. In Akt 3 gehört zusätzlich ein
zweiter Import mit Vergleich zum Abschluss. Ein einzelner erfolgreicher Prüflauf genügt dort
nicht; folgt dem Ablauf, sobald dieser Akt freigegeben ist.

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

Auf dem Schulserver laufen grafische Werkzeuge wie DBeaver oder Compass nicht. Die
Verbindungsdaten sind dieselben; ihr erreicht die Datenbanken im Terminal mit `letsmeet psql` und
`letsmeet mongosh` oder aus einem Notebook heraus. `letsmeet zugang` zeigt euch diese Angaben
jederzeit an.

Ein fertiges Startnotebook liegt unter `notebooks/00-zugriff.ipynb` — beide Verbindungen als
lauffähige Zellen, dazu SQL direkt in der Zelle über `%sql`. Es ist auf den Schulserver
zugeschnitten; unter Docker tauscht ihr im Verbindungsstring `pg8000` gegen euren Treiber.
Daneben liegt `notebooks/01-erd-zu-tabelle.ipynb`, die Aufwärmrunde vor Akt 1 (siehe
[Vorbereitung in projekt.md](./projekt.md#vor-akt-1-eine-aufwärmrunde)).

**Eine Abweichung, die ihr sonst suchen müsstet:** Der PostgreSQL-Treiber heißt auf dem
Schulserver `pg8000`, nicht `psycopg2`. `pg8000` ist dort bereits installiert, `psycopg2` nicht —
nehmt `pg8000`. Ausgewählt wird er über den Verbindungsstring:

```python
# PostgreSQL
from sqlalchemy import create_engine
engine = create_engine("postgresql+pg8000://user:secret@127.0.0.1:5432/lf8_lets_meet_db")

# MongoDB
from pymongo import MongoClient
db = MongoClient("mongodb://127.0.0.1:27017/")["LetsMeet"]
```

Wie ihr von dort weiterarbeitet — `pandas.read_sql`, `%sql`-Magic, direkte Abfragen —, entscheidet
ihr selbst. Bei Variante A gilt der übliche Weg mit `psycopg2`.

Der Verlauf eurer Prüfläufe liegt im Volume `lf8_lets_meet_check_history` und bleibt beim
Container-Neustart erhalten; auf dem Schulserver liegt er in eurem Arbeitsbereich und übersteht
`letsmeet down` ebenfalls.

## Alles zurücksetzen

Variante A — Docker:

```bash
docker compose down -v
```

Das löscht eure lokalen PostgreSQL- und MongoDB-Daten sowie den Verlauf der Prüfläufe vollständig.

Variante B — Schulserver:

```bash
letsmeet reset-all
```

**Achtung:** `letsmeet reset-all` setzt MongoDB und den Prüfverlauf zurück, **aber nicht eure
PostgreSQL-Daten**. Wollt ihr auch die Tabellen und Views in PostgreSQL löschen, startet bei
Bedarf zuerst mit `letsmeet up`, führt dann `letsmeet leeren` aus und erst danach
`letsmeet reset-all`. Die Reihenfolge ist wichtig: `reset-all` stoppt die Dienste;
`letsmeet leeren` braucht eine laufende PostgreSQL-Datenbank. Euer Git-Stand bleibt in
beiden Varianten erhalten. Für den normalen Neuaufbau vor einem Prüflauf braucht ihr `reset-all`
**nicht** — dafür genügt das Leeren des Schemas aus dem Abschnitt oben. Gegen einen belegten Port
hilft es ebenfalls nicht; das löst der Abschnitt [Wenn etwas nicht funktioniert](#wenn-etwas-nicht-funktioniert).

Nicht zu verwechseln mit dem Knopf „Lokalen Stand zurücksetzen" auf der Begleit-Website: Der
löscht nur eure dort gesetzten Haken im Browser und rührt keine Datenbank an.

## Wenn etwas nicht funktioniert

### `no configuration file provided` (Variante A)

Ihr seid im falschen Verzeichnis. Alle `docker compose`-Befehle laufen dort, wo `compose.yml`
liegt — im Wurzelverzeichnis eures geklonten Projekts.

### `port is already allocated` oder `address already in use` (Variante A)

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

### Auf dem Schulserver ist nach der Anmeldung nichts erreichbar (Variante B)

Eure Dienste laufen nur, solange eure Arbeitsumgebung läuft. Nach einer längeren Pause oder einer
Neuanmeldung startet ihr sie mit `letsmeet up` wieder — **eure Daten bleiben dabei erhalten**.
`letsmeet status` zeigt jederzeit, was gerade läuft.

Meldet die Shell `letsmeet: command not found`, läuft eure Arbeitsumgebung noch aus einer älteren
Sitzung. Meldet euch ab und startet den Server neu; danach ist das Kommando da.

Startet die Kundinnen-App nicht, steht der Grund in `~/work/letsmeet/run/app.log`.

### Das Werkzeug zeigt alles grün, der Prüfstand meldet `Keine View migration_users`

Ihr seid vermutlich auf dem alten Port verbunden und arbeitet in der bereits laufenden Datenbank
eures Rechners. Eure Tabellen und Views entstehen dann dort statt im Container.
