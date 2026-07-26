# Rücklauf aus der ERD-Modellierungsstation (Paket 4)

> **Lehrerartefakt, nicht an Lernende ausgeben.**
> Stand: 26. Juli 2026. Quelle: Umsetzungs-Session im Repo `~/projects/heidelab/erd.heidelab.de`.
> Dieses Dokument spiegelt **fachliche Entscheidungen** zurück, die beim Bau der Station getroffen
> wurden und in der Lernsituation nachgezogen werden müssen. Ohne diesen Rücklauf laufen
> Lernsituation und Station auseinander.

## 1. Was gebaut wurde, in drei Sätzen

Die ERD-Werkbank kann jetzt **mehrere gleichwertig korrekte Lösungen pro Aufgabe** prüfen: Eine
Aufgabe deklariert pro Aspekt mehrere zulässige Formen, die Engine wählt deterministisch die
bestpassende und prüft **beide Phasen** dagegen. Zusätzlich beherrscht sie **m:n-Selbstbezüge**
(Person–Person), die vorher weder deklarierbar noch ableitbar waren. Die LetsMeet-Aufgabe ist
gebaut und geprüft: alle **8** zulässigen Kombinationen gehen befundfrei durch.

## 2. Änderung, die `LEHRER-ERD-STATION.md` betrifft (Handlungsbedarf)

**Der Varianten-Aspekt „Hobby-Taxonomie" ist entfallen.** §3 dieses Dokuments führt eine Tabelle mit
**vier** Aspekten; es sind jetzt **drei**:

| Aspekt | Variante A | Variante B |
|---|---|---|
| Personen-Schlüssel | Surrogat-ID, E-Mail als Attribut | E-Mail als Schlüssel |
| Adresse | Attribute in Person | eigene Adress-Entität |
| Freundschaft | gerichtet mit Bestätigung | ungerichtet |

**Begründung (Bernd, 26.07.2026):** Die Herkunft einer Hobbyzuordnung war nie als dauerhafte
fachliche Eigenschaft gedacht. Die Zielsetzung war: Excel hat für bestimmte Personen schon Hobbys,
XML bringt neue dazu. Ob eine Zuordnung vor Jahren aus Excel oder XML kam, behält man nicht
dauerhaft. Damit entfällt der Grund, aus dem getrennte Entitäten überhaupt als vertretbare Form
galten: der **Vokabular-Unterschied** zwischen den rund 220 langen Excel-Beschreibungen und den
rund 30 kurzen XML-Begriffen.

Es bleibt **eine** gemeinsame Entität `Hobby`, mit `Priorität` (nullable) und `Quelle` als
**Beziehungsattributen**. Das ist deckungsgleich mit Vertrag V2 §4, der `migration_user_hobbies` als
**eine** View mit **einem** Namensraum plus `source`-Spalte verlangt. Die getrennte Form hätte beim
View-Bau ohnehin wieder vereinigen müssen.

**Nachzuziehen:** §3-Tabelle, jeder Verweis auf „vier Aspekte", und die Zuordnung von Q-03/XM-06 als
Modellierungsfreiheit.

## 3. Q-03 bleibt jetzt offen (Verbesserung gegenüber dem ursprünglichen Design)

Der ursprüngliche Entwurf hätte über den Taxonomie-Aspekt implizit vorentschieden, wie Hobbys und
Aktivitäten zueinander stehen. **Das ERD entscheidet Q-03 jetzt nicht mehr vor.** Die Frage bleibt
Kundinnenfrage und Aushandlungsstoff im Unterricht.

Damit verbunden: Die **Suchpräferenz** (Wertebereich −100..100, `0` neutral) hängt eindeutig an der
einen `Hobby`-Entität. Die zwischenzeitlich offene Frage, an welche von zwei getrennten Entitäten
sie gehört, ist gegenstandslos geworden.

## 4. Offene Idee, bewusst nicht umgesetzt: XML-Hobbys sprachlich angleichen

Bernds Vorschlag im Gespräch: die XML-Hobbys beschreibender formulieren, damit die Vokabulare
zusammenpassen. Fachlich löst das den Vokabular-Unterschied tatsächlich auf.

**Nicht umgesetzt, weil es die Quelldaten der Lernsituation ändert.** Betroffen wären:

- die eingefrorenen Zielwerte, insbesondere **4.828** Hobbyzuordnungen
- die bereits gebauten V2-Checks (`server/src/checks/engineV2.ts`)
- Vertrag V2 §4 selbst

Das gehört in einen bewussten **V3-Schritt** in diesem Repo, nicht nebenbei in eine Session im
Werkbank-Repo. Für die Modellierungsstation wird es nicht gebraucht: Ohne die getrennte Form ist der
Vokabular-Unterschied dort kein Thema mehr.

## 5. Spannung, die offen bleibt: `source` im Vertrag vs. Zielsetzung

