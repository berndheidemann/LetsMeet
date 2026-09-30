# Lernsituation: LetsMeet-Datenmigration

Die **Let’s Meet GmbH** wechselt nach einer schwierigen Trennung den IT-Dienstleister. Statt einer
laufenden Datenbank liegen nur schrittweise freigegebene Datenstände vor. Euer Team rekonstruiert
daraus eine PostgreSQL-Datenbank, die eine Anzeige-App der Kundin (im Folgenden: Kundinnen-App)
wieder versorgen kann.

![Ausschnitt aus „Tea with friends, and one must wear one's finest hat!“ (Public Domain)](./images/tea-with-friends.png)

## Einstieg

Die Begleit-Website zeigt euch die vollständigen Aufträge je Akt und führt euch durch die
Übergänge zwischen ihnen:

**[LetsMeet-Projektbegleitung öffnen](https://station.heidelab.de/letsmeet/)**

Sie speichert euren Stand nur lokal im Browser. Sie ist keine Abgabe und prüft weder Datenbank
noch ER-Diagramm selbst. Die Website und die folgenden Dateien verwenden dieselben
Arbeitsanweisungen. Ihr könnt sie also auch hier im Repository nachlesen:

- [Arbeitsweise, Befundnotiz und Artefakte](./auftrag/projekt.md) — gilt für alle Akte
- [Akt 1 — Erste Daten aus Excel](./auftrag/akt-1.md)
- [Akt 2 — Zielmodell und MongoDB](./auftrag/akt-2.md)
- Akt 3 folgt, sobald die Begleit-Website ihn nach Akt 2 freigibt.

## Vorbereitung und Arbeitsumgebung

Der technische Einstieg — Start/Stopp in beiden Betriebsarten (Docker oder Schulserver),
Verbindungsdaten, Datenverträge umstellen, Fehlerhilfe — steht gesammelt unter
[Technischer Einstieg](./auftrag/technik.md). Eure Lehrkraft sagt euch, welche Betriebsart für
euch gilt; an den Aufgaben ändert das nichts.

## Materialübersicht

| Datei | Zweck |
|---|---|
| [`Lets Meet DB Dump.xlsx`](./Lets%20Meet%20DB%20Dump.xlsx) | Quelle für Akt 1 und Akt 2 |
| [`Lets_Meet_Hobbies.xml`](./Lets_Meet_Hobbies.xml) | Basisdatei für Akt 3, bleibt bis dahin unberührt |
| [`gute-tabellen.md`](./gute-tabellen.md) | fachliche Hilfe: woran man unaufgeräumte Tabellen erkennt |
| [`normalization.md`](./normalization.md) | fachliche Hilfe: Normalisierung bis zur 3. Normalform |
| [`notebooks/00-zugriff.ipynb`](./notebooks/00-zugriff.ipynb) | Verbindungstest zu PostgreSQL und MongoDB |
| [`notebooks/01-erd-zu-tabelle.ipynb`](./notebooks/01-erd-zu-tabelle.ipynb) | Aufwärmrunde vor Akt 1 |
| [`images/use-case.png`](./images/use-case.png) | Anwendungsfalldiagramm für Akt 2 |
| [`compose.yml`](./compose.yml) | Docker-Betrieb (Variante A) |
| [`scripts/check-schulserver.sh`](./scripts/check-schulserver.sh) | Schulserver-Prüfaufruf mit Zusatzargumenten (Akt 3) |
