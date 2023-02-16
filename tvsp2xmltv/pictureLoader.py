#!/data/data/com.termux/files/usr/bin/python2
# -*- coding: utf-8 -*-
import requests
import glob
from io import open
from os import path, remove, fchmod
from urlparse import urlsplit
from . import defaults
from . import logger
from xml.etree.ElementTree import Element

new_file_list = []


def cleanup_images():
    if defaults.remove_orphaned_images:
        files_in_dir = glob.glob(path.abspath(path.join(defaults.epgimages_dir, '*.jpg')))
        orphaned_files = list(set(files_in_dir) ^ set(new_file_list))
        for f in orphaned_files:
            logger.log("removing orphaned file: {0}".format(f), logger.DEBUG)
            remove(f)


class PictureLoader(object):
    def __init__(self, programme):
        self.programme = programme

    def get_xml(self):
        icons = []
        if self.programme.images:
            if len(self.programme.images) > 0:
                i = 0
                for im in sorted(self.programme.images):
                    i += 1
                    f = self.__download_image(im['size{0}'.format(defaults.size_of_images)], defaults.epgimages_dir)
                    if f:
                        icon = Element('icon', {'src': f})
                        icons.append(icon)
                    if i >= defaults.number_of_images_per_show:
                        break

        return icons

    def __download_image(self, file_url, file_dir):
        suffix_list = ['jpg', 'gif', 'png']
        file_name = urlsplit(file_url)[2].split('/')[-1]
        file_suffix = file_name.split('.')[1]
        full_file_path = path.abspath(path.join(file_dir, file_name))
        #check if file exists before downloading it again
        if path.exists(full_file_path):
            logger.log("file already exists: {0}".format(full_file_path), logger.DEBUG)
        else:
            i = requests.get(file_url)
            if file_suffix in suffix_list and i.status_code == requests.codes.ok:
                with open(full_file_path, 'wb') as f:
                    fchmod(f.fileno(), defaults.file_mode)
                    f.write(i.content)
                    logger.log("new file downloaded: {0}".format(full_file_path), logger.DEBUG)
            else:
                return False

        # remember the File
        new_file_list.append(full_file_path)
        return 'file://' + full_file_path
