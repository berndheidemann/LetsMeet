# Akt 2 — Zielmodell und MongoDB

Grundlage: [Arbeitsweise, Befundnotiz und Artefakte](./projekt.md). Technische Befehle für beide
Betriebsarten: [Technischer Einstieg](./technik.md).

## Ziel und Ausgangspunkt

Euer Excel-Import aus [Akt 1](./akt-1.md) ist der Ausgangspunkt. Jetzt erweitert ihr das Modell um
die weiteren Anforderungen dieses Akts und ergänzt den Import um MongoDB. Nutzt eure bisherigen
Skripte und die Befundnotiz weiter. Am Ende steht das vollständige Zielmodell mit integrierten
Excel-/MongoDB-Daten und dem Datenvertrag V2 unten.

Dabei können fachlich begründete Änderungen am bisherigen Modell nötig werden. Haltet fest, was
ihr ändert und warum. Das ist eine Weiterentwicklung eures Entwurfs — kein Auftrag, sämtliche
bisherigen Tabellen oder Skripte zu verwerfen. Eure Datenbank muss am Ende die Views des
Datenvertrags V2 liefern. Die View-Namen und ihre Spalten sind verbindlich; die Namen eurer
internen Tabellen müssen nicht genauso lauten.

## Vorbereitung: vier Trainingsfälle

