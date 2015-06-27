# Blobbin

How to set up a Wii Fit with a Raspberry Pi to record your weight to the web. I am using a CanaKit: http://www.canakit.com/raspberry-pi-starter-kit.html

1. Set up raspbian.
2. Set up WiFi. 
3. `sudo apt-get update && sudo apt-get upgrade`
4. `sudo apt-get install bluez bluez-tools python-bluez python-gobject wminput`

## Set up the hardware with bluetooth.

This hack is based on the instructions at http://www.stavros.io/posts/your-weight-online/ I've added some Raspberry Pi specific build details. Also, this is updated to account for some minor changes to bluez. The gist is that you have to temporary replace your bluetooth stack with a version that's hacked up to send the correct keycode.

1. Use `sudo bluez-test-discovery` or `hcitool scan` to get the address of the Wii Fit.
2. Uninstall bluez with `sudo apt-get remove bluez` (or you can use dpkg -r).
3. `sudo apt-get install build-essential libdbus-1-dev check checkinstall libglib2.0-dev libudev-dev`
4. `sudo nano /etc/apt/sources.list` and uncomment the deb-src line.
5. `sudo apt-get update`
6. `mkdir -p ~/src && cd ~/src && apt-get source bluez`
7. `cd bluez-*`
8. `./configure --enable-test --prefix=/ --exec_prefix=/usr`
9. Hand edit `pincode_cb` in `src/event.c` like this: https://gist.github.com/bklimt/9f7b290d0a664b7a3567
10. `make`
11. `sudo checkinstall --fstrans=no`
12. `sudo service bluetooth restart`
13. Press the red button on your Wii Fit, then `sudo ./test/simple-agent hci0 <your wii fit's address> && sudo wminput <your wii fit's address>`
14. For the pin, enter the numbers in **your bluetooth adapter's** (not the Wii Fit) address backwards with a dollar sign. For example, if your adapter's address is `00:1A:7D:DA:71:13`, use pin code `$1371da7d1a00`. If you aren't sure of your apapter's address, one was to find it is `ls /var/lib/bluetooth/`.
15. `sudo bt-device —set <your wii fit's address> Trusted 1`
16. `sudo dpkg -r bluez`
17. `sudo apt-get install bluez`
18. Wait 3 days. Yeah, I don't know. It didn't work for me, and then I came back 3 days later and everything worked.

## Get the python scripts and website code.

1. Set up git access to github. https://help.github.com/articles/generating-ssh-keys/
2. `mkdir -p ~/src && cd ~/src`
3. `git clone git@github.com:bklimt/blobbin.git`

## Set up the Parse app.

You can skip this step if you want to do something with the weights other than record them to the web. If so, you'll need to hack up the python scripts to do whatever you want them to do.

1. Create an app on parse.com.
2. Secure it by disabling client class creation, making a Weight class, adding a weight number field and a person string field to it, and making the class readonly.
3. Download the parse cli.
4. `cd ~/src/blobbin/`
5. `parse new` to set the keys for the Parse app you want to deploy to.
6. `cd ./parse`
7. `parse deploy`

## Configure the python script to listen.

1. `cd ~/src/blobbin/parse`
2. Edit the `DEVICE` variable in `listen.py` to use the address of your Wii Fit. 
3. Change the logic in `storage.py` to do whatever you want with the weights.
4. Create the config for accessing Parse.

        $ cat >~/src/blobbin/config.py
        appId = "<Your App Id>"
        masterKey = "<Your Master Key>"
        ^D

5. `sudo python listen.py`


