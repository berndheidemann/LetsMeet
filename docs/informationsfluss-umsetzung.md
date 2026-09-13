# Informationsfluss für den nächsten LetsMeet-Durchlauf

## Freigegebener Umfang

Eine kurze Start-README und vollständige Aufträge je Akt ersetzen die bisher wechselnde
Verteilung zwischen README und Begleitwebsite. Die Website zeigt die Akt-Inhalte aus einer
gemeinsamen Quelle; die Markdown-Dateien bleiben auch direkt im Material-Repository lesbar.

Die bestehenden Lernziele, Datenverträge, Artefakte und Abschlussbedingungen bleiben erhalten.
Präzisiert werden das Minimalmodell in Akt 1, die Weiterentwicklung in Akt 2, der reproduzierbare
Neuaufbau, die verschiedenen Prüfungen und die Interessenwerte. Datenschutz bleibt eine kurze
Reflexion in der Befundnotiz. Ein MongoDB-Grundlagenkurs und konkrete Checkeränderungen gehören
nicht zu diesem Paket.

## Zuordnung der bisherigen Inhalte

| Bisheriger Ort | Neuer Ort |
|---|---|
| README: Geschichte, Einstieg und Materiallinks | `readme.md`, kurz als Wegweiser |
| README: Arbeitsweise und allgemeine Artefakte | `auftrag/projekt.md` |
| README: Aufwärmrunde vor Akt 1 | `auftrag/projekt.md`, aus Akt 1 direkt verlinkt |
| README: Akt-1-Auftrag und V1-Vertrag | `auftrag/akt-1.md` |
| README: Modellierung, MongoDB und V2-Vertrag | `auftrag/akt-2.md` |
| Website: vier konkrete ERD-Trainings | `auftrag/akt-2.md` |
| Website: Akt-3-Auftrag, V3-Regeln und Prüfablauf | `auftrag/akt-3.md` |
| README: Befundnotiz und Datenschutzfrage | `auftrag/projekt.md`, aktübergreifend verlinkt |
| README: Betrieb, Verbindungen und Fehlerhilfe | `auftrag/technik.md` |
| Website: Modelllink, Fortschrittshaken und Transferdownload | bleiben interaktive Website-Elemente |

`gute-tabellen.md`, `normalization.md`, die Quelldateien und die Notebooks bleiben inhaltlich
unverändert. Die getrennte Hobby-Suchpräferenz wurde im Akt-2-Auftrag ausdrücklich sichtbar
gemacht; sie stammt aus dem bestehenden Szenario der ERD-Station und ist keine neue Anforderung.

## Gemeinsame Quelle und Veröffentlichung

Autoritative Textquelle ist `auftrag/` in diesem Repository. Das getrennte Website-Repository
`berndheidemann/letsmeet-begleit-website` übernimmt daraus einen **generierten** Snapshot mit
Quellcommit und Dateihashes. Der dokumentierte Sync-Befehl dort lautet:

```bash
node scripts/sync-content.mjs --source /pfad/zum/LetsMeet-repo
node scripts/check-content.mjs --source /pfad/zum/LetsMeet-repo
```

Die Website benötigt beim normalen Build weder ein Nachbarrepository noch einen Netzwerkzugriff
auf die Auftragsquelle. Änderungen werden im Material-Repository vorgenommen, committet und
anschließend ausdrücklich in das Website-Repository synchronisiert. Generierte Dateien nicht
von Hand bearbeiten. Für die Veröffentlichung muss der Snapshot auf den sauberen, gepushten
Materialstand zeigen; ein Dirty-Snapshot ist nur ein Entwicklungsstand.

Die neue Fassung wird zunächst auf `next/informationsfluss` in beiden Repositories gesichert.
Sie wird **nicht** in die laufende Kursfassung übernommen und die Begleitwebsite wird **nicht**
neu deployt. Erst nach Ende beziehungsweise ausdrücklicher Freigabe des laufenden Durchlaufs
werden die zusammengehörenden Stände übernommen und veröffentlicht. Die Start-README dieser
vorbereiteten Fassung beschreibt bereits die dann gemeinsam zu veröffentlichende Website;
sie ist deshalb nicht als isolierter README-Hotfix für den aktuellen Kurs gedacht.

