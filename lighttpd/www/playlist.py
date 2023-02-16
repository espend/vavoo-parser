#!/data/data/com.termux/files/usr/bin/python2

import sys, re, os, requests, sqlite3, json, time, urllib, base64, codecs, threading, random, gzip, ssl
from datetime import date
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib2 import urlopen, Request, HTTPError

db = '/data/data/com.termux/files/home/lighttpd/www/playlist.db'
hurl = 'http://localhost:8080'

def m3u8():
    #url = 'https://www2.vavoo.to/live2/index'
    matches1 = ["13TH", "AXN", "A&E", "INVESTIGATION", "TNT", "DISNEY", "SKY", "WARNER"]
    matches2 = ["BUNDESLIGA", "SPORT", "TELEKOM"]
    matches3 = ["CINE", "EAGLE", "KINO", "FILMAX", "POPCORN"]
    groups = []

    con = sqlite3.connect(db)
    cur = con.cursor()

    ssl._create_default_https_context = ssl._create_unverified_context
    req = Request('https://www2.vavoo.to/live2/index?output=json', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'})
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    response = urlopen(req)
    content = response.read().decode('utf8')
    channel = json.loads(content)

    for c in channel:
        url = c['url']
        group = c['group']
        if c['group'] not in groups:
            groups.append(c['group'])
        if c['group'] == 'Germany':
            if any(x in c['name'] for x in matches1):
                group = 'Sky'
            if any(x in c['name'] for x in matches2):
                group = 'Sport'
            if any(x in c['name'] for x in matches3):
                group = 'Cine'
        cur.execute('SELECT * FROM channel WHERE name="' + c['name'].encode('ascii', 'ignore').decode('ascii') + '" AND grp="' + group + '"')
        test = cur.fetchone()
        if not test:
            name = re.sub('( (AUSTRIA|AT|HEVC|RAW|SD|HD|FHD|UHD|H265|GERMANY|DEUTSCHLAND|1080|DE|S-ANHALT|SACHSEN|MATCH TIME))|(\\+)|( \\(BACKUP\\))|\\(BACKUP\\)|( \\([\\w ]+\\))|\\([\\d+]\\)', '', c['name'].encode('ascii', 'ignore').decode('ascii'))
            logo = c['logo']
            tid = ''
            if c['group'] == 'Germany':
                cur.execute('SELECT * FROM tvs WHERE name="' + name + '" OR name1="' + name + '" OR name2="' + name + '" OR name3="' + name + '" OR name4="' + name + '"')
                test = cur.fetchone()
                if test:
                    tid = test[0]
                    logo = test[2]
            cur.execute('INSERT INTO channel VALUES(NULL,"' + c['name'].encode('ascii', 'ignore').decode('ascii') + '","' + group + '","' + logo + '","' + tid + '","' + c['url'] + '","' + name + '")')
        else:
            cur.execute('UPDATE channel SET url="' + c['url'] + '" WHERE name="' + c['name'].encode('ascii', 'ignore').decode('ascii') + '" AND grp="' + group + '"')

    con.commit()

    for group in groups:
        if os.path.exists("/data/data/com.termux/files/home/lighttpd/www/%s.m3u8" % group):
            os.remove("/data/data/com.termux/files/home/lighttpd/www/%s.m3u8" % group)
        tf = open("/data/data/com.termux/files/home/lighttpd/www/%s.m3u8" % group, "w")
        tf.write("#EXTM3U")
        tf.close()

    for c in channel:
        group = c['group']
        if c['group'] not in groups:
            groups.append(c['group'])
        if c['group'] == 'Germany':
            if any(x in c['name'] for x in matches1):
                group = 'Sky'
            if any(x in c['name'] for x in matches2):
                group = 'Sport'
            if any(x in c['name'] for x in matches3):
                group = 'Cine'
        cur.execute('SELECT * FROM channel WHERE name="' + c['name'].encode('ascii', 'ignore').decode('ascii') + '" AND grp="' + group + '"')
        row = cur.fetchone()
        if row:
            tf = open("/data/data/com.termux/files/home/lighttpd/www/%s.m3u8" % c['group'], "a")
            if not str(row[3]) == '' and not str(row[4]) == '':
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s" tvg-logo="%s" tvg-id="%s",%s' % (row[1], row[2], row[3], row[4], row[6]))
            elif not str(row[3]) == '' and str(row[4]) == '':
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s" tvg-logo="%s",%s' % (row[1], row[2], row[3], row[6]))
            elif not str(row[4]) == '' and  str(row[3]) == '':
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s" tvg-id="%s",%s' % (row[1], row[2], row[4], row[6]))
            else:
                tf.write('\n#EXTINF:-1 tvg-name="%s" group-title="%s",%s' % (row[1], row[2], row[6]))
            tf.write('\n#EXTVLCOPT:http-user-agent=VAVOO/2.6')
            tf.write('\n%s/playlist2.php?id=%s' % (hurl, row[0]))
            tf.close()
        else:
            print('error!')
    con.close()
    print('\nAll Done!')


def sig():
    try:
        vec = {"vec": "9frjpxPjxSNilxJPCJ0XGYs6scej3dW/h/VWlnKUiLSG8IP7mfyDU7NirOlld+VtCKGj03XjetfliDMhIev7wcARo+YTU8KPFuVQP9E2DVXzY2BFo1NhE6qEmPfNDnm74eyl/7iFJ0EETm6XbYyz8IKBkAqPN/Spp3PZ2ulKg3QBSDxcVN4R5zRn7OsgLJ2CNTuWkd/h451lDCp+TtTuvnAEhcQckdsydFhTZCK5IiWrrTIC/d4qDXEd+GtOP4hPdoIuCaNzYfX3lLCwFENC6RZoTBYLrcKVVgbqyQZ7DnLqfLqvf3z0FVUWx9H21liGFpByzdnoxyFkue3NzrFtkRL37xkx9ITucepSYKzUVEfyBh+/3mtzKY26VIRkJFkpf8KVcCRNrTRQn47Wuq4gC7sSwT7eHCAydKSACcUMMdpPSvbvfOmIqeBNA83osX8FPFYUMZsjvYNEE3arbFiGsQlggBKgg1V3oN+5ni3Vjc5InHg/xv476LHDFnNdAJx448ph3DoAiJjr2g4ZTNynfSxdzA68qSuJY8UjyzgDjG0RIMv2h7DlQNjkAXv4k1BrPpfOiOqH67yIarNmkPIwrIV+W9TTV/yRyE1LEgOr4DK8uW2AUtHOPA2gn6P5sgFyi68w55MZBPepddfYTQ+E1N6R/hWnMYPt/i0xSUeMPekX47iucfpFBEv9Uh9zdGiEB+0P3LVMP+q+pbBU4o1NkKyY1V8wH1Wilr0a+q87kEnQ1LWYMMBhaP9yFseGSbYwdeLsX9uR1uPaN+u4woO2g8sw9Y5ze5XMgOVpFCZaut02I5k0U4WPyN5adQjG8sAzxsI3KsV04DEVymj224iqg2Lzz53Xz9yEy+7/85ILQpJ6llCyqpHLFyHq/kJxYPhDUF755WaHJEaFRPxUqbparNX+mCE9Xzy7Q/KTgAPiRS41FHXXv+7XSPp4cy9jli0BVnYf13Xsp28OGs/D8Nl3NgEn3/eUcMN80JRdsOrV62fnBVMBNf36+LbISdvsFAFr0xyuPGmlIETcFyxJkrGZnhHAxwzsvZ+Uwf8lffBfZFPRrNv+tgeeLpatVcHLHZGeTgWWml6tIHwWUqv2TVJeMkAEL5PPS4Gtbscau5HM+FEjtGS+KClfX1CNKvgYJl7mLDEf5ZYQv5kHaoQ6RcPaR6vUNn02zpq5/X3EPIgUKF0r/0ctmoT84B2J1BKfCbctdFY9br7JSJ6DvUxyde68jB+Il6qNcQwTFj4cNErk4x719Y42NoAnnQYC2/qfL/gAhJl8TKMvBt3Bno+va8ve8E0z8yEuMLUqe8OXLce6nCa+L5LYK1aBdb60BYbMeWk1qmG6Nk9OnYLhzDyrd9iHDd7X95OM6X5wiMVZRn5ebw4askTTc50xmrg4eic2U1w1JpSEjdH/u/hXrWKSMWAxaj34uQnMuWxPZEXoVxzGyuUbroXRfkhzpqmqqqOcypjsWPdq5BOUGL/Riwjm6yMI0x9kbO8+VoQ6RYfjAbxNriZ1cQ+AW1fqEgnRWXmjt4Z1M0ygUBi8w71bDML1YG6UHeC2cJ2CCCxSrfycKQhpSdI1QIuwd2eyIpd4LgwrMiY3xNWreAF+qobNxvE7ypKTISNrz0iYIhU0aKNlcGwYd0FXIRfKVBzSBe4MRK2pGLDNO6ytoHxvJweZ8h1XG8RWc4aB5gTnB7Tjiqym4b64lRdj1DPHJnzD4aqRixpXhzYzWVDN2kONCR5i2quYbnVFN4sSfLiKeOwKX4JdmzpYixNZXjLkG14seS6KR0Wl8Itp5IMIWFpnNokjRH76RYRZAcx0jP0V5/GfNNTi5QsEU98en0SiXHQGXnROiHpRUDXTl8FmJORjwXc0AjrEMuQ2FDJDmAIlKUSLhjbIiKw3iaqp5TVyXuz0ZMYBhnqhcwqULqtFSuIKpaW8FgF8QJfP2frADf4kKZG1bQ99MrRrb2A="}
        req = requests.post('https://www.vavoo.tv/api/box/ping2', data=vec).json()
        sig = req['response'].get('signed')
        stime = int(time.time())

        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute('DELETE FROM sig')
        cur.execute('INSERT INTO sig VALUES("' + sig + '","' + str(stime) + '")')
        con.commit()
        con.close()
    except Exception  as e:
        raise


def sig2():
    try:
        vec = {"vec": "9frjpxPjxSNilxJPCJ0XGYs6scej3dW/h/VWlnKUiLSG8IP7mfyDU7NirOlld+VtCKGj03XjetfliDMhIev7wcARo+YTU8KPFuVQP9E2DVXzY2BFo1NhE6qEmPfNDnm74eyl/7iFJ0EETm6XbYyz8IKBkAqPN/Spp3PZ2ulKg3QBSDxcVN4R5zRn7OsgLJ2CNTuWkd/h451lDCp+TtTuvnAEhcQckdsydFhTZCK5IiWrrTIC/d4qDXEd+GtOP4hPdoIuCaNzYfX3lLCwFENC6RZoTBYLrcKVVgbqyQZ7DnLqfLqvf3z0FVUWx9H21liGFpByzdnoxyFkue3NzrFtkRL37xkx9ITucepSYKzUVEfyBh+/3mtzKY26VIRkJFkpf8KVcCRNrTRQn47Wuq4gC7sSwT7eHCAydKSACcUMMdpPSvbvfOmIqeBNA83osX8FPFYUMZsjvYNEE3arbFiGsQlggBKgg1V3oN+5ni3Vjc5InHg/xv476LHDFnNdAJx448ph3DoAiJjr2g4ZTNynfSxdzA68qSuJY8UjyzgDjG0RIMv2h7DlQNjkAXv4k1BrPpfOiOqH67yIarNmkPIwrIV+W9TTV/yRyE1LEgOr4DK8uW2AUtHOPA2gn6P5sgFyi68w55MZBPepddfYTQ+E1N6R/hWnMYPt/i0xSUeMPekX47iucfpFBEv9Uh9zdGiEB+0P3LVMP+q+pbBU4o1NkKyY1V8wH1Wilr0a+q87kEnQ1LWYMMBhaP9yFseGSbYwdeLsX9uR1uPaN+u4woO2g8sw9Y5ze5XMgOVpFCZaut02I5k0U4WPyN5adQjG8sAzxsI3KsV04DEVymj224iqg2Lzz53Xz9yEy+7/85ILQpJ6llCyqpHLFyHq/kJxYPhDUF755WaHJEaFRPxUqbparNX+mCE9Xzy7Q/KTgAPiRS41FHXXv+7XSPp4cy9jli0BVnYf13Xsp28OGs/D8Nl3NgEn3/eUcMN80JRdsOrV62fnBVMBNf36+LbISdvsFAFr0xyuPGmlIETcFyxJkrGZnhHAxwzsvZ+Uwf8lffBfZFPRrNv+tgeeLpatVcHLHZGeTgWWml6tIHwWUqv2TVJeMkAEL5PPS4Gtbscau5HM+FEjtGS+KClfX1CNKvgYJl7mLDEf5ZYQv5kHaoQ6RcPaR6vUNn02zpq5/X3EPIgUKF0r/0ctmoT84B2J1BKfCbctdFY9br7JSJ6DvUxyde68jB+Il6qNcQwTFj4cNErk4x719Y42NoAnnQYC2/qfL/gAhJl8TKMvBt3Bno+va8ve8E0z8yEuMLUqe8OXLce6nCa+L5LYK1aBdb60BYbMeWk1qmG6Nk9OnYLhzDyrd9iHDd7X95OM6X5wiMVZRn5ebw4askTTc50xmrg4eic2U1w1JpSEjdH/u/hXrWKSMWAxaj34uQnMuWxPZEXoVxzGyuUbroXRfkhzpqmqqqOcypjsWPdq5BOUGL/Riwjm6yMI0x9kbO8+VoQ6RYfjAbxNriZ1cQ+AW1fqEgnRWXmjt4Z1M0ygUBi8w71bDML1YG6UHeC2cJ2CCCxSrfycKQhpSdI1QIuwd2eyIpd4LgwrMiY3xNWreAF+qobNxvE7ypKTISNrz0iYIhU0aKNlcGwYd0FXIRfKVBzSBe4MRK2pGLDNO6ytoHxvJweZ8h1XG8RWc4aB5gTnB7Tjiqym4b64lRdj1DPHJnzD4aqRixpXhzYzWVDN2kONCR5i2quYbnVFN4sSfLiKeOwKX4JdmzpYixNZXjLkG14seS6KR0Wl8Itp5IMIWFpnNokjRH76RYRZAcx0jP0V5/GfNNTi5QsEU98en0SiXHQGXnROiHpRUDXTl8FmJORjwXc0AjrEMuQ2FDJDmAIlKUSLhjbIiKw3iaqp5TVyXuz0ZMYBhnqhcwqULqtFSuIKpaW8FgF8QJfP2frADf4kKZG1bQ99MrRrb2A="}
        req = requests.post('https://www.vavoo.tv/api/box/ping2', data=vec).json()
        sig = req['response'].get('signed')

        print(sig)
    except Exception  as e:
        raise


def test():
    print('Python2 Test')


def main():
    if len(sys.argv) == 1:
        print('Play with the Best...')
    else:
        if sys.argv[1] == 'm3u8':
            m3u8()
        elif sys.argv[1] == 'sig':
            sig()
        elif sys.argv[1] == 'sig2':
            sig2()
        elif sys.argv[1] == 'test':
            test()
        else:
            print('Syntax Error!')


if __name__ == '__main__':
    main()

