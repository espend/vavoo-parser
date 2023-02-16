#!/data/data/com.termux/files/usr/bin/python2
# -*- coding: utf-8 -*-
import operator
import os
import stat
import ConfigParser

import requests
import logger


# ugo+rw because may different user work with this file
file_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH


def find_in_path(file_name, path=None):
    """
    Search for file in the defined pathes
    """
    path = path or '/etc/tvspielfilm2xmltv:/etc/vdr/plugins/tvspielfilm2xmltv'
    for directory in path.split(os.pathsep):
        file_path = os.path.abspath(os.path.join(directory, file_name))
        if os.path.exists(file_path):
            return file_path
    return file_name


config = ConfigParser.ConfigParser()
conf_file = find_in_path('tvspielfilm2xmltv.ini')
config.read(conf_file)

destination_file = config.get('DEFAULT', 'destination_file')
control_file = config.get('DEFAULT', 'control_file')
epgimages_dir = config.get('DEFAULT', 'epgimages_dir')
remove_orphaned_images = config.getboolean('DEFAULT', 'remove_orphaned_images')
grab_today = config.getboolean('DEFAULT', 'grab_today')
number_of_images_per_show = config.getint('DEFAULT', 'number_of_images_per_show')
size_of_images = config.getint('DEFAULT', 'size_of_images')
debug = config.getboolean('DEFAULT', 'debug')

sart_map = {
    'SE': 'series',
    'SP': 'movie',
    'RE': 'news',
    'KIN': 'kids',
    'SPO': 'sports',
    #'AND': 'Andere',
    #'U': 'Undefined'
}
thumb_id_map = {
    'DOWN': 1,
    'MIDDLE': 2,
    'UP': 3
}

combination_channels = {
    'nickcomedy.de': ['NICK', 'CC']
}

