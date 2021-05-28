 Ein Bump Bot in Discord.py!

## Eigenschaften
- Einfach zu konfigurierender Bot
- Direkte Unterstützung durch die Entwickler
- Webhook-Beulen
- Serverlistenerweiterung

# Einrichten
### Bot konfigurieren
- Benennen Sie `config-example.yml` in` config.yml` um und ändern Sie die Werte.
```jaml
Manager:
- Manager
- IDs
Prefix: "bevorzugtes Prefix"
Token: "Bot-Token"
version: 'bot-version'
mongo: "mongo-uri"
bot_name: "bot-name"
`` `
#### Beispielkonfiguration
```jaml
Manager:
- 219567539049594880
Prefix: "="
Token: "Th1s1s4vE5yG0odT0k3n1.M4yB3.To0G6DT0B3Tr93z" # Gefälschtes Token
Version: '1.0'
mongo: "mongodb + srv: // dbuser: dbpassword@cluster0.r4nd0m.mongodb.net/"
bot_name: "BytesBump"
`` `
### Ändern von `settings.json`
- `settings.json` enthält Daten zur Funktionalität des Bots. Sie können alle Werte ändern.
`` `json
{
    "cooldown": 3600, // COOLDOWN in Sekunden
    "show_motd": false, // motd.txt nach dem Bumpen anzeigen
    "show_motd_wait": 10, // Wartezeit bis zum Anzeigen von motd.txt
    "enable_serverlist": false, // Serverliste aktivieren. Scrollen Sie nach unten, um weitere Informationen zu erhalten.
    "serverlist_url": "http://127.0.0.1:5000/" // Index-URL für die Serverliste (mit dem Schrägstrich am Ende)
}}
`` `
Wenn Sie sich entscheiden, die obige Konfiguration zu kopieren, entfernen Sie die Kommentare pls.

# Datenbank vorbereiten
Um die Serverdaten speichern zu können, benötigen Sie eine ** Mongo-Datenbank **. Sie können eine kostenlose ** 500MB ** Datenbank von [MongoDB Atlas] (https://www.mongodb.com/cloud/atlas) erhalten. Das reicht für Dutzende von Servern.


Wählen Sie die "KOSTENLOSE" und geben Sie ihr einen Namen. Folge diesen Schritten;
- Gehen Sie zum Abschnitt "Datenbankzugriff" auf der Registerkarte "Sicherheit" und klicken Sie auf "+ NEUEN BENUTZER HINZUFÜGEN". Geben Sie ihm die Berechtigung "Lesen und Schreiben in eine beliebige Datenbank", damit der Bot die Daten ordnungsgemäß speichern kann. Geben Sie ihm einen Benutzernamen und ein **sicheres** Passwort. Speichern Sie nur das Passwort.
! [Neuer Benutzer] (https://i.imgur.com/zfhxyNX.png)
- Damit der Bot tatsächlich auf die Datenbank zugreifen kann, sollten Sie alle IP-Adressen auf die Whitelist setzen. Gehen Sie zum Abschnitt "Netzwerkzugriff" unter der Registerkarte "Sicherheit" und klicken Sie auf "+ IP-ADRESSE HINZUFÜGEN". Klicken Sie auf `Zugriff von überall zulassen` und `0.0.0.0/0` sollte im `Whitelist-Eintrag` erscheinen. Wenn dies nicht der Fall ist, geben Sie es manuell ein. Klicken Sie abschließend auf Bestätigen.
![Alle IPs auf die weiße Liste setzen](https://i.imgur.com/UgIYkoA.png)
- Zeit, sich mit der Datenbank zu verbinden! Gehen Sie zu "Cluster" unter der Registerkarte "DATENSPEICHER". Wenn Ihre Datenbank noch eingerichtet ist, warten Sie bitte, bis sie fertig ist! Sobald dies der Fall ist, klicken Sie auf die Schaltfläche "VERBINDEN" und dann auf "Ihre Anwendung verbinden". Kopieren Sie einen Link, der so **aussieht**; `mongodb+srv://<Benutzername>:<Passwort>@cluster0.r4nd0m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`
- Entfernen Sie zum Schluss den Teil "myFirstDatabase? RetryWrites = true & w = Mehrheit" und ersetzen Sie "<Benutzername>" durch den Namen Ihres Benutzers (manchmal wird er bereits ersetzt, wenn nur ein Benutzer vorhanden ist) und "<Kennwort>" durch Ihr gespeichertes Passwort . Nehmen Sie den Link und fügen Sie ihn als Wert von "mongo" in "config.yml" ein!
- Ihre Datenbank ist fertig!

# Serverlistenerweiterung
Ihr Bot ist im Grunde fertig. Sie können es sofort verwenden! Wir stellen Ihnen jedoch eine Serverlisten-Website zur Verfügung, auf der alle in der Datenbank gespeicherten Server angezeigt werden! Sie können ** [dieses Repo] (https://github.com/Nemika-Haj/BytesBumpList) ** auschecken, um die Serverliste einzurichten.

# Zusätzliche Information
## Unterstützung
Wenn Sie Fragen haben, besuchen Sie **(https://discord.gg/penguins**!
