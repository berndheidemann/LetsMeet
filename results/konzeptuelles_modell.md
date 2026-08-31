# Konzeptuelles Modell (ER-Diagramm)

Dieses Dokument beschreibt das **konzeptuelle Modell** der Datenbank für die Plattform "Let's Meet". Es basiert auf dem ER-Diagramm, das in der entsprechenden Abbildung dargestellt wird.

## Hauptentitäten

1. **User**  
   - Hauptattribute: 
     - User_ID  
     - Vorname  
     - Nachname  
     - CreatedAt / UpdatedAt  
     - Geschlecht  
     - Geburtsdatum  
   - Ein Benutzer kann mit mehreren Entitäten wie Nachrichten, Likes, Hobbys usw. verknüpft sein.

2. **Anmeldedaten**  
   - Hauptattribute:
     - E-Mail  
     - Passwort-Hash  
     - Zeitstempel  
     - Status  
   - Steht in einer 1:1-Beziehung mit **User** (jeder Benutzer hat seine Zugangsdaten).

3. **Hobbys**  
   - Hauptattribute: 
     - Hobby_ID  
     - Name

4. **User_Hobbys** (Zwischenentität)  
   - Attribute: 
     - Priorität (die Priorität des Hobbys für diesen Benutzer)  
   - Verknüpft **User** mit **Hobbys** (N:N-Beziehung).  
   - Ermöglicht die Erfassung der Priorität (oder der Abneigung, wenn der Wert negativ ist).

5. **Freunde**  
   - Verknüpft zwei Benutzer, die befreundet sind.  
   - Hauptattribute: 
     - Freundschafts_ID  
     - User_ID1  
     - User_ID2  
     - Zeitstempel  

6. **Likes**  
   - Repräsentiert ein „Like“ zwischen zwei Benutzern:
     - Liker_User_ID  
     - Liked_User_ID  
     - Status (ausstehend, gegenseitig usw.)  
     - Zeitstempel  

7. **Nachrichten**  
   - Hauptattribute:
     - Nachrichten_ID  
     - Sender_User_ID  
     - Receiver_User_ID  
     - Nachrichtentext  
     - Zeitstempel  
     - Status  

8. **User_Bilder**  
   - Hauptattribute:
     - Bild_ID  
     - Bild (BLOB)  
     - is_profilepicture (gibt an, ob es sich um ein Profilbild handelt)  
     - Zeitstempel_Upload  
   - Steht in einer 1:N-Beziehung mit **User** (ein Benutzer kann mehrere Bilder hochladen).

## Beziehungen und Kardinalitäten

- **User** — (1 zu 1) — **Anmeldedaten**  
  Jeder Benutzer hat seine Authentifizierungsdaten in einer einzigen Zeile (E-Mail, Passwort-Hash usw.).

- **User** — (1 zu N) — **User_Bilder**  
  Ein Benutzer kann mehrere Bilder hochladen.

- **User** — (1 zu N) — **Nachrichten**  
  Ein Benutzer kann viele Nachrichten senden oder empfangen, aber jede Nachricht gehört zu einem einzigen Absender und einem einzigen Empfänger.

- **User** — (1 zu N) — **Likes**  
  Ein Benutzer (Liker_User_ID) kann vielen Benutzern (Liked_User_ID) ein „Like“ geben.

- **User** — (N zu N) — **Freunde**  
  Zwei Benutzer können befreundet sein. Die Tabelle „Freunde“ speichert die Beziehung.

- **User** — (N zu N) — **Hobbys** (mit der Zwischenentität **User_Hobbys**)  
  Ermöglicht die Darstellung der Priorität jedes Hobbys und die Möglichkeit, dass ein Benutzer mehrere Hobbys hat und ein Hobby mehreren Benutzern zugeordnet ist.

## Diagramm

_Es würde eine konzeptuelle Abbildung eingefügt oder darauf verwiesen werden. Das konzeptuelle Diagramm zeigt die Entitäten als Rechtecke und die Beziehungen (mit Rauten), wobei die Kardinalitäten angegeben werden._

---
