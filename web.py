#!/usr/bin/env python

import webkit, os
import pygtk
pygtk.require('2.0')
import gtk
#import sys
import subprocess

radiostations = {#name:(address,homepage),
    #These are the default stations. More stations can be added via
    #configuration files located at ~/.radiopy and /etc/radiopy.conf
    'P1'     :('http://sverigesradio.se/topsy/direkt/132-hi.mp3','http://sverigesradio.se/'),
    'P3'     :('http://sverigesradio.se/topsy/direkt/164-hi.mp3','http://sverigesradio.se/'),
    'Ekot'   :('http://sverigesradio.se/api/radio/radio.aspx?type=latestbroadcast&id=4540&codingformat=.m4a&metafile=asx','http://sverigesradio.se/'),
    'Studio1':('http://sverigesradio.se/api/radio/radio.aspx?type=latestbroadcast&id=1637&codingformat=.m4a&metafile=asx','http://sverigesradio.se/')
    }

pid = 0

def startChannel(station):
    #check if we need the '-playlist' argument for mplayer
    playlist=''
    if (radiostations[station][0][-4:] in ('=asx','.asx','.ram','.m3u')) or \
        (station[0:7]=='radioIO') or \
	(station[0:10] == 'Classic FM'):
        playlist='-playlist'

    execargs=['mplayer', '-softvol', '-cache', str(128), playlist, radiostations[station][0] ]

    print execargs
    
    global pid
    if pid > 0:
        os.kill(pid, 15) # 15 = SIGTERM
        pid = 0
    else:
        pid = subprocess.Popen(execargs).pid

        
def pbVolUp(widget, data=None):
    os.system("./volu.sh")

def pbVolDown(widget, data=None):
    os.system("./vold.sh")
    
def pbRadioMenu(widget=None, data=None):

    global radioMenuActive
    global powerMenuActive
    global contentBox
        
    if radioMenuActive:
        print("hiding radioMenu")
        radioMenu.hide()
        webTop.show()
        radioMenuActive = False
        contentBox.set_resize_mode(gtk.RESIZE_PARENT)
        win.resize(800, 480)

    else:
        print("showing radioMenu")
        radioMenu.show()
        powerMenu.hide()
        webTop.hide()
        radioMenuActive = True
        powerMenuActive = False
        contentBox.set_resize_mode(gtk.RESIZE_PARENT)
        win.resize(800, 480)

def pbPowerMenu(widget, data=None):
    global powerMenuActive
    global radioMenuActive
    global contentBox
        
    if powerMenuActive:
        print("hiding powerMenu")

        powerMenu.hide()
        webTop.show()
        powerMenuActive = False
        contentBox.set_resize_mode(gtk.RESIZE_PARENT)
        win.resize(800, 480)

    else:
        print("showing powerMenu")
        powerMenu.show()
        radioMenu.hide()
        webTop.hide()
        radioMenuActive = False
        powerMenuActive = True 
        contentBox.set_resize_mode(gtk.RESIZE_PARENT)
        win.resize(800, 480)


def pbP1(widget, data=None):
    startChannel("P1")
    
def pbP3(widget, data=None):
    startChannel("P3")
    
def pbEkot(widget, data=None):
    startChannel("Ekot")
    
def pbStudio1(widget, data=None):
    startChannel("Studio1")

def pbToday(widget, data=None):
    global webBottom
    webBottom.open("http://privat.yoakim.com/powerlog/day_acc_tiny.html")

def pbdynHist(widget, data=None):
    webBottom.open("http://privat.yoakim.com/powerlog/int.html")
    
def pbTable(widget, data=None):
    webBottom.open("http://privat.yoakim.com/powerlog/table.html")
     

        
def createMenu(title, spacing, layout):
    frame = gtk.Frame()

    bbox = gtk.VButtonBox()
    bbox.set_border_width(0)
    frame.add(bbox)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)

#    btnVolUp = gtk.Button("Up")
#    btnVolUp.connect("clicked", pbVolUp)

    ebVolu = gtk.EventBox()
    ebVolu.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebVolu.connect("button_press_event", pbVolUp)
    imVolu = gtk.Image()
    imVolu.set_from_file("buttons/volu.png")
    ebVolu.add(imVolu)

    ebVold = gtk.EventBox()
    ebVold.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebVold.connect("button_press_event", pbVolDown)
    imVold = gtk.Image()
    imVold.set_from_file("buttons/vold.png")
    ebVold.add(imVold)
    
    
#    btnP1 = gtk.Button("P1")
#    btnP1.connect("clicked", pbRadioP1)

    ebRadio = gtk.EventBox()
    ebRadio.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebRadio.connect("button_press_event", pbRadioMenu)
    imRadio = gtk.Image()
    imRadio.set_from_file("buttons/radio.png")
    ebRadio.add(imRadio)

    ebPower = gtk.EventBox()
    ebPower.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebPower.connect("button_press_event", pbPowerMenu)
    imPower = gtk.Image()
    imPower.set_from_file("buttons/powerlog.png")
    ebPower.add(imPower)

    bbox.add(ebVolu)
    bbox.add(ebRadio)
    bbox.add(ebPower)
    bbox.add(ebVold)
    
    return frame

