#!/usr/bin/python
# vim:ts=4 expandtab:
"""
radio.py 0.5

A script that makes it easy to listen to online radio via mplayer
"""


###########################################################################
 #   Copyright (C) 2007-2008 by Guy Rutenberg                              #
 #   guyrutenberg@gmail.com                                                #
 #                                                                         #
 #   This program is free software; you can redistribute it and/or modify  #
 #   it under the terms of the GNU General Public License as published by  #
 #   the Free Software Foundation; either version 2 of the License, or     #
 #   (at your option) any later version.                                   #
 #                                                                         #
 #   This program is distributed in the hope that it will be useful,       #
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
 #   GNU General Public License for more details.                          #
 #                                                                         #
 #   You should have received a copy of the GNU General Public License     #
 #   along with this program; if not, write to the                         #
 #   Free Software Foundation, Inc.,                                       #
 #   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import sys
import os
import subprocess
import time
from optparse import OptionParser
import ConfigParser
import tempfile
import random
import threading

radiostations = {#name:(address,homepage),
    #These are the default stations. More stations can be added via
    #configuration files located at ~/.radiopy and /etc/radiopy.conf
    'Galgalatz':('http://gifs.msn.co.il/media/gglz.asx','http://glz.msn.co.il/'),
    'Radio Tel Aviv':('mms://s35wm.castup.net/992120001-52.wmv','http://www.102fm.co.il/'),
    'Galatz':('http://gifs.msn.co.il/media/glz.asx','http://glz.msn.co.il/'),
    'Reshet Bet':('mms://s35wm.castup.net/990310001-52.wmv','http://bet.iba.org.il/'),
    'Reshet Gimel':('mms://s36wm.castup.net/990310004-52.wmv','http://bet.iba.org.il/'),
    '88fm':('mms://s35wm.castup.net/990310006-52.wmv','http://88fm.iba.org.il/'),
    'BBC World Service':('http://www.bbc.co.uk/worldservice/meta/tx/nb/live_news_au_nb.ram','http://www.bbc.co.uk/worldservice/'),
    'BBC1':('http://www.bbc.co.uk/radio1/realaudio/media/r1live.ram','http://www.bbc.co.uk/radio1/'),
    'BBC2':('http://www.bbc.co.uk/radio2/realmedia/fmg2.ram','http://www.bbc.co.uk/radio2/'),
    'BBC3':('http://www.bbc.co.uk/radio3/ram/r3g2.ram','http://www.bbc.co.uk/radio3/'),
    'BBC4':('http://www.bbc.co.uk/radio4/realplayer/media/fmg2.ram','http://www.bbc.co.uk/radio4/'),
    'BBC5':('http://www.bbc.co.uk/fivelive/live/surestream_int.ram','http://www.bbc.co.uk/fivelive/'),
    'Classic FM':('http://mediaweb.musicradio.com/Playlist.asx?StreamID=2', 'http://www.classicfm.co.uk/'),
    'KING-FM':('http://www.king.org/kingfm.asx','http://www.king.org/'),
    'CNN':('http://www.cnn.com/audio/radio/liveaudio.asx','http://www.cnn.com/'),
    '103fm':('http://live.103.fm/103fm-high/','http://www.103.fm/'),
    'Radius':('http://s34wm.castup.net/993820002-52.wmv','http://www.100fm.co.il/'),

    'radioIO 70s Rock':('http://streampoint.radioio.com/streams/6','http://www.radioio.com/'),
    'radioIO 70s Pop':('http://streampoint.radioio.com/streams/24','http://www.radioio.com/'),
    'radioIO 80s New Wave':('http://streampoint.radioio.com/streams/42','http://www.radioio.com/'),
    'radioIO 80s Pop':('http://streampoint.radioio.com/streams/60','http://www.radioio.com/'),
    'radioIO Acoustic Cafe':('http://streampoint.radioio.com/streams/96','http://www.radioio.com/'),
    'radioIO Ambient':('http://streampoint.radioio.com/streams/114','http://www.radioio.com/'),
    'radioIO Chill':('http://streampoint.radioio.com/streams/132','http://www.radioio.com/'),
    'radioIO Classical':('http://streampoint.radioio.com/streams/150','http://www.radioio.com/'),
    'radioIO Alt Country':('http://streampoint.radioio.com/streams/168','http://www.radioio.com/'),
    'radioIO Dead':('http://streampoint.radioio.com/streams/186','http://www.radioio.com/'),
    'radioIO Disco Hits':('http://streampoint.radioio.com/streams/205','http://www.radioio.com/'),
    'radioIO Eclectic':('http://streampoint.radioio.com/streams/223','http://www.radioio.com/'),
    'radioIO Alternative Rock':('http://streampoint.radioio.com/streams/241','http://www.radioio.com/'),
    'radioIO History Of Rock':('http://streampoint.radioio.com/streams/259','http://www.radioio.com/'),
    'radioIO Jam Bands':('http://streampoint.radioio.com/streams/277','http://www.radioio.com/'),
    'radioIO Real Jazz':('http://streampoint.radioio.com/streams/295','http://www.radioio.com/'),
    'radioIO Todays Pop':('http://streampoint.radioio.com/streams/313','http://www.radioio.com/'),
    'radioIO Todays Rock':('http://streampoint.radioio.com/streams/331','http://www.radioio.com/'),
    'radioIO Idols':('http://streampoint.radioio.com/streams/620','http://www.radioio.com/'),
    'radioIO Classic RnB':('http://streampoint.radioio.com/streams/566','http://www.radioio.com/'),
    'radioIO Classical Favorites':('http://streampoint.radioio.com/streams/638','http://www.radioio.com/'),
    'radioIO Classic Rock':('http://streampoint.radioio.com/streams/439','http://www.radioio.com/'),
    'radioIO Todays Country':('http://streampoint.radioio.com/streams/457','http://www.radioio.com/'),
    'radioIO Smooth Jazz':('http://streampoint.radioio.com/streams/475','http://www.radioio.com/'),
    'radioIO Guitar Heroes':('http://streampoint.radioio.com/streams/602','http://www.radioio.com/'),
    'radioIO Bluegrass':('http://streampoint.radioio.com/streams/548','http://www.radioio.com/'),
    'radioIO Dance Hits':('http://streampoint.radioio.com/streams/656','http://www.radioio.com/'),
    'radioIO Hairbands':('http://streampoint.radioio.com/streams/674','http://www.radioio.com/'),
    'radioIO Lovesongs':('http://streampoint.radioio.com/streams/692','http://www.radioio.com/'),
    'radioIO 90s Pop':('http://streampoint.radioio.com/streams/710','http://www.radioio.com/'),
    'radioIO Vocal Jazz':('http://streampoint.radioio.com/streams/728','http://www.radioio.com/'),
    'radioIO Blues':('http://streampoint.radioio.com/streams/746','http://www.radioio.com/'),
    'radioIO Indie Rock':('http://streampoint.radioio.com/streams/764','http://www.radioio.com/'),
    'radioIO Top 20 RnB Hits':('http://streampoint.radioio.com/streams/782','http://www.radioio.com/'),
    'radioIO Top 20 Hip Hop Hits':('http://streampoint.radioio.com/streams/800','http://www.radioio.com/'),
    'radioIO Top 20 Rock Hits':('http://streampoint.radioio.com/streams/818','http://www.radioio.com/'),
    'radioIO Top 20 Pop Hits':('http://streampoint.radioio.com/streams/836','http://www.radioio.com/'),
    'radioIO Top 20 Country Hits':('http://streampoint.radioio.com/streams/854','http://www.radioio.com/'),
    'radioIO Top 100 Classic Rock Hits':('http://streampoint.radioio.com/streams/872','http://www.radioio.com/'),
    'radioIO Shuffle':('http://streampoint.radioio.com/streams/890','http://www.radioio.com/'),
    'radioIO 90s Rock':('http://streampoint.radioio.com/streams/908','http://www.radioio.com/'),
    'radioIO 80s Rock':('http://streampoint.radioio.com/streams/926','http://www.radioio.com/'),
    'radioIO Alt Rock Classics':('http://streampoint.radioio.com/streams/944','http://www.radioio.com/'),
    'radioIO Standards':('http://streampoint.radioio.com/streams/962','http://www.radioio.com/'),
    'radioIO NuSoul':('http://streampoint.radioio.com/streams/980','http://www.radioio.com/'),
    'radioIO Pop Mix':('http://streampoint.radioio.com/streams/998','http://www.radioio.com/'),
    'radioIO RnB Mix':('http://streampoint.radioio.com/streams/1016','http://www.radioio.com/'),
    'radioIO Rock Mix':('http://streampoint.radioio.com/streams/1034','http://www.radioio.com/'),
    'radioIO Rock Mix':('http://streampoint.radioio.com/streams/1034','http://www.radioio.com/'),
    'radioIO Newgrass':('http://streampoint.radioio.com/streams/1052','http://www.radioio.com/'),
    'radioIO Country Mix':('http://streampoint.radioio.com/streams/1070','http://www.radioio.com/'),
    'radioIO Classic Acoustic Rock':('http://streampoint.radioio.com/streams/1088','http://www.radioio.com/'),
    'radioIO Folk':('http://streampoint.radioio.com/streams/1106','http://www.radioio.com/'),
    'radioIO Big Band':('http://streampoint.radioio.com/streams/1124','http://www.radioio.com/'),
    'radioIO Classic Country':('http://streampoint.radioio.com/streams/1142','http://www.radioio.com/'),
    'radioIO Progressive Rock':('http://streampoint.radioio.com/streams/1160','http://www.radioio.com/'),
    'radioIO Classic Hip Hop':('http://streampoint.radioio.com/streams/1178','http://www.radioio.com/'),
    'radioIO Women In Rock':('http://streampoint.radioio.com/streams/1196','http://www.radioio.com/'),
    'radioIO Roots of Rock':('http://streampoint.radioio.com/streams/1214','http://www.radioio.com/'),
    'radioIO Todays RnB':('http://streampoint.radioio.com/streams/1232','http://www.radioio.com/'),

    'Radio Paradise':('http://www.radioparadise.com/musiclinks/rp_128aac.m3u','http://www.radioparadise.com'),
    'Onda Cero':('mms://a562.l507241195.c5072.e.lm.akamaistream.net/d/562/5072/v0001/reflector:41195','http://www.ondacero.es'),
    'Beethoven':('http://www.beethoven.com/beethoven_ad.asx','http://www.beethoven.com/'),
    'Ram FM':('http://uberant-web.antfarm.co.za/clients/ramfm/ramfm.asx','http://www.ramfm.net/'),
    'Radio Caroline':('http://lazygit.org/listen.asx','http://www.radiocaroline.co.uk/'),
    }

