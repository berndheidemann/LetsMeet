# Akt 3 — Nachlieferung integrieren und Ergebnis absichern

Grundlage: [Arbeitsweise, Befundnotiz und Artefakte](./projekt.md). Technische Befehle für beide
Betriebsarten: [Technischer Einstieg](./technik.md).

Dieser Akt ist erst nach Abschluss und Bestätigung von Akt 2 in der Begleit-Website verbindlich.
Die Materialdateien im Repository könnt ihr technisch schon vorher finden — das ist keine
Freigabe zur Bearbeitung. Beginnt erst, wenn die Begleit-Website diesen Akt öffnet.

## Material für die Nachlieferung

Verarbeitet zuerst die Basisdatei [`Lets_Meet_Hobbies.xml`](../Lets_Meet_Hobbies.xml) aus eurem
Projekt-Repository. Ladet danach in der Begleit-Website das Änderungspaket herunter und bewahrt
das Archiv unverändert auf; die Prüfsumme (SHA-256) steht dort neben dem Download.

## Datenvertrag für Akt 3 (V3)

Die fünf Datenbankansichten (Views) aus Akt 2 gelten weiter. Hinzu kommt genau eine Pflicht-View:

```sql
migration_rejections(source text, source_ref text, reason text)
```

### Was in die Views gehört

- XML-Hobbys tragen `source = 'xml'` und `priority = NULL`. Fachlich gleiche Person/Hobby-
  Zuordnungen erscheinen nur einmal.
- Jeder nicht übernommene Datensatz steht genau einmal mit eindeutiger Kombination aus `source`
  und `source_ref` sowie eurer kurzen, nichtleeren Begründung in `migration_rejections`.
- Für jeden Datensatz aus dem Änderungspaket ist sichtbar, ob er übernommen, verändert übernommen
  oder begründet abgelehnt wurde. Stilles Weglassen ist kein Ergebnis.
- Die fachlich vereinbarten Wertebereiche aus Akt 2 gelten weiter — insbesondere `priority` von
  `-100` bis `100`. Ein Datensatz außerhalb des vereinbarten Bereichs ist fehlerhaft.

### Was auch bei Fehlern und beim zweiten Import gilt

- Ein fehlerhafter Datensatz darf gültige Datensätze derselben Lieferung nicht verschwinden
  lassen. Die technische Strategie bleibt eure Entscheidung.
- Beim zweiten identischen Import des Änderungspakets bleiben alle sechs Views mengen- und
  wertgleich. Auch abgelehnte Datensätze vervielfachen sich nicht.

### Was der Prüfstand euch abnimmt

- Der Prüfstand vereinheitlicht Texte vor dem Vergleich auf Unicode-NFC; dadurch gelten zum
  Beispiel technisch unterschiedlich gespeicherte Akzente als gleich. Zeitpunkte vergleicht er als
  Zeitwerte. Die Zeilenreihenfolge ist ohne Bedeutung; eure Begründung dürft ihr frei formulieren.

## Abschluss von Akt 3 in zwei Prüfschritten

Führt die folgenden Befehle im Wurzelverzeichnis eures geklonten Projekt-Repositorys aus — dort,
wo `compose.yml` und der Ordner `scripts` liegen. Auf dem Schulserver nutzt ihr dafür das Terminal
eurer JupyterLab-Umgebung.

Startet zuerst die Kundinnen-App mit dem Datenvertrag für Akt 3 (V3) neu:

Variante A — Docker:

```bash
LETSMEET_CONTRACT_VERSION=V3 docker compose up -d --force-recreate kundinnen_app
```

Variante B — Schulserver:

```bash
letsmeet contract V3
```

Baut alle Daten in einer leeren Datenbank neu auf (siehe
[Technischer Einstieg → Neuaufbau](./technik.md#neuaufbau-vor-jedem-prüflauf-leeren-importieren-prüfen))
und importiert das Änderungspaket einmal. Speichert danach einen Vergleichszustand:

Variante A — Docker:

```bash
docker compose run --rm -e CONTRACT_VERSION=V3 kundinnen_app node server/dist/cli.js --snapshot-out /data/v3-snapshot.json
```

Variante B — Schulserver — verwendet dafür das Hilfsskript
[`scripts/check-schulserver.sh`](../scripts/check-schulserver.sh), weil `letsmeet check V3` allein
keine weiteren Argumente entgegennimmt:

```bash
bash scripts/check-schulserver.sh V3 --snapshot-out "$HOME/work/letsmeet/v3-snapshot.json"
```

Führt exakt denselben Importbefehl für das Änderungspaket ein zweites Mal aus und vergleicht
anschließend:

Variante A — Docker:

```bash
docker compose run --rm -e CONTRACT_VERSION=V3 kundinnen_app node server/dist/cli.js --snapshot-compare /data/v3-snapshot.json
```

Variante B — Schulserver:

```bash
bash scripts/check-schulserver.sh V3 --snapshot-compare "$HOME/work/letsmeet/v3-snapshot.json"
```

Nur Exit-Code 0 des zweiten Befehls schließt Akt 3 ab. Ein Prüflauf ohne gespeicherten
Vergleichszustand hilft bei der Fehlersuche, zählt aber nicht als Abschluss. Haltet ihr ein rotes
Ergebnis für falsch, zeigt der Lehrkraft Quelle, Datensatzreferenz und erwartetes Ergebnis.

Setzt danach in der Begleit-Website den Haken für Akt 3.