def createRadioMenu(title, spacing, layout):
    frame = gtk.Frame()

    bbox = gtk.HButtonBox()
    bbox.set_border_width(0)
    frame.add(bbox)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)

    ebP1 = gtk.EventBox()
    ebP1.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebP1.connect("button_press_event", pbP1)
    imP1 = gtk.Image()
    imP1.set_from_file("buttons/p1.png")
    ebP1.add(imP1)

    ebP3 = gtk.EventBox()
    ebP3.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebP3.connect("button_press_event", pbP3)
    imP3 = gtk.Image()
    imP3.set_from_file("buttons/p3.png")
    ebP3.add(imP3)

    ebEkot = gtk.EventBox()
    ebEkot.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebEkot.connect("button_press_event", pbEkot)
    imEkot = gtk.Image()
    imEkot.set_from_file("buttons/ekot.png")
    ebEkot.add(imEkot)

    ebStudio1 = gtk.EventBox()
    ebStudio1.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebStudio1.connect("button_press_event", pbStudio1)
    imStudio1 = gtk.Image()
    imStudio1.set_from_file("buttons/studio1.png")
    ebStudio1.add(imStudio1)

    bbox.add(ebP1)
    bbox.add(ebP3)
    bbox.add(ebEkot)
    bbox.add(ebStudio1)

    return frame

def createPowerMenu(title, spacing, layout):
    frame = gtk.Frame()

    bbox = gtk.HButtonBox()
    bbox.set_border_width(0)
    frame.add(bbox)
    bbox.set_layout(layout)
    bbox.set_spacing(spacing)

    ebToday = gtk.EventBox()
    ebToday.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebToday.connect("button_press_event", pbToday)
    imToday = gtk.Image()
    imToday.set_from_file("buttons/powerlog.png")
    ebToday.add(imToday)

    ebdynHist = gtk.EventBox()
    ebdynHist.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebdynHist.connect("button_press_event", pbdynHist)
    imdynHist = gtk.Image()
    imdynHist.set_from_file("buttons/powerlog.png")
    ebdynHist.add(imdynHist)

    ebTable = gtk.EventBox()
    ebTable.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ebTable.connect("button_press_event", pbTable)
    imTable = gtk.Image()
    imTable.set_from_file("buttons/powerlog.png")
    ebTable.add(imTable)

    ## ebStudio1 = gtk.EventBox()
    ## ebStudio1.set_events(gtk.gdk.BUTTON_PRESS_MASK)
    ## ebStudio1.connect("button_press_event", pbStudio1)
    ## imStudio1 = gtk.Image()
    ## imStudio1.set_from_file("buttons/studio1.png")
    ## ebStudio1.add(imStudio1)

    bbox.add(ebToday)
    bbox.add(ebdynHist)
    bbox.add(ebTable)
    #bbox.add(ebStudio1)

    return frame


os.chdir("/home/pi/python")
#os.chdir("/home/joakim/jojoc/python")
win = gtk.Window()
win.connect('destroy', lambda w: gtk.main_quit())

mainBox = gtk.HBox(False, 0)
win.add(mainBox)

mainBox.pack_start(createMenu("", 0, gtk.BUTTONBOX_SPREAD), True, True, 0)

#frameMenu = gtk.Frame("V")
#mainBox.pack_start(frameMenu, True, True, 0)

#hbox = gtk.HBox(False, 0)
#hbox.set_border_width(10)
#frameMenu.add(hbox)

#win.add(hbox)

contentBox = gtk.VBox(False, 0)
mainBox.pack_start(contentBox, True, True, 0)


webTop = webkit.WebView()
webBottom = webkit.WebView()
#web.open("http://privat.yoakim.com/powerlog/padda.html")
webTop.open("http://privat.yoakim.com/powerlog/pow_tiny.html")
webBottom.open("http://privat.yoakim.com/powerlog/day_tiny.html")

#global radioMenu
radioMenu = createRadioMenu("", 0, gtk.BUTTONBOX_SPREAD)
radioMenuActive = False

powerMenu = createPowerMenu("", 0, gtk.BUTTONBOX_SPREAD)
powerMenuActive = False

contentBox.pack_start(radioMenu, False, True, 0)
contentBox.pack_start(powerMenu, False, True, 0)
contentBox.pack_start(webTop, False, True, 0)
contentBox.pack_start(webBottom, False, True, 0)

#contentBox.remove(webBottom)
#radioMenuActive = True

#pbRadioMenu()

win.fullscreen()
win.resize(800, 480)
win.show_all()
gtk.Window.fullscreen
radioMenu.hide()
powerMenu.hide()

#pbRadioMenu()
gtk.main()