channel_map = {
    'PRO7M': 'ProSieben MAXX',
    'ARD': 'Das Erste',
    'ZDF': 'ZDF',
    'RTL': 'RTL',
    'SAT1': 'SAT.1',
    'PRO7': 'ProSieben',
    'K1': 'kabel eins',
    'RTL2': 'RTL II',
    'VOX': 'VOX',
    '3SAT': '3sat',
    'ARTE': 'ARTE',
    'TELE5': 'Tele 5',
    'CC': 'Comedy Central',
    'DMAX': 'DMAX',
    'SIXX': 'sixx',
    'RTL-N': 'NITRO',
    'SAT1G': 'SAT.1 Gold',
    'SUPER': 'SUPER RTL',
    'KIKA': 'KiKA',
    'NICK': 'nick',
    'RIC': 'ric.de',
    'BR': 'BR',
    'HR': 'HR',
    'PHOEN': 'PHOENIX',
    'TAG24': 'tagesschau24',
    'FES': 'ONE',
    'MUX': 'einsplus.de',
    '2NEO': 'ZDFneo',
    '2KULT': 'zdfkultur.de',
    'ZINFO': 'ZDFinfo',
    'ANIXE': 'ANIXE',
    'SKLAR': 'Sonnenklar.TV',
    'BIBEL': 'Bibel TV',
    'CNN': 'cnn.de',
    'N24': 'n24.de',
    'NTV': 'n-tv',
    'SPORT': 'SPORT1',
    'S1PLU': 'SPORT1+',
    'EURO': 'Eurosport 1',
    'EURO2': 'Eurosport 2',
    'SPO-D': 'sportdigital Fussball',
    'DMC': 'DELUXE MUSIC',
    'MTV': 'MTV',
    'VIVA': 'viva.de',
    'VH1': 'vh1-classic.uk',
    'ATV': 'atv.at',
    'ATV2': 'atv2.at',
    'ORF1': 'ORF 1',
    'ORF2': 'ORF 2',
    'ORF3': 'ORF III',
    'ORFSP': 'ORF SPORT +',
    'PULS4': 'puls4.at',
    'SERVU': 'ServusTV',
    'SF1': 'SRF 1',
    'STTV': 'star-tv.ch',
    'SF2': 'SRF zwei',
    '3PLUS': '3plus.ch',
    'CIN': 'Sky Cinema Premieren',
    'CIN1': 'sky-cinema-1.de',
    'CIN24': 'Sky Cinema Premieren +24',
    'SKY-H': 'Sky Cinema Best Of',
    'SKY-A': 'Sky Action',
    'SKY-C': 'Sky Cinema Fun',
    'SKY-E': 'sky-emotion.de',
    'SKY-N': 'Sky Cinema Classics',
    'MGM': 'mgm.de',
    'DCM': 'disney-cinemagic.de',
    'SKY3D': 'sky-3d.de',
    'SKYAT': 'Sky Atlantic HD',
    'N-GHD': 'Nat Geo HD',
    'HDDIS': 'Discovery HD',
    'HISHD': 'History HD',
    'SNHD': 'Sky Sport News',
    'BULI': 'Sky Sport Bundesliga',
    'SPO-A': 'Sky Sport Austria',
    'HDSPO': 'Sky Sport HD 1',
    'SHD2': 'Sky Sport HD 2',
    '13TH': '13th Street Universal',
    'CLASS': 'Classica',
    'DISNE': 'Disney Channel',
    'DXD': 'disney-xd.de',
    'DJUN': 'Disney Junior',
    'FOX': 'FOX',
    'GOLD': 'goldstar-tv.de',
    'HEIMA': 'Heimatkanal',
    'MOVTV': 'Motorvision TV',
    'JUNIO': 'Junior',
    'N-GW': 'NAT GEO WILD',
    'PASS': 'RTL Passion',
    'RTL-C': 'RTL Crime',
    'SCIFI': 'Syfy',
    'SP-GE': 'Spiegel Geschichte',
    'SKY-K': 'Sky Krimi',
    'TNT-S': 'TNT Serie',
    'AXN': 'AXN',
    'AMAX': 'animax.de',
    'BOOM': 'boomerang-tv.de',
    'C-NET': 'Cartoon Network',
    'K1CLA': 'kabel eins classics',
    'KINOW': 'KinoweltTV',
    'NICKT': 'Nicktoons',
    'ROM': 'Romance TV',
    'RTL-L': 'RTL Living',
    'SAT1E': 'SAT.1 emotions',
    'TNT-F': 'TNT Film',
    'SKY-S': 'Sky select',
    'APLAN': 'Animal Planet',
    'GUSTO': 'bongusto.de',
    'E!': 'E! Entertainment',
    'GLITZ': 'glitz.de',
    'PLANE': 'Planet',
    'PBOY': 'playboy.de',
    'PRO7F': 'ProSieben Fun',
    'SILVE': 'Silverline',
    'SPTVW': 'Spiegel TV Wissen',
    'FATV': 'fashiontv.fr',
    'HSE': 'HSE24',
    'JUKE': 'Jukebox',
    'SONY': 'Sony Channel',
    'DR1': 'dr1.dk',
    'GEO': 'geo-television.de',
    'WDWTV': 'Welt der Wunder TV',
    'NAUCH': 'nautical-channel.com',
    'BBC-E': 'bbc-entertainment.dk',
    'FAMTV': 'family-tv.de',
    'EURON': 'euronews.de',
    'LAUNE': 'gute-laune-tv.de',
    'QVC': 'qvc.de',
    'CENTE': 'center.tv',
    'NL1': 'nl1.nl',
    'NL3': 'nl2.nl',
    'NL2': 'nl3.nl',
    'UNIVE': 'Universal Channel HD',
    'BLM': 'Bloomberg Europe TV',
    'MUE2': 'muenchen-2.de',
    'DWTV': 'dw.de',
    'BE1': 'belgien.be',
    'MEZZO': 'mezzotv.fr',
    'BUTV': 'beate-uhse-tv.de',
    'TVM': 'tv-muenchen.de',
    'MOTOR': 'motors-tv.fr',
    'TVB': 'tv-berlin.de',
    'AETV': 'ae-tv.de',
    'MTV-D': 'mtv-dance.uk',
    'MTV-B': 'mtv-base.de',
    'MTV-L': 'mtv-live.uk',
    'BBC': 'bbcworld.uk',
    'MTV-H': 'mtv-hits.uk',
    'TV2': 'tv2.tr',
    'TLC': 'TLC',
    'EX-SP': 'extreme-sports-channel.de',
    'TRACE': 'tracetv.fr',
    'BLUM': 'blue-movie-1.de',
    'JOIZ': 'joiz.de',
    'BLUM3': 'blue-movie-3.de',
    'BLUM2': 'blue-movie-2.de',
    'HH1': 'hamburg-1.de',
    'RCK': 'rcktv.de',
    'DAF': 'deutsches-anleger-fernsehen.de',
    'TV5': 'tv5-monde.fr',
    'SP1US': 'sport1US.de',
    'YFE': 'yourfamilyentertainment.de',
    'KTV': 'K-TV',
    'N-GP': 'nat-geo-people.de',
    'DWF': 'deutsches-wetter-fernsehen.de',
    'ADULT': 'adult-channel.com',
    'LUSTP': 'lust-pur.de',
    'ALPHA': 'ARD alpha',
    'WDR-MS' : 'wdr-muenster.de',
    'SWRRP' : 'swr-rp.de',
    'REGIO' : 'regio-tv.de',
    'BLIZZ' : 'blizztv.de',
    'ALJAZ' : 'al-jazeera.com',
    'WDR-DU' : 'wdr-duisburg.de',
    'SWRBW' : 'swr-bw.de',
    'SACH' : 'sachsen-fernsehen.de',
    'WDR-DO' : 'wdr-dortmund.de',
    'NDR-SH' : 'ndr-sh.de',
    'NDR-MV' : 'ndr-mv.de',
    'RB-TV' : 'radio-bremen-tv.de',
    'MDR-TH' : 'mdr-thueringen.de',
    'PULS8' : 'plus-acht.de',
    'FLN' : 'fine-living-network.com',
    'FR24F' : 'france24.fr',
    'FR24E' : 'france24.com',
    'MDR-ST' : 'mdr-sachsen-anhalt.de',
    'WDR-W' : 'wdr-wuppertal.de',
    'AMS' : 'Auto Motor Sport',
    'WDR-BN' : 'wdr-bonn.de',
    'WDR-BI' : 'wdr-bielefeld.de',
    'FOOD' : 'foodnetwork.com',
    'WDR-K' : 'wdr-koeln.de',
    'TRCH' : 'travelchannel.de',
    'WDR-E' : 'wdr-essen.de',
    'WDR-D' : 'wdr-duesseldorf.de',
    'CH21' : 'channel21.de',
    'RNF' : 'rhein-neckar-fernsehen.de',
    'WDR-SI' : 'wdr-siegen.de',
    'RMTV' : 'rheinmain-tv',
    'CNBC' : 'cnbc.com',
    'QVCBS' : 'qvcbeauty.qvc.de',
    'WDR-AC' : 'wdr-aachen.de',
    'RBB-B' : 'rbb-berlin.de',
    'DMF' : 'Deutsches Musik Fernsehen',
    'MDR-SN' : 'mdr-sachsen.de',
    'NDR-HH' : 'ndr-hh.de',
    'NICKJ' : 'Nick Jr.',
    'SR' : 'sr.de',
    'FFTV' : 'Fix &amp; Foxi',
    'LEITV' : 'leipzig-fernsehen.de',
    'RBB-BB' : 'rbb-brandenburg.de',
    'REGBS' : 'regio-tv-bodensee.de',
    'NRWTV' : 'nrw-tv.de',
    'NDR-NI' : 'ndr-ni.de',
    'QVCP' : 'qvc-plus.de',
    'MAPO' : 'marcopolo.de',
    '123TV': '123.tv',
    'CRIN': 'CRIME + INVESTIGATION',
    'DAZN': 'DAZN',
    'HEALTH': 'Health TV',
    'K1DOKU': 'kabel eins Doku',
    'MDR': 'MDR',
    'N24DOKU': 'N24 Doku',
    'N3': 'NDR',
    'RTLPL': 'RTLplus',
    'SKYCS': 'Sky Cinema Special HD',
    'SKYTH': 'Sky Cinema Thriller',
    'SKY-CO': 'Sky Comedy',
    'SKY-CR': 'Sky Crime',
    'SKY-F': 'Sky Family',
    'SKY1': 'Sky One',
    'SKYF1': 'Sky Sport F1',
    'SWR': 'SWR/SR',
    'TNT-C': 'TNT Comedy',
    'TOGGO': 'TOGGO plus',
    'VOXUP': 'VOXup',
    'WDR': 'WDR',
    'WELT': 'WELT'
}


