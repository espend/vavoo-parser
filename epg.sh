#!/data/data/com.termux/files/usr/bin/bash

if [ "$1" == "epg" ] || [ "$1" == "" ]; then
    ro="/data/data/com.termux/files/home";

    db="$ro/lighttpd/www/playlist.db";
    if ! [ -e "$db" ]; then echo "Error! playlist.db not found!"; exit 1; fi;
    xmltv=`which tvspielfilm2xmltv`;
    if ! [ -e "$xmltv" ]; then
        xmltv="$ro/.local/bin/tvspielfilm2xmltv";
        if ! [ -e "$xmltv" ]; then
            xmltv="/data/data/com.termux/files/usr/lib/python2.7/site-packages/tvspielfilm2xmltv.py";
            if ! [ -e "$xmltv" ]; then echo "Error! tvspielfilm2xmltv not found!"; exit 1; fi;
        fi;
    fi;
    ini="$ro/tvspielfilm2xmltv.ini";
    if ! [ -e "$ini" ]; then echo "Error! tvspielfilm2xmltv.ini not found!"; exit 1; fi;
    con="$ro/tvspielfilm2xmltv.control";
    if ! [ -e "$ini" ]; then echo "Error! tvspielfilm2xmltv.control not found!"; exit 1; fi;

    cd $ro;

    epgfile=`cat $ini | grep destination_file | sed -e 's/.* = //g'`;
    confile=`cat $ini | grep control_file | sed -e 's/.* = //g'`;
    imgdir=`cat $ini | grep epgimages_dir | sed -e 's/.* = //g'`;

    if [ -e "$epgfile" ]; then rm $epgfile; fi;
    if ! [ -e "$confile" ]; then mkdir -p $(dirname $confile); cp $con $confile; fi;
    if ! [ -d "$imgdir" ]; then mkdir -p $imgdir; fi;

    $xmltv 5 '' "123.tv" "13th Street Universal" "3sat" "Animal Planet" "ANIXE" "ARD alpha" "ARTE" "Auto Motor Sport" "AXN" "Bibel TV" "Bloomberg Europe TV" "BR" "Cartoon Network" "Classica" "Comedy Central" "CRIME + INVESTIGATION" \
"Das Erste" "DAZN" "DELUXE MUSIC" "Deutsches Musik Fernsehen" "Discovery HD" "Disney Channel" "DMAX" "Eurosport 1" "Eurosport 2" "Fix &amp; Foxi" "Health TV" "Heimatkanal" "History HD" "HR" "HSE24" "Jukebox" "kabel eins" \
"kabel eins classics" "kabel eins Doku" "KiKA" "KinoweltTV" "K-TV" "MDR" "Motorvision TV" "MTV" "N24 Doku" "Nat Geo HD" "NAT GEO WILD" "NDR" "nick" "Nick Jr." "Nicktoons" "NITRO" "n-tv" "ONE" "ORF 1" "ORF 2" "ORF III" "ORF SPORT +" \
"PHOENIX" "ProSieben" "ProSieben Fun" "ProSieben MAXX" "Romance TV" "RTL" "RTL Crime" "RTL II" "RTL Living" "RTL Passion" "RTLplus" "SAT.1" "SAT.1 emotions" "SAT.1 Gold" "ServusTV" "Silverline" "sixx" "Sky Action" "Sky Atlantic HD" \
"Sky Cinema Best Of" "Sky Cinema Classics" "Sky Cinema Fun" "Sky Cinema Premieren" "Sky Cinema Premieren +24" "Sky Cinema Special HD" "Sky Cinema Thriller" "Sky Comedy" "Sky Crime" "Sky Family" "Sky Krimi" "Sky One" \
"Sony Channel" "Spiegel Geschichte" "Spiegel TV Wissen" \
"SUPER RTL" "SWR/SR" "Syfy" "tagesschau24" "Tele 5" "TLC" "TNT Comedy" "TNT Film" "TNT Serie" "TOGGO plus" "Universal Channel HD" "VOX" "VOXup" "WDR" "ZDF" "ZDFinfo" "ZDFneo";
    if ! [ -e "$epgfile" ]; then echo "Error! epg.xml not found!"; exit 1; fi;
    gzip epg.xml;
    if [ -e "epg.xml.gz" ]; then
        if [ -e "lighttpd/www/epg.xml.gz" ]; then rm lighttpd/www/epg.xml.gz; fi;
        mv epg.xml.gz lighttpd/www/;
        echo "epg.xml.gz successful created @ $ro/lighttpd/www";
        exit 0;
    else echo "Error! creating epg.xml.gz!"; exit 1; fi;
else
    echo "$(basename $0) syntax error!";
    echo "";
    echo "Please try again ...";
    exit 1;
fi;
