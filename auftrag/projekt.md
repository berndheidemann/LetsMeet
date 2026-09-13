# Arbeitsweise, Befundnotiz und Artefakte

## Hinweis für laufende Teams

Die Aufträge sind jetzt übersichtlicher geordnet und unklare Stellen präzisiert. Es gibt dadurch
**keine zusätzlichen Abgaben**. Arbeitet an eurem bisherigen Stand weiter: Wegen dieser Umstellung
müsst ihr **keine Datenbank leeren oder Modelle neu erstellen**. Bestehende Absprachen mit eurer
Lehrkraft bleiben bestehen.

Zum Wiederfinden bisheriger Stellen bleibt die
[alte Aufgabenfassung](https://github.com/berndheidemann/LetsMeet/blob/b19984ea3bcbcc5f6951463344f8fa7214ff8d4c/readme.md)
als Orientierung erreichbar. Sie wird nicht weiter gepflegt; die aktuellen Aufträge findet ihr
hier und in den Akt-Karten der Begleit-Website.

## Arbeitsweise

Ihr arbeitet in drei Akten. Akt 1 und Akt 2 sind vollständig beschrieben ([Akt 1](./akt-1.md),
[Akt 2](./akt-2.md)); die Begleit-Website gibt Akt 3 erst frei, wenn Akt 2 abgeschlossen ist. Für
jeden aktuell freigegebenen Akt baut ihr die Datenbank mit euren Skripten **aus einer leeren
PostgreSQL-Datenbank neu auf** und prüft das Ergebnis. Ein anderes Team muss denselben Aufbau
wiederholen können — genau das ist mit einem reproduzierbaren Import gemeint. Die Tabellen hinter
den geforderten Datenbankansichten (Views) dürft ihr selbst entwerfen.

Ihr baut die Migration schrittweise aus. In Akt 1 übernehmt ihr alle Personen aus der Excel-Datei,
aber zunächst nur die Angaben, die der Datenvertrag V1 verlangt, bis in die Kundinnen-App. In Akt 2 erweitert ihr diesen Stand zum vollständigen
Zielmodell und integriert die MongoDB-Daten. Ihr beginnt also nicht jedes Mal wieder bei null:
Eure Modelle, Skripte und Beobachtungen sind die Grundlage für den nächsten Schritt.

Wenn im Auftrag „aus einer leeren Datenbank neu aufbauen" steht, geht es um eure Skripte: Sie
müssen Tabellen und Views erneut anlegen und die Daten erneut importieren können. Gemeint ist
nicht, dass ihr euren Entwurf oder eure bisherigen Skripte wegwerfen sollt.

Der Prüfstand in der Kundinnen-App gibt euch Hinweise zum Weiterarbeiten. Für den Abschluss eines
Akts zählt der Prüfbefehl im Terminal nach einem frischen Datenbankaufbau. Haltet ihr ein rotes
Ergebnis für fachlich falsch, gebt der Lehrkraft Quelle, betroffenen Datensatz und eure
Begründung.

**Zur Arbeitsweise:** In diesem Auftrag begegnen euch Techniken, die im Unterricht noch nicht dran
waren — das gehört dazu und ist kein Versehen. Erwartet wird nicht, dass ihr das alles schon
könnt, sondern dass ihr euch einarbeitet: recherchiert, lest Dokumentation, fragt im Team und
nutzt KI-Werkzeuge dort, wo sie euch weiterbringen. Eine Bedingung gilt dabei immer: Ihr müsst
alles, was ihr abgebt, erklären können — woher es stammt, was es tut und warum ihr euch so
entschieden habt. Was ihr nicht erklären könnt, gehört nicht in eure Abgabe.

Die Begleit-Website zeigt euch die vollständigen Aufträge je Akt und führt euch durch die Übergänge:

**[LetsMeet-Projektbegleitung öffnen](https://station.heidelab.de/letsmeet/)**

Sie speichert euren Stand nur lokal im Browser. Sie ist keine Abgabe und prüft weder Datenbank noch
ER-Diagramm selbst.

## Vor Akt 1: eine Aufwärmrunde

Bevor es an die echten Daten geht, macht ihr **alle** einmal die
[Aufwärmrunde im Notebook](../notebooks/01-erd-zu-tabelle.ipynb) —
35 Minuten an einem fremden Fall, einer Fahrradwerkstatt. Aus einem kleinen ER-Diagramm baut ihr
zwei Tabellen, füllt sie, prüft die Beziehung mit einem `JOIN` und beantwortet eine Frage. Vier
Schritte, nach jedem steht ein prüfbares „Fertig, wenn …".

Der Zweck: `CREATE TABLE`, `INSERT` und `JOIN` einmal an einem winzigen Fall gesehen zu haben,
bevor sie in Akt 1 gleichzeitig mit Datenqualität, Migration und Git auf euch treffen. Mit
Let's Meet hat der Fall nichts zu tun — übertragen müsst ihr selbst. Alle Tabellen darin heißen
`demo_…` und stören eure spätere Migration nicht.

## Eure Artefakte

- Versioniert SQL, Importcode und eigene Datenprüfungen mit Git.
- Erstellt physische Modelle und die zugehörigen SQL-Anweisungen zur Definition der
  Datenbankstruktur (DDL) für die aufgenommenen Quelldaten und das PostgreSQL-Zielsystem — je Akt
  entsprechend seines Umfangs (siehe [Akt 1](./akt-1.md), [Akt 2](./akt-2.md)).
- Schreibt eigene SQL-Abfragen oder automatisierte Tests für eure zentralen Importannahmen; der
  Kundinnen-Checker ergänzt diese, ersetzt sie aber nicht.
- Führt eine **Befundnotiz** — das eine schriftliche Stück, das ihr durchgehend pflegt (siehe
  unten).

Alles Weitere — Modelle, Skripte, Tests — legt ihr so ab, wie es euch dient. Verbindlich ist nicht
die Ordnerstruktur, sondern dass ein anderes Team eure Entscheidungen nachvollziehen und die
Prüfbefehle nach einem eigenen Neuaufbau erneut ausführen kann.

## Eure Befundnotiz

Ihr führt **ein** schriftliches Dokument durch das ganze Projekt — nennt es
`results/befundnotiz.md`. Es entsteht **ab der ersten Woche** und wächst mit: Ihr schreibt hinein,
sobald ihr etwas findet oder entscheidet, nicht rückwirkend am Ende. Wer sie erst zum Schluss
schreibt, merkt das im Fachgespräch.

Drei Fragen tragen die Notiz. Zu jedem Eintrag gehört das Datum:

1. **Was ist uns an der Quelle aufgefallen?** Beobachtungen, nicht Vermutungen — auffällige
   Formate, Mehrfachwerte, Lücken, Widersprüche, offene Fragen an die Kundin.
2. **Was haben wir daraufhin entschieden, und warum?** Die Regel, die ihr angewendet habt, dazu
   die Alternative, die ihr verworfen habt, und was sie gekostet hätte.
3. **Was haben wir nicht übernommen, und warum?** Was nicht importiert ist, fehlt sichtbar — hier
   steht, weshalb.

Dazu einmal im Projekt, spätestens wenn ihr die Daten das erste Mal vollständig vor euch habt:

4. **Welche dieser Daten sind besonders schützenswert, und was folgt daraus für euren Umgang
   damit?**

Datenschutz ist hier ein Randthema: Wenige Stichpunkte zu dieser Frage genügen. Ein eigenes
Datenschutzkonzept, eine juristische Prüfung der Rechtsgrundlagen oder ein Maßnahmenkatalog sind
nicht Teil eures Auftrags.

Die Notiz ist kein Aufsatz. Stichpunkte genügen, solange sie jemand anderes versteht. Sie ist euer
eigenes Arbeitsmittel: **Im Fachgespräch dürft ihr sie offen vor euch liegen haben.**

In Akt 2 speichert ihr dort zusätzlich die Freigabe-URL (Share-URL) eures ERD-Modells (siehe
[Akt 2](./akt-2.md)).