Bearbeitet zuerst die folgenden vier Trainingsfälle im
[ERD-Katalog](https://erd.heidelab.de/), bevor ihr an der
LetsMeet-Modellierungsstation weiterarbeitet:

1. Bücher & Autoren — eine Viele-zu-viele-Beziehung sauber ins Tabellenschema überführen.
2. Kochbuch: Rezepte & Zutaten — ein Attribut modellieren, das zur Verbindung gehört.
3. Mitarbeiter & Vorgesetzte — einen Selbstbezug lesen und ableiten.
4. Personen & Nachrichten — Absender und Empfänger als getrennte Rollen modellieren.

Normalisierung und „gute Tabellen" sind fachliche Hilfen für den Modellierungsauftrag:
[`normalization.md`](../normalization.md) (Transformation ins Relationenmodell und dritte
Normalform) und [`gute-tabellen.md`](../gute-tabellen.md) (wenn ihr noch kein Gefühl dafür habt,
woran man eine unaufgeräumte Tabelle merkt — dieselben Daten einmal gewachsen und einmal
aufgeräumt, ohne Regelwerk).

Das [Zugriffsnotebook](../notebooks/00-zugriff.ipynb) hilft euch, die Datenbanken zu erreichen
und erste Daten anzusehen. Bei fehlenden Grundlagen könnt ihr die Lehrkraft ansprechen.
Für euren eigenen Code gilt weiterhin: Ihr müsst ihn erklären können.

## Arbeitsauftrag

Öffnet die [LetsMeet-Modellierungsstation](https://station.heidelab.de/letsmeet-erd/), entwickelt
ER-Diagramm und relationales Schema und registriert in der Begleit-Website die vollständige
Freigabe-URL (Share-URL) eures Modells.
Sichert dieselbe URL zusätzlich in eurer Befundnotiz.

Berücksichtigt dabei:

- Transformiert das ER-Diagramm ins Relationenmodell und bringt das relationale Schema in die
  dritte Normalform; nutzt dazu die oben verlinkten Hilfen.
- Entwickelt das Zielmodell einschließlich der folgenden fachlichen Anforderungen:
  - priorisierte und ausdrücklich nicht gemochte Hobbys (`-100` bis `100`). Der Wertebereich ist
    fachlich mit der Kundin vereinbart; die aktuelle Datenlieferung schöpft ihn nicht aus.
    Modelliert den vereinbarten Bereich, nicht den in der Stichprobe vorgefundenen;
  - getrennt von der Priorität des eigenen Hobbys: nach welchem Hobby jemand bei anderen sucht,
    wie im Szenario der Modellierungsstation beschrieben;
  - Freundeslisten;
  - ein direkt gespeichertes Profilbild sowie weitere hochgeladene oder verlinkte Fotos;
  - je Anwendungsfall eine beispielhafte SQL-Abfrage.
- ERD und relationales Schema erstellen; Trainingsfälle und Projektmodell klar auseinanderhalten.
- MongoDB-Quelle analysieren, Konflikte klären und Import erweitern (siehe unten).
- Physische Modelle und die zugehörige DDL sowohl für die aufgenommenen Quelldaten als auch für
  das PostgreSQL-Zielsystem erstellen.
- Eigene Tests für Mengen, Eindeutigkeit, Referenzen und zentrale Transformationsregeln — der
  Kundinnen-Checker ergänzt diese, ersetzt sie aber nicht.
- Befundnotiz fortführen; Datenschutz bleibt die bereits vereinbarte kurze Reflexion (siehe
  [projekt.md](./projekt.md#eure-befundnotiz)).

![Anwendungsfalldiagramm für die LetsMeet-Datenbank](../images/use-case.png)

## MongoDB-Quelle

Das Backup ist in eurer MongoDB bereitgestellt — unter Docker im Service `mongodb_for_lf8`,
auf dem Schulserver nach `letsmeet up`. Die Sammlung `users` enthält
ergänzende Profildaten sowie gerichtete Likes und Nachrichten. Analysiert insbesondere
verschachtelte Datensätze, Referenzen, Mehrfachwerte und Widersprüche zur Excel-Quelle. Holt für
offene fachliche Konflikte eine Kundinnenentscheidung ein und haltet die angewandte Regel in eurer
Befundnotiz fest.

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
- `interest_code` und `gender` übernehmen die einzelnen Werte aus der Quelle unverändert.
  Übersetzt sie in den Views nicht in ausgeschriebene Bezeichnungen oder selbst gewählte Codes.
  Die Spaltenüberschriften der Excel-Datei sind Beschriftungen, keine Wertespezifikation — welche
  Werte tatsächlich vorkommen, ergibt eure Quellenanalyse.
- Likes und Nachrichten sind gerichtet: Absender beziehungsweise auslösende Person stehen links.
- Bei widersprüchlichen Angaben zur selben Person gilt die eingeholte und dokumentierte
  Kundinnenentscheidung. Das betrifft nicht nur Kontaktdaten, sondern jedes Feld, in dem sich die
  Quellen widersprechen.
- Die E-Mail-Adresse verbindet die beiden Quellen. Sie ist quellenübergreifend eindeutig, wobei
  Groß- und Kleinschreibung keinen Unterschied macht: `Martin.Forster@web.ork` und
  `martin.forster@web.ork` bezeichnen dieselbe Person. In den Views erscheint die Schreibweise aus
  der Excel-Quelle.
- Textvergleich wie in Akt 1; Zeitpunkte werden als Zeitwerte und auf die Sekunde genau verglichen.

**Zu den Interessen:** `interest_code` bezeichnet einen Interessenwert aus der Quelle, keinen
Code, den ihr neu erfinden sollt. Mehrere Interessen einer Person erscheinen in der View als
mehrere Zeilen. Übernehmt die einzelnen Quellwerte, statt sie in selbst gewählte Codes oder
ausgeschriebene Bezeichnungen umzuwandeln. Eine interne Nachschlagetabelle ist damit nicht
grundsätzlich verboten; entscheidend ist, welche Werte eure View nach außen liefert.

Startet die Anzeige-App für Akt 2 neu:

Variante A — Docker:

```bash
LETSMEET_CONTRACT_VERSION=V2 docker compose up -d --force-recreate kundinnen_app
```

Variante B — Schulserver:

```bash
letsmeet contract V2
```

## Was die Prüfungen bedeuten

**Akt und Werkzeugphase sind nicht dasselbe.** Akt 2 ist der zweite Abschnitt des Projekts. In der
ERD-Werkbank bearbeitet ihr innerhalb dieses Akts zwei Phasen: das ER-Diagramm und seine Ableitung
ins relationale Schema. Beides gehört zum Modellierungsauftrag.

Die ERD-Werkbank gibt Rückmeldung zu eurem Modell und seiner Ableitung. Der Kundinnen-Checker
prüft dagegen die Datenbank-Views und ihre Inhalte. Er liest nicht euer ER-Diagramm. Ein
erfolgreicher Datenbankcheck ersetzt deshalb nicht die geforderten Modellierungsarbeiten.

Die Begleit-Website merkt sich nur eure Bestätigungen und den Modelllink. Ein gespeicherter Link
bedeutet nicht, dass euer Modell fachlich geprüft wurde.

Die Werkbank erkennt bestimmte Modellvarianten, nicht jede fachlich mögliche Lösung. Wenn ihr
einen Befund für unzutreffend haltet, zeigt der Lehrkraft euer Modell, die konkrete Meldung und
eure fachliche Begründung. Ändert euren Entwurf nicht allein deshalb, weil eine andere Darstellung
leichter ein grünes Ergebnis erzeugt; klärt zuerst, ob ein Modellfehler oder eine Grenze des
Werkzeugs vorliegt.

## Abschluss von Akt 2: Gemeinsamen Neuaufbau prüfen

Leert die Datenbank wie im [technischen Einstieg](./technik.md#neuaufbau-vor-jedem-prüflauf-leeren-importieren-prüfen)
beschrieben, baut Excel- und MongoDB-Import gemeinsam neu auf und führt danach diesen Prüfbefehl
im Terminal aus:

Variante A — Docker:

```bash
docker compose run --rm -e CONTRACT_VERSION=V2 kundinnen_app node server/dist/cli.js
```

Variante B — Schulserver:

```bash
letsmeet check V2
```

Endet der Befehl mit Exit-Code `0`, ist die Abschlussprüfung für Akt 2 bestanden. Registriert
vorher eure ERD-Share-URL und setzt anschließend in der Begleit-Website den Haken für Akt 2.
Danach folgt die nächste Anweisung.