def get_channel_key(value):
    for name, val in channel_map.items():
        if val == value:
            return name


def write_controlfile(grab_time, grab_days):
    print('Writing Controlfile [{0}, {1}, {2}]'.format(control_file, grab_time, grab_days))
    sorted_x = sorted(channel_map.values(), key=operator.itemgetter(1))
    try:
        # Delete first because user have no permission to change attrib from files other users own
        if os.path.exists(control_file):
            os.remove(control_file)
        f = open(control_file, "w")
        # Set filemode for every written file!
        os.fchmod(f.fileno(), file_mode)
        f.write('file;{0};0;1\n'.format(grab_time))
        f.write('{0}\n'.format(grab_days))
        for key in combination_channels:
            f.write(key)
            f.write('\n')
        for val in sorted_x:
            f.write(val)
            f.write('\n')

    finally:
        f.close()


def checkchannelids():
    # Go to http://www.vdr-wiki.de/wiki/index.php/Xmltv2vdr-plugin
    # and safe the "Verbindliche EPG-Senderliste" to an text file
    # called "channelids.txt".
    try:
        print('Reading "channelids.txt"')
        f = open("channelids.txt", "U")
        channelids = f.read().split(os.linesep)
        f.close()
        channelids = filter(lambda x: len(x) > 0, channelids)

        print("The following channels are NOT in the official list:")

        for name, val in channel_map.items():
            if val not in channelids:
                print("%s" % val)

        for val in combination_channels.keys():
            if val not in channelids:
                print("%s" % val)
    except IOError as e:
        logger.log(e, logger.ERROR)


def checkchannelmap():
    r = requests.get('https://live.tvspielfilm.de/static/content/channel-list/livetv',
                     headers={'Connection': 'close', 'User-Agent': '4.2 (Nexus 10; Android 6.0.1; de_DE)', 'Accept-Encoding' : 'gzip, deflate'})
    r.encoding = 'utf-8'
    data = r.json()
    tvsp_ids = {}
    for val in data:
        tvsp_ids[val['id']] = val['name']

    channelids = filter(lambda x: len(x) > 0, tvsp_ids)

    print("The following channels included in the channel map are NOT provided by the server:")
    for name, val in channel_map.items():
        if name not in channelids:
            print("%s : %s," % (name, val) )

    print("\n")

    channelids = filter(lambda x: len(x) > 0, channel_map)

    print("The following channels are NOT in the current channel map:")
    for name, val in tvsp_ids.items():
        if name not in channelids:
            print('"%s" : "%s",' % (name, val) )