def parseArguments():
    version="%prog 0.5\nCopyright (C) 2007-2008 Guy Rutenberg\nhttp://www.guyrutenberg.com/category/projects/radiopy/"
    parser = OptionParser(usage="%prog [options] station", 
                        version=version)
    parser.add_option("-s", "--sleep", dest="sleep", type="int", default=0,
                    help="go to sleep after MIN minutes", metavar="MIN")
    parser.add_option("-w", "--wake-up", dest="wake", type="int", default=0,
                    help="wake up and start playing after MIN minutes", metavar="MIN")
    parser.add_option("-l", "--list", dest="list", action="store_true", default=False,
                    help="show a list of known radio stations and their homepage")
    parser.add_option("-c", "--cache", dest="cache", type="int", default=128,
                    help="set the size of the cache in KBytes [default: %default]", metavar="SIZE")
    parser.add_option("-r", "--record", dest="record", type="string",
                    help="record the stream as mp3 and save it to FILE", metavar="FILE")
    
    return parser.parse_args()

def main(options, args):
    readRadioStations(radiostations,os.path.expanduser("~/.radiopy"))
    readRadioStations(radiostations,"/etc/radiopy.conf")
    
    if options.list:
        showStations()
        return 0
    
    if len(args)<1:
        print "you need to supply a station name"
        showStations()
        return 1
    
    req_station = ""
    for arg in args:
        req_station += arg + " "
    #delete the last appended space
    req_station = req_station[0:-1]
    try:
        radiostations[req_station]
    except KeyError:
        print "Didn't recognized this station name:",req_station
        print "See 'radio.py --list' for a list of recognized station names."
        return 1
    
    if options.wake > 0:
        print "Radio will wake up in", options.wake, "minutes"
        time.sleep(60*options.wake)
    
    if options.cache > 32: #mplayer requires cache>=32
        cache = str(options.cache)
    else: cache = str(32)
    
    #check if we need the '-playlist' argument for mplayer
    playlist=''
    if (radiostations[req_station][0][-4:] in ('.asx','.ram','.m3u')) or \
        (req_station[0:7]=='radioIO') or \
	(req_station[0:10] == 'Classic FM'):
        playlist='-playlist'

    #handle the record flag
    if options.record is not None:
        while(1):
            try:
                named_pipe = tempfile.gettempdir()+'/radiopy'+str(random.randint(0,1000000))
                os.mkfifo(named_pipe)
                break
            except OSError:
                continue
        record = ['-ao','pcm:file='+named_pipe,'-vc','null','-vo','null']
    else :
        record = []
    
    execargs=['mplayer', '-softvol', '-cache', cache, playlist, radiostations[req_station][0] ] + record

    # save the process id of the mplayer
    pid = None

    if options.sleep > 0:
        print "Radio will go to sleep in", options.sleep, "minutes"
        pid = subprocess.Popen(execargs).pid
        #time.sleep(60*options.sleep)
        def kill_mplayer():
            os.kill(pid, 15) # 15 = SIGTERM
        threading.Timer(60*options.sleep, kill_mplayer).start()
    elif options.record is None:
        os.execvp(execargs[0],execargs)

    if options.record is not None:
        if pid is None: pid = subprocess.Popen(execargs).pid
        lame_args = ['lame']
        lame_args += ['--tt',req_station]
        lame_args += ['--tc',"Stream recorded by radio.py"]
        #lame_args += ['-V2'] # record using VBR
        lame_args += [named_pipe, options.record]
        try:
            subprocess.call(lame_args)
        except KeyboardInterrupt:
            None
        os.unlink(named_pipe)

def showStations():
    keys = radiostations.keys()
    keys.sort()
    
    maxlen = 0 # find the longest station name
    for key in keys:
        if len(key) > maxlen: maxlen = len(key) 
    for key in keys:
        print key.ljust(maxlen+1), radiostations[key][1]

    print "Total:", len(radiostations), "recognized stations"

def readRadioStations(radiostations,file):
    try:
        config = ConfigParser.RawConfigParser()
        config.read(file)
        for section in config.sections():
            for option in config.options(section):
                radiostations[section] = (config.get(section, 'stream') , config.get(section, 'home'))
    except ConfigParser.ParsingError:
        print "Error reading", file
        return 1


if __name__== '__main__':
    (options, args) = parseArguments()
    sys.exit(main(options, args))
