# vavoo-parser

A solution to parse [Vavoo](https://www.vavoo.tv) Live TV Stream's via python2 over Web Server & PHP to IPTV Client local on Android TV.

Eine möglichkeit [Vavoo](https://www.vavoo.tv) Live TV Stream's via python2 über einen Lokalen Web Server & PHP zu einem IPTV Client auf einem Android TV zu parsen.

## Getting started / Log gehts

### Prerequisites / Vorraussetungen

[Termux](https://play.google.com/store/apps/details?id=com.termux) installed on your Android Device.

[Termux](https://play.google.com/store/apps/details?id=com.termux) installiert auf deinem Android Gerät.

### 1. Getting the Code / Bekomm die Programm Dateien

The best way to start is to clone our [vavoo-parser](https://github.com/Mastaaa1987/vavoo-parser) into `Termux`.

Der beste Weg zu starten ist [vavoo-parser](https://github.com/Mastaaa1987/vavoo-parser) in `Termux` zu klonen.


```shell
apt update;
apt upgrade -y;
apt install -y wget;
wget https://github.com/Mastaaa1987/vavoo-parser/archive/refs/heads/main.zip;
mv vavoo-parser-main/* $HOME/;
rmdir vavoo-parser-main;
chmod -R 777 *;
```


### 2. Parse the Lists and EPG / Bekomm die Listen und die Zeitschrift

Starting any Browser (aka `Chrome`) on your Android TV and Browse to this URL's.

Starte irgendeinen Browser (aka `Chrome`) auf deinem Android TV und öffne diese URL's.

[http://localhost:8080/m3u8.php](http://localhost:8080/m3u8.php)

`to parse Stream link's into sqlite3 Database & create the m3u8 List's.`

`Um die Stream link's in eine sqlite3 Datenbank einzutragen und die m3u8 Listen zu erstellen.`

[http://localhost:8080/sig.php](http://localhost:8080/sig.php)

`to parse signatur-key into sqlite3 Database.` 

`Um den signatur-key in die sqlite3 Datenbank einzutragen.`

[http://localhost:8080/epg.php](http://localhost:8080/epg.php)

`to create German EPG to epg.xml.gz.`

`Um Deutsches EPG in epg.xml.gz zu erstellen.`

All Files will created in Termux @ `$HOME/lighttpd/www`. / Alle Dateien werden in Termux unter `$HOME/lighttpd/www` gespeichert.

### 3. Load everthing into your IPTV Client App. / Lade alles in deine IPTV Client App.
As Playlist URL input:

Als Playlist URL trage ein:

[http://localhost:8080/Germany.m3u8](http://localhost:8080/Germany.m3u8) 

`Witch Countries available look in Termux @ $HOME/lighttpd/www/` 

`Welche Länder noch verfügbar sind siehst du in Termux unter $HOME/lighttpd/www/`

As EPG URL input: 

Als EPG URL trage ein:

[http://localhost:8080/epg.xml.gz](http://localhost:8080/epg.xml.gz) 

`If you have created German EPG.`

`Wenn du die Fernsehzeitschrift erstellt hast.`


### 4. Setting Http-User-Agent. / Setze den Http-User-Agent.

In your IPTV Client App you need to set the Http-User-Agent to:

In deiner IPTV Client App musst du als Http-User-Agent eintragen:

`VAVOO/2.6`


### 5. Starting a Stream & Enjoy! / Starte einen Stream und freue dich!


## Optional & Backgroud Command's you need. / Optionale & Hintergrund Kommandos die du benötigen wirst.

### After restart type into Termux: / Nach einem neustart in Termux einzugeben:

```shell
./start.sh
```

### If you need to restart lighttpd Server. / Wenn du mal den lighttpd Server neustarten musst.

```shell
pkill lighttpd;
```

### To install Cronjob into Termux: / Um Cronjob in Termux zu installieren:

```shell
pkg install cronie termux-services;
sv-enable crond;
crontab -e # this start's nano / damit startet nano um cronfile zu erstellen ...
```

And type into Texteditor: / Und füge im Texteditor ein:

```shell
#Min Hour DayOfMonth Month DayOfWeek [command]
#Min Std TagImMonat Monat TagDerWoche [command]
0 */6 * * * python2 ~/lighttpd/www/playlist.py m3u8 # Take every 6 Hour's new m3u8 list's / Aktuallisiert alle 6 Stunden m3u8 Listen.
0 23 * * * bash ~/epg.sh epg # Create every Day new epg.xml.gz / Erstellt jeden Tag um 23 Uhr neue epg.xml.gz
```


### Background Info's. / Hintergrund Informationen.
- The Python plugin witch I used for the EPG is forkt from this [repo](https://github.com/chriszero/tvspielfilm2xmltv)
- Das Python Plugin welche hier genutzt wird kommt ursprünglich von diesem [repo](https://github.com/chriszero/tvspielfilm2xmltv)