Vertrag V2 §4 verlangt `source` als Pflichtspalte in `migration_user_hobbies`, und der Vertrag ist
seit dem 25.07. verbindlich **und gebaut**. Bernds Sicht ist, dass die Herkunft nur Übergangswert
hat. Solange der Vertrag gilt, muss das ERD sie tragen können, deshalb führt das kanonische Modell
`Quelle` als Beziehungsattribut. **Wenn V3 die Spalte streicht, muss das ERD mitgezogen werden.**

Ebenfalls im Modell festgehalten: `Priorität` ist nullable, weil die XML-Quelle sie nie liefert
(XM-04). Sie hängt an der Hobby-Beziehung, nicht an der Entität.

## 6. Was die Station jetzt kann und die Lernsituation nutzen darf

- **m:n-Selbstbezüge** sind deklarierbar, ableitbar und prüfbar. Das betrifft **Like** und
  **Freundschaft** (beide Person–Person). Vorher hätte ein *korrektes* Schülermodell dort
  Falsch-Rot bekommen. Nebeneffekt: Der öffentliche Aufgabenkatalog kann jetzt rekursive
  m:n-Aufgaben führen (Verlinkung, Stückliste), was vorher unmöglich war.
- **Deklarierte Varianten** mit deterministischer Best-Fit-Auflösung über beide Phasen.
- **Die gelesene Form wird im Feedback benannt** („Gelesen als: …"). Das stützt die
  Bewertungs-Kohärenz aus §7: Im Fachgespräch wird die **Begründung** der Varianten-Wahl bewertet,
  also muss die Gruppe wissen, dass sie eine getroffen hat.
- **Eskalationstext bei unerkannter Struktur**, mit Einspruchs-Aufforderung an die Lehrkraft. Er
  erscheint bewusst **nicht** bei klaren Fehlern, sonst würde er zur Standardfloskel.

### Eine Wortlaut-Abweichung, die du kennen solltest

Der Eskalationstext aus `LEHRER-ERD-STATION.md` §4 enthält einen Gedankenstrich („Das kann ein
Modellierungsfehler sein — oder eine Variante …"). Der Copy-Style-Lint des Werkbank-Repos verbietet
Em-Dashes in sichtbaren Produkttexten. Im ausgelieferten Text steht daher ein **Komma** statt des
Gedankenstrichs; Bedeutung und Ton sind unverändert. Falls du den Gedankenstrich willst, müsste der
Lint angepasst werden.

## 7. Was NICHT gebaut ist

Die LetsMeet-Aufgabe existiert im Werkbank-Repo, ist validiert und durch Tests abgesichert — aber
sie ist **nirgends ausgeliefert**. Offen sind:

- **Auftrag 4, Einzel-Aufgaben-Instanz:** eigene Auslieferung ohne Aufgaben-Bibliothek, eigener
  Titel, eigenes Deploy-Ziel. Die Entscheidung Build-Flag vs. deklaratives Instanz-Profil ist laut
  Handover bewusst erst unmittelbar vor dem Bau zu treffen.
- **Auftrag 5, Begleit-Website:** Registrierungsfeld für die Share-URL. Liegt in LetsMeet-Paket 5.

**Die Aufgabe taucht im öffentlichen Katalog von `erd.heidelab.de` nicht auf** und ist durch einen
Test dagegen abgesichert. Es gibt also derzeit keine URL, die man den Gruppen geben könnte.

## 8. Konkrete To-dos in diesem Repo

- [ ] `LEHRER-ERD-STATION.md` §3: Tabelle auf drei Aspekte kürzen, „vier Aspekte" ersetzen.
- [ ] `LEHRER-ERD-STATION.md` §6: Umsetzungsauftrag 1 und 2 als erledigt markieren, 4 und 5 als offen.
- [ ] Entscheiden, ob die Idee aus §4 dieses Dokuments (XML-Hobbys angleichen) als V3-Kandidat in
      `LEHRER-VIEWS-VERTRAG.md` §5a aufgenommen wird.
- [ ] Prüfen, ob Q-03 im `LEHRER-DATENQUALITAETSKONZEPT.md` einen Vermerk braucht, dass die
      Modellierungsstation die Frage bewusst **nicht** vorentscheidet.

## 9. Wo die Details liegen

Im Repo `~/projects/heidelab/erd.heidelab.de`:

- `docs/superpowers/specs/2026-07-25-letsmeet-station-design.md` — Design und Begründungen, §6.2
  enthält die Streichung der Hobby-Taxonomie im Wortlaut.
- `docs/superpowers/plans/2026-07-25-letsmeet-station.md` — der Umsetzungsplan.
- `src/tasks/letsmeet/letsmeet.ts` — das kanonische Modell.
- `VISION.md` §4.9 (E) — die deklarierten Varianten als Teil des Determinismus-Kerns.
