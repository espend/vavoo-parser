#!/data/data/com.termux/files/usr/bin/bash

apt update;
apt install -y root-repo x11-repo;
apt upgrade -y;
apt install -y python2 lighttpd php curl wget;
pip2 install --upgrade pip;
pip2 install requests pytz;

if ! [ -d "/data/data/com.termux/files/usr/lib/python2.7/site-packages/tvsp2xmltv" ] || ! [ -e "/data/data/com.termux/files/usr/lib/python2.7/site-packages/tvspielfilm2xmltv.py" ]; then
    cp -r /data/data/com.termux/files/home/tvsp2xmltv /data/data/com.termux/files/usr/lib/python2.7/site-packages/;
    cp /data/data/com.termux/files/home/tvspielfilm2xmltv.py /data/data/com.termux/files/usr/lib/python2.7/site-packages/;
fi;

echo "init Done! Now start: ./start.sh ...";

/data/data/com.termux/files/home/start.sh;
