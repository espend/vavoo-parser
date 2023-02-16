#!/data/data/com.termux/files/usr/bin/python2
# encoding: utf-8
'''
setup -- shortdesc

setup is a description

It defines classes_and_methods

@author:     chris
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import traceback

# Root path
base_path = os.path.realpath(__file__)

# Insert local directories into path
sys.path.append(os.path.join(base_path))

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from tvsp2xmltv import logger
from tvsp2xmltv import defaults
from tvsp2xmltv import tvsGrabber

__all__ = []
__version__ = '0.1.0'
__date__ = '2016-04-01'
__updated__ = '2016-04-01'

DEBUG = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by chris on %s.
  Copyright 2013 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-c", "--controlfile", dest="cfile", action='store_true', help="create the controlfile")
        parser.add_argument("-t", "--time", dest="time", default="00:00", help="The time for the control file")
        parser.add_argument("-d", "--days", dest="days", default="14", help="numberof days for the control file")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="option", help="options from xmltv2vdr call [default: %(default)s]", metavar="option",
                            nargs='*')
        parser.add_argument('-l', '--checkchannels', action='store_true', help='Go to http://www.vdr-wiki.de/wiki/index.php/Xmltv2vdr-plugin and safe the "Verbindliche EPG-Senderliste" to an text file called "channelids.txt"')
        parser.add_argument('-m', '--checkchannelmap', action='store_true', help='Show the diff between channel map and server.')

        # Process arguments
        args = parser.parse_args()

        argvline = ""
        for a in sys.argv:
            argvline += a
            argvline += " "

        logger.log('Called with following arguments: "' + argvline + '"', logger.DEBUG)

        option = args.option
        cfile = args.cfile

        if args.checkchannels:
            defaults.checkchannelids()

        if args.checkchannelmap:
            defaults.checkchannelmap()

        if cfile:
            defaults.write_controlfile(args.time, args.days)

        if option:
            logger.log('Prepare grabbing...')
            grabber = tvsGrabber.TvsGrabber()
            #<days> ‘‘ [<pictures>] ard.de zdf.de
            grabber.grab_days = int(option.pop(0))
            option.pop(0) # We do not use an PIN
            if option[0] == '1':
                grabber.pictures = True
                option.pop(0)
            elif option[0] == '0':
                grabber.pictures = False
                option.pop(0)

            grabber.add_channel(option)

            logger.log('Start grabbing...')
            grabber.start_grab()
            logger.log('Saving xml...')
            grabber.save()
            logger.log('End of grabbing...')

        return 0
    except Exception as e:
        logger.log("{0}:\n{1}\n{2}".format(program_name, repr(e), traceback.format_exc()), logger.ERROR)
        return 2


if __name__ == "__main__":
    if DEBUG:
        #sys.argv.append("-m")
        #sys.argv.append("1 '' 0 ard.de zdf.de")
        pass
    sys.exit(main())