Akt 3 bleibt in der Website an seine bisherige Freigabe gebunden. Die Materialdateien im
Repository sind technisch auffindbar; wie bisher ist dies didaktische Reihenfolge und kein
Zugriffsschutz. Der Schülertext unterscheidet deshalb Auffindbarkeit und Bearbeitungsfreigabe.

## Schulserver-Prüfaufruf für Akt 3

Der vorhandene `letsmeet check V3`-Wrapper reicht Zusatzargumente nicht an die Node-CLI weiter.
`scripts/check-schulserver.sh` schließt ausschließlich diese Aufruflücke: gleiche vorhandene
CLI und Betriebsumgebung, zusätzliche Argumente und Exitcode unverändert durchgereicht.
Es installiert nichts, verändert keine Dienste und setzt keine Daten zurück.

Die Anleitung verwendet einen absoluten Snapshotpfad, weil der Helfer wie der bestehende Wrapper
ins installierte App-Verzeichnis wechselt. Aufgerufen wird er aus dem geklonten Materialrepo.
`LETSMEET_SHARED`, `LETSMEET_NODE`, `LETSMEET_HOME` und `LETSMEET_PG_PORT` werden berücksichtigt;
`CHECK_HISTORY_PATH` kann ausdrücklich überschrieben werden. Versionsangaben müssen V1/V2/V3
sein, damit Tippfehler nicht still im V1-Paket landen.

Zusätzlich wurde die Beschreibung von `letsmeet reset-all` anhand des bestehenden Wrappers
präzisiert: PostgreSQL bleibt erhalten, die Dienste werden gestoppt. Für ein vollständiges
Leeren daher bei laufenden Diensten zuerst `letsmeet leeren`, danach `letsmeet reset-all`.
Der Originalwrapper und das Lehrer-Tools-Repository wurden nicht verändert.

## Inhaltsgegenlese und geschlossene Befunde

Eine unabhängige Claude-Gegenlese verglich die neu geordneten Dateien mit der vorherigen README,
den Website-Regeln für Akt 3 und dem Stationsszenario. Alle bisherigen Pflichten und V1-/V2-/V3-
Vertragsregeln wurden als erhalten beurteilt. Fünf konkrete Formulierungsbefunde wurden korrigiert:

1. Auffindbarkeit der Akt-3-Datei nicht mehr mit der Bearbeitungsfreigabe gleichgesetzt.
2. „Kleiner Ausschnitt“ präzisiert: alle Personen, zunächst nur die verlangten Angaben.
3. Akt-2-Verweis zum Leeren direkt auf die technische Hilfe gerichtet.
4. Arbeitsverzeichnis für die Akt-3-Helferbefehle ausdrücklich genannt.
5. Hilfe bei fehlenden Grundlagen als Angebot statt neuer Genehmigungspflicht formuliert.

Die technische Gegenlese und Browserabnahme werden im Website-Repository dokumentiert.

## Prüfungen dieses Material-Repositories

```bash
bash -n scripts/check-schulserver.sh
node scripts/check-schulserver.test.mjs
git diff --check
```

Der Helfertest verwendet einen lokalen Node-Stub, **keine echte Schülerdatenbank**. Zehn Fälle
prüfen Argumente, Pfade mit Leerzeichen/Sonderzeichen, Umgebungsvariablen, Arbeitsverzeichnis,
Exitcodes 1/2 und frühe Fehler. Zwei gezielte Mutationen in Wegwerfkopien wurden erkannt:
Argumentweitergabe entfernt und Versionsprüfung deaktiviert. Beide führten zu roten Tests.

Eine tatsächliche Ausführung gegen den Schulserver ist damit nicht behauptet. Vor dem nächsten
Unterrichtseinsatz gehört der V3-Durchlauf mit dem neuen Helfer zur Live-Abnahme des Gesamtpakets.
