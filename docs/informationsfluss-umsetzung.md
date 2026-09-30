# Informationsfluss und kontrollierter Wechsel im laufenden LetsMeet-Kurs

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

Die neue Fassung wurde zunächst auf `next/informationsfluss` in beiden Repositories gesichert,
ohne den laufenden Kurs zu verändern. Am 13.09.2026 hat Bernd ausdrücklich den kontrollierten
Wechsel **im laufenden Kurs** freigegeben: Übergangshinweis, zugängliche Altfassung und unveränderte
fachliche Anforderungen. Material und Website werden deshalb zusammen veröffentlicht, nicht als
isolierter README-Hotfix.

Der Hinweis für laufende Teams steht verbindlich in `auftrag/projekt.md`; die Website übernimmt
ihn aus demselben Snapshot. Die alte README bleibt über den unveränderlichen Commit `b19984e`
erreichbar, ausdrücklich nur zur Orientierung. Bestehende Absprachen mit der Lehrkraft bleiben
bestehen. Wegen der Informationsumstellung werden weder Modelle noch Datenbanken zurückgesetzt.
Bereits geklonte Schülerprojekte können den neuen Akt-3-Helfer einzeln über einen fest gepinnten
Download nachladen, ohne eigene Dateien oder das gesamte Projekt zu ersetzen.

Nach Kursende hat Bernd am 30.09.2026 den Hinweis für laufende Teams zurückgenommen: Er steht
nicht mehr in `auftrag/projekt.md` und `readme.md`, und die Website zeigt keinen Übergangshinweis
mehr. Der Altfassungs-Commit `b19984e` bleibt in der Git-Historie erhalten.

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

## Schulserver-Abnahme am 13.09.2026

Nach Herstellung der Schul-VPN-Verbindung wurde der Helfer auf `euler-host` tatsächlich geprüft:
in einem temporären Container des vorhandenen Images `euler-jhub:v42-litellm`, ohne externes
Netzwerk, mit der produktiven Schüler-Mountquelle read-only unter `/opt/letsmeet` und einer
eigens angelegten PostgreSQL-Instanz. Verwendet wurden die vorhandene App (Stand `f3113b9`),
Node 16.20.2 und PostgreSQL 16.14 auf ppc64le. Alle vier Ground-Truth-Dateien waren hashgleich
zur lokalen Referenzquelle.

- Referenz-V3-Import zweimal ausgeführt: Snapshot speichern und vergleichen jeweils Exit 0;
  erst der Vergleich setzt `gateComplete` und `gatePassed`.
- Zulässige Begründung gezielt verändert: Snapshotvergleich erkennt den Unterschied,
  `v3-idempotency` rot und Exit 1.
- Fehlende Snapshotdatei: Exit 2 wird durchgereicht.
- Snapshotpfad mit Leerzeichen und Umlaut funktioniert.
- Download des gepinnten Helfers aus dem Jupyter-Container über den Schüler-Zugangsweg `euler`:
  SHA-256 stimmt mit der getesteten Datei überein
  (`697b90b6235149d67aeabfae5613003c823e3d3e81bf8f524577a9d02b0305a4`).

Die temporäre Datenbank wurde gestoppt, Container und Testverzeichnis wurden entfernt. Keine
bestehende Schülerdatenbank, kein laufender Schülerprozess und keine gemeinsame Installation
wurden geändert. Dies prüft den Helfer mit einer Referenzlösung, nicht die individuellen
Migrationen der Lernenden. Probe und Ergebnisprotokoll liegen lokal unter
`/tmp/letsmeet-rollout-20260913/`; die wesentlichen Befunde sind hier dauerhaft festgehalten.
