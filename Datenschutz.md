# Datenschutzmaßnahmen für die App "lets_meet"

## **Erforderlichkeiten zur Verarbeitung und Speicherung der Daten**

### **Rechtsgrundlage für die Datenverarbeitung**
Damit die Daten der Benutzer der App verarbeitet werden dürfen, müssen die rechtlichen Grundlagen der DSGVO eingehalten werden. Dabei sind folgende Punkte zu beachten:

### **1. Einwilligung**
- Nutzer müssen aktiv und freiwillig zustimmen, dass ihre Daten verarbeitet werden.  
- Dies erfolgt durch eine klare Datenschutzerklärung, der der Benutzer beim Erstellen seines Kontos zustimmen muss.

### **2. Vertragserfüllung**
- Daten, die notwendig sind, um das Hauptziel der App zu ermöglichen, dürfen verarbeitet werden.

### **3. Zweckbindung**
- Die Daten dürfen nur für klar definierte Zwecke erhoben und verarbeitet werden.

### **4. Datensparsamkeit**
- Es dürfen nur Daten erhoben werden, die für die Nutzung der App unbedingt erforderlich sind.  
- Daten wie Adresse und Telefonnummer wurden bewusst aus dem Datenbankmodell entfernt.

### **5. Speicherbegrenzung**
- Personenbezogene Daten dürfen nicht länger als notwendig gespeichert werden.

### **6. Transparenz**
- Nutzer müssen klar darüber informiert werden, welche Daten erhoben werden, warum sie erhoben werden, wie sie verarbeitet werden und wie lange sie gespeichert werden.

### **7. Rechte der Benutzer**
- **Recht auf Vergessenwerden**: Nutzer können verlangen, dass alle ihre Daten dauerhaft gelöscht werden.  
- **Widerrufsrecht**: Nutzer können ihre Zustimmung zur Verarbeitung ihrer Daten widerrufen.  
- **Recht auf Auskunft**: Nutzer können Informationen darüber anfordern, ob und welche personenbezogenen Daten verarbeitet werden.  
- **Recht auf Berichtigung**: Nutzer können die Korrektur unrichtiger oder unvollständiger Daten verlangen.  

---

## **Datenarten und Schutzmaßnahmen**

### **1. Personenbezogene Daten**
**Beispiele**: Vorname, Nachname, E-Mail, Geburtstag, Geschlecht  
**Schutzmaßnahmen**:  
- Speicherung in verschlüsselter Form  
- Beschränkter Zugriff auf die Daten  
- Anonymisierung oder Pseudonymisierung, wo möglich  

---

### **2. Sensible Daten**
**Beispiele**: Präferenzen, Interessen (Hobbys), sexuelle Orientierung  
**Schutzmaßnahmen**:  
- Speicherung auf separaten, stark gesicherten Servern  
- Anonymisierung oder Pseudonymisierung, wo möglich  
- Einholung einer expliziten Einwilligung  

---

### **3. Kommunikationsdaten**
**Beispiele**: Nachrichteninhalte, Likes  
**Schutzmaßnahmen**:  
- Ende-zu-Ende-Verschlüsselung für private Nachrichten  
- Logs und Metadaten (z. B. Zeitstempel) nur so lange speichern, wie notwendig  

---

### **4. Bilddaten**
**Beispiele**: Profilbilder, hochgeladene Fotos  
**Schutzmaßnahmen**:  
- Speicherung in einem sicheren Cloud-Storage mit Zugriffsbeschränkungen  
- Automatische Erkennung und Entfernung potenziell problematischer Inhalte  
- Sicherstellen, dass gelöschte Bilder nicht mehr in der Datenbank oder Backups vorhanden sind  

---

### **5. Metadaten**
**Beispiele**: Zeitstempel von Logins, Likes, Matches  
**Schutzmaßnahmen**:  
- Anonymisierung der Metadaten, sofern sie für Analysen verwendet werden  
- Beschränkung des Zugriffs auf aggregierte Daten  

---

### **6. Anmeldedaten**
**Beispiele**: Passwort, E-Mail  
**Schutzmaßnahmen**:  
- Verwendung eines starken Hash-Algorithmus für Passwörter (z. B. bcrypt, Argon2)  
- Zufälliges Salt für jedes Passwort, um Rainbow-Table-Angriffe zu verhindern  
- Speicherung in einer verschlüsselten Datenbank  
- Regelmäßige Sicherheitsüberprüfungen und Penetrationstests  