# LetsMeet — Real-Pilot-Paket

**Vorbereitet:** 1. August 2026

**Status:** Software-Gate `PASS`; Geräte-Preflight vor Einladung auf den tatsächlichen Schülergeräten erforderlich

## Freigabegrundlage

Der fokussierte Drei-Persona-Re-Test ist grün:

- SIM-01: Editor-/Kardinalitätsklicks in Standard- und dichter LetsMeet-Station;
- SIM-02: History-Auswahl bleibt gegen Hover autoritativ;
- SIM-03: Querywechsel und umgekehrte Response-Reihenfolge bleiben konsistent;
- SIM-05: ausgeschriebene FK-Rollen grün, erfundene Suffixe rot;
- Share, Persistenz, Zoom, Aufräumen, Companion-Registrierung und mobile Breite ohne Regression.

Audit: `kundinnen-app/audits/2026-08-01-schueler-sim-fokussierter-retest.md`

Der lokale Compose-Stand pinnt die im Re-Test verwendete Kundinnen-App:

```text
berndheidemann/letsmeet-kundinnen-app:v3-sim03-2026-08-01
sha256:7623de38b059b9b2f58b0d10918e3a5c4c12a19ce0aa6f3ac553b2bd6c1f38ea
```

## Verbindliche Produktentscheidungen vor dem Pilot

### SIM-04 — keine zusätzliche Quellen-Erinnerung

Die Begleit-Website erhält vorerst keinen zusätzlichen Erinnerungssatz und die Station keine
kompakte Feldliste. Migrationsvertrag, Excel, XML und MongoDB-Backup sind gemeinsam der Auftrag;
das selbstständige Zusammenführen dieser Quellen ist Teil der Analyseleistung. Im Pilot wird
beobachtet, ob Lernende die vorhandenen Quellen tatsächlich wiederfinden. Erst wiederholte reale
Retrieval-Probleme rechtfertigen eine erneute Designentscheidung.

### SIM-06 — aktuelle Best-Match-Semantik bleibt

Eine erkannte variantenspezifische Entität bindet den Variantenaspekt nicht bis zu ihrer Entfernung.
Die deterministisch bestpassende Form darf im unfertigen Zwischenstand wechseln. Eine monotone
Bindung würde den allgemeinen Variantenvertrag materiell ändern; eine einzelne simulierte
Irritation reicht dafür nicht. Im Pilot wird der konkrete Adress-Zustandswechsel beobachtet.

## Teilnehmer und Format

**Besetzung:** zwei bis drei Auszubildende, anonym als `P1`–`P3`.

| Kennung | Profil | Schwerpunkt |
|---|---|---|
| P1 | wenig ERD-/SQL-Routine | Quellenorientierung, Feedback-Recovery, Kardinalitäten |
| P2 | mittlerer Ausbildungsstand | Transfer Training → LetsMeet, Rollen-FKs, Share |
| P3 optional | leistungsstark | Varianten, Einspruchsweg, V3-Gate-Semantik |

**Block 1 — ERD-Transfer, 60–75 Minuten**

1. Begleitung bis Akt 2.
2. Sinnvolle Stichprobe der vier Trainingsfälle.
3. LetsMeet Phase 1.
4. Share-URL erzeugen und in der Begleitung registrieren.
5. Phase 2 beginnen; keine künstliche Grünvorgabe.

**Block 2 — Daten-/Gate-Verständnis, 30–45 Minuten**

1. Kundinnen-App und formativer Browserlauf.
2. CLI-Lauf gegen den eigenen frischen Teilnehmerstand.
3. Verlauf lesen: Browser-Zwischenstand, CLI-Capture, Zweitimport, Compare-Gate.
4. Erklären lassen, welche Aussage der jeweilige Punkt tatsächlich trägt.

Der Pilot muss nicht das gesamte Migrationsprojekt abschließen. Ziel ist die Tragfähigkeit der
Übergänge und Rückmeldungen.

## Geräte-Preflight — am Vortag pro Arbeitsplatz

Die Compose-Datei verwendet feste Ports und feste Containernamen. Deshalb entweder **ein eigener
Docker-Host pro Teilnehmer** oder sequenzielle Nutzung mit vollständigem Reset; keine parallelen
Teilnehmerstände auf demselben Docker-Daemon.

### 1. Voraussetzungen

```bash
git pull --ff-only
docker --version
docker compose version
docker compose config --quiet
```

Folgende Dateien müssen vorhanden und lesbar sein:

```text
Lets Meet DB Dump.xlsx
Lets_Meet_Hobbies.xml
readme.md
normalization.md
compose.yml
```

### 2. Images vorladen

```bash
docker compose pull
```

Dabei muss insbesondere das Image `v3-sim03-2026-08-01` geladen werden.

### 3. Teilnehmerstand leeren und starten

Nur auf dem dafür vorgesehenen Pilotgerät:

```bash
docker compose down -v
docker compose up -d
```

