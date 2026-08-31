# Beispiele für SQL-Abfragen

## 1. Priorisierte Hobbys eines Benutzers
-- Zeige die Hobbys eines Benutzers (nach user_id) in absteigender Priorität  
SELECT h.name AS hobby_name,
       uh.prio
FROM user_hobbys uh
JOIN hobbys h ON uh.hobby_id = h.hobby_id
WHERE uh.user_id = 123
ORDER BY uh.prio DESC;

## 2. Freundesliste eines Benutzers
-- Zeige die Freunde eines Benutzers mit user_id = 10  
SELECT u.user_id, u.vorname, u.nachname
FROM freunde f
JOIN users u ON (f.user_id1 = u.user_id OR f.user_id2 = u.user_id)
WHERE (f.user_id1 = 10 OR f.user_id2 = 10)
  AND u.user_id <> 10;

## 3. Ausstehende Likes (status = 'pending') eines Benutzers
-- Zeige, wem der Benutzer 10 ein "Like" gegeben hat, das noch aussteht  
SELECT liked_user_id, status, created_at
FROM likes
WHERE liker_user_id = 10
  AND status = 'pending';

## 4. Gesendete und empfangene Nachrichten eines Benutzers
-- Zeige die Nachrichten des Benutzers 10, sowohl als Sender als auch als Empfänger  
SELECT m.message_id,
       sender_user_id,
       receiver_user_id,
       message_content,
       created_at,
       status
FROM nachrichten m
WHERE m.sender_user_id = 10
   OR m.receiver_user_id = 10
ORDER BY created_at DESC;

## 5. Profilbild eines Benutzers anzeigen
-- Zeige das Bild (BLOB), das als "is_profilepicture = TRUE" markiert ist  
SELECT bild_id, image, timestamp_upload
FROM user_bilder
WHERE user_id = 10
  AND is_profilepicture = TRUE;

## 6. Den Status eines Likes auf 'mutual' ändern
-- Beispiel: Wenn Benutzer 10 und Benutzer 20 sich gegenseitig geliked haben  
UPDATE likes
SET status = 'mutual'
WHERE (liker_user_id = 10 AND liked_user_id = 20)
   OR (liker_user_id = 20 AND liked_user_id = 10);
