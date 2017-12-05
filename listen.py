#!/usr/bin/python

# This is a heavily modified version of the snippet on:
# http://askubuntu.com/questions/138522/how-do-i-run-a-script-when-a-bluetooth-device-connects

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import gr8w8upd8m8
import subprocess
import sys
import time

DEVICE="00:23:CC:23:8A:55"

# bluetooth is incredibly flaky, so restart it all the time
print "Stopping bluetooth..."
subprocess.check_output(["service", "bluetooth", "stop"])
time.sleep(2)
print "Starting bluetooth..."
subprocess.check_output(["service", "bluetooth", "start"])
time.sleep(2)

dbus_loop = DBusGMainLoop()
bus = dbus.SystemBus(mainloop=dbus_loop)
loop = gobject.MainLoop()

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

def cb(prop, val, iface=None, mbr=None, path=None):
    print "Called for %s=%s (%s, %s, %s)" % (prop, val, iface, mbr, path)
    if prop == 'Connected' and val == True:
        print 'Device connected.'
        print 'iface: %s' % iface
        print 'mbr: %s' % mbr
        print 'path: %s' % path
        print "\n"
        gr8w8upd8m8.main(["bin", DEVICE])
        print "\n"
        print "assuming disconnected"
        print "\n"
        loop.quit()

device.connect_to_signal("PropertyChanged", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')
device.connect_to_signal("Connected", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')
device.connect_to_signal("Disconnected", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')

if connected:
  gr8w8upd8m8.main(["bin", DEVICE])

#notify = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
#method = notify.get_dbus_method('Notify', 'org.freedesktop.Notifications')
#method("wakeup", 1234, "", "The time is", "9PM", [], [], 1)
#device.connect_to_signal("wakeup", cb)

loop.run()