`down -v` löscht PostgreSQL, MongoDB und Prüfhistorie dieses Geräts. Vorher sicherstellen, dass auf
dem Docker-Daemon kein erhaltenswerter LetsMeet-Stand liegt.

### 4. Technisch prüfen

```bash
docker compose ps
curl -fsS http://localhost:3611/api/status
```

Erwartung zu Beginn:

- Kundinnen-App antwortet;
- `contractVersion` ist `V1`;
- PostgreSQL und MongoDB laufen;
- ein fehlendes `migration_users` ist im leeren Schülerstand erwartbar und kein Preflight-Fehler.

Zusätzlich im Browser öffnen:

- `http://localhost:3611`
- `https://station.heidelab.de/letsmeet/`
- `https://erd.heidelab.de/`
- `https://station.heidelab.de/letsmeet-erd/`

### 5. Browserzustand trennen

Für P1–P3 getrennte Browserprofile verwenden. Vor jeder Person:

- Begleit-Website-`localStorage` leer;
- Standard-ERD- und LetsMeet-Station-Stand leer;
- keine geteilten Tabs oder Zwischenablagen aus dem vorherigen Lauf;
- Browserzoom 100 %; Hardware-/OS-Zoom dokumentieren.

### 6. Freigabeentscheidung

Erst einladen, wenn pro Gerät dokumentiert ist:

```text
[ ] Docker/Compose vorhanden
[ ] compose config grün
[ ] Images vollständig gepullt
[ ] PostgreSQL läuft
[ ] MongoDB läuft
[ ] Kundinnen-App lokal erreichbar, V1
[ ] vier HTTPS-Ziele erreichbar
[ ] eigener Browserzustand
[ ] vollständiger Reset einmal praktisch ausgeführt
```

## Beobachtungsbogen

Pro kritischem Moment genau eine Zeile:

| Zeit | Person | sichtbare Aktion/wörtliche Äußerung | tatsächlicher Systemzustand | Hilfe | Hängezeit | Recovery | Kandidat/Prinzip |
|---|---|---|---|---|---:|---|---|
| | P1/P2/P3 | Beobachtung, keine Interpretation | DOM/Checker/CLI-Evidenz | keine / Referenz / Peer / Lehrkraft | min | selbst / Hinweis / nicht | Slug oder neu |

Interpretationen separat notieren. Eine Schüleräußerung ist noch kein Bug.

## Leitfragen

1. Findet die Person Vertrag und Rohdaten wieder, ohne dass die Station den Auftrag wiederholt?
2. Überträgt sie m:n, Beziehungsattribute, Selbstbezug und Rollen-FKs aus dem Training?
3. Bleiben Kardinalitäten bei offenem Editor erreichbar?
4. Versteht sie die Share-URL als Modelltransport, nicht als fachliche Abgabe?
5. Unterscheidet sie Browser-Zwischenstand, Snapshot, Zweitimport und Compare-Gate?
6. Erzeugt der Adress-Best-Match-Wechsel produktive Revision oder lähmende Widerspruchswahrnehmung?
7. Eskaliert sie vermeintliches Falsch-Rot mit Quelle und Begründung statt durch Alias-Raten?

## Datenschutz und Einwilligung

Vorschlag für die mündliche Einleitung:

> Wir testen heute die Lernumgebung, nicht euch. Eure Teilnahme ist freiwillig und hat keinen
> Einfluss auf Bewertung oder Unterricht. Ich notiere anonymisierte Beobachtungen unter P1 bis P3.
> Es gibt standardmäßig keine Audio-, Video- oder Bildschirmaufnahme. Ihr könnt jederzeit ohne
> Begründung abbrechen.

- Einwilligung vor Beginn dokumentieren.
- Keine Namen, E-Mail-Adressen oder persönliche Profildaten in den Pilotbericht übernehmen.
- Keine Aufzeichnung als Default.
- Rohnotizen nach der anonymisierten Synthese löschen.

## Abbruchkriterien

Pilot sofort pausieren bei:

- Datenverlust oder Vermischung von Teilnehmerständen;
- falsch dargestelltem Gate-Abschluss;
- zwei unabhängigen Personen, die an derselben Kernsteuerung scheitern;
- nicht erreichbarer lokaler Kundinnen-App oder öffentlicher Station;
- Rücknahme der Einwilligung;
- Beeinträchtigung des regulären Unterrichts.

## Auswertung innerhalb von 24 Stunden

1. Beobachtung und Interpretation trennen.
2. Wiederholungen nach Root Cause clustern.
3. Kandidaten rejection-first gegen Code, Quellen und Prinzipien prüfen.
4. SIM-04 und SIM-06 nur bei real wiederholter Evidenz erneut öffnen.
5. Bericht unter `kundinnen-app/audits/<datum>-realpilot-findings.md` sichern.
6. Echte Pilotbeobachtungen ausdrücklich von der vorangegangenen Simulation unterscheiden.

## Noch einzutragen

```text
Pilotdatum:
Raum/Geräte:
Beobachtende Person:
P1-Profil:
P2-Profil:
P3-Profil optional:
Preflight durchgeführt am/von:
```
