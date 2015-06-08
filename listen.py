#!/usr/bin/python

# This is a heavily modified version of the snippet on:
# http://askubuntu.com/questions/138522/how-do-i-run-a-script-when-a-bluetooth-device-connects

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import gr8w8upd8m8

import subprocess

# ID of the device we care about
DEV_ID = '00_23_CC_23_8A_55'

dbus_loop = DBusGMainLoop()
bus = dbus.SystemBus(mainloop=dbus_loop)

# Figure out the path to the headset
manager = bus.get_object('org.bluez', '/')
manager = dbus.Interface(manager, 'org.bluez.Manager')
adapterPath = manager.DefaultAdapter()
print "adapter:", adapterPath

adapter = bus.get_object('org.bluez', adapterPath)
adapter = dbus.Interface(adapter, 'org.bluez.Adapter')
devices = adapter.ListDevices()
print "devices:", devices

devicePath = str(devices[0])
print "device:", devicePath
device = bus.get_object('org.bluez', devicePath)
device = dbus.Interface(device, 'org.bluez.Device')

connected =  bool(device.GetProperties()['Connected'])
print "connected:", connected

#headset = bus.get_object('org.bluez', adapterPath + '/dev_' + DEV_ID)
    # ^^^ I'm not sure if that's kosher. But it works.

def cb(prop, val, iface=None, mbr=None, path=None):
    if prop == 'Connected' and val == True:
        print 'Device connected.'
        print 'iface: %s' % iface
        print 'mbr: %s' % mbr
        print 'path: %s' % path
        print "\n"
        gr8w8upd8m8.main(["bin", "00:23:CC:23:8A:55"])
        print "\n"
        print "assuming disconnected"
        print "\n"

device.connect_to_signal("PropertyChanged", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')
#headset.connect_to_signal("Connected", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')
#headset.connect_to_signal("Disconnected", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')

loop = gobject.MainLoop()
loop.run()
