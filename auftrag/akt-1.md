# Akt 1 — Erste Daten aus Excel bis zur Kundinnen-App bringen

Grundlage: [Arbeitsweise, Befundnotiz und Artefakte](./projekt.md). Technische Befehle für beide
Betriebsarten: [Technischer Einstieg](./technik.md).

## Ausgangslage

Quelle ist [`Lets Meet DB Dump.xlsx`](../Lets%20Meet%20DB%20Dump.xlsx). Darin stehen Name,
Adresse, Telefon, fünf priorisierte Hobbys, E-Mail-Adresse, Geschlecht, Interessen und
Geburtsdatum in teilweise zusammengesetzten Feldern.

Für Akt 1 ist die Excel-Datei eure einzige Quelle. Weitere Quellen kommen erst in einem späteren
Akt hinzu.

## Vorbereitung

Bearbeitet vor dem ersten Import die [SQL-Aufwärmrunde an der Fahrradwerkstatt](./projekt.md#vor-akt-1-eine-aufwärmrunde).
Sie gehört für alle zum Einstieg. Startet anschließend eure Arbeitsumgebung wie im
[technischen Einstieg](./technik.md#start-und-stopp) beschrieben.

## Auftrag

**Was ihr jetzt modelliert — und was noch nicht:** Erstellt zunächst nur das physische Modell
für die View `migration_users` dieses Akts: die dafür benötigten Tabellen mit Spalten, Datentypen
und Schlüsseln. Das vollständige LetsMeet-Zielmodell mit allen Beziehungen und Erweiterungswünschen
ist erst in Akt 2 dran.

Das kleine Modell ist kein Wegwerfprodukt. Es soll zusammen mit eurem Import bereits funktionieren
und bildet die Grundlage für die Erweiterung. Was ihr bei der Quellenanalyse entdeckt, aber noch
nicht verarbeitet, haltet ihr in eurer Befundnotiz fest.

1. Profiliert die Quelle und haltet auffällige Formate, Mehrfachwerte und offene Fragen in eurer
   Befundnotiz fest.
2. Erstellt das minimale physische Modell — die Tabellen, die ihr für die geforderte View wirklich
   braucht, mit Spalten, Datentypen und Schlüsseln — und einen Import aus einer **leeren**
   Datenbank. Die Wahl der Programmiersprache und des Werkzeugs für den Import liegt bei euch.
3. Stellt die folgende View bereit. Eure internen Tabellen und Joins bleiben eure Entscheidung.
4. Öffnet die Kundinnen-App und untersucht sichtbare Folgen eurer Importentscheidungen.
5. Schreibt eigene SQL-Abfragen oder automatisierte Tests für eure zentralen Importannahmen.
6. Haltet in der Befundnotiz fest, wo euer Import an Grenzen stößt.

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
  müsst ihr nichts tun. Ansonsten übernimmt Akt 1 die Inhalte unverändert, einschließlich äußerer
  Leerzeichen: Daten zu bereinigen ist ein eigener Arbeitsschritt und nicht Teil des Imports;
- in den zusammengesetzten Spalten `Nachname, Vorname` und `Straße Nr, PLZ Ort` trennt „Komma +
  genau ein Leerzeichen"; jedes weitere Leerzeichen gehört zum Wert. Aus `Stanislav , Petrov` wird
  der Nachname `Stanislav ` — mit Leerzeichen. Andere Spalten haben andere Trennzeichen, die ihr
  beim Profilieren selbst bestimmt;
- die Adresszelle besteht aus **genau drei Teilen** in dieser Reihenfolge: Straße mit Hausnummer,
  Postleitzahl, Ort. Der Ort ist alles nach dem zweiten Komma — ein Komma im Ortsnamen gehört also
  zum Ort: `Demmin, Hansestadt`.

## Abschluss von Akt 1: Neuaufbau prüfen

Leeren, importieren, prüfen — der genaue Ablauf für beide Betriebsarten steht unter
[Technischer Einstieg → Neuaufbau vor jedem Prüflauf](./technik.md#neuaufbau-vor-jedem-prüflauf-leeren-importieren-prüfen).
Für Akt 1 lautet der Prüfbefehl:

Variante A — Docker:

```bash
docker compose run --rm -e CONTRACT_VERSION=V1 kundinnen_app node server/dist/cli.js
```

Variante B — Schulserver:

```bash
letsmeet check V1
```

Endet der Befehl mit Exit-Code `0` — also ohne Fehler —, ist die Abschlussprüfung für Akt 1
bestanden. Setzt danach in der Begleit-Website den Haken für Akt 1; dort öffnet sich Akt 2.
