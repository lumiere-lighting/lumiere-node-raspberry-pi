# Lumière Raspberry Pi

[Lumiere](http://lumiere.lighting/).  Change holiday lights around the world.

Here you will find code and instructions on how to set up some Lumiere lights with a Raspberry Pi.  By default, it will talk with the main Lumiere application at [lumiere.lighting](http://lumiere.lighting), but you can also set up your own [Lumiere server](https://github.com/lumiere-lighting/lumiere-server).

## Ingredients

There are links to products at Adafruit as reference points; though Adafruit is awesome, there is no requirement to buy products from them.

### Device

* A [Raspberry Pi](http://www.raspberrypi.org/).  There are many different kits and extensions at  [Adafruit](http://www.adafruit.com/category/105).  Note that these instructions were tested on a Model B Raspberry Pi.
* (optional, but recommended) Raspberry Pi's come with a wired ethernet adapter, but more than likely you will want a wireless connection.  Try [this one](https://www.adafruit.com/product/814).

### Lights

* [Programmable LED strip (LPD8806 model)](http://www.adafruit.com/products/306).
    * These are preferred because other lights, like NeoPixels, are not actually compatible with Raspberry Pi.
    * Any length is fine, but note that 5 meters comes with a JST connection.  If there is not a JST connection, then soldering will be necessary to hook things up.
    * These lights require 5V; no more.  Depending on how many lights you have, you will need to have more power (still 5V).
    * It is recommended that you read [this tutorial](http://learn.adafruit.com/digital-led-strip/wiring) to know the intricacies of this LED strip.

### Other stuff

The following are recommendations on things that will help connect things up, but you may want to connect the lights your own way.

* [4 pin JST SM plug](http://www.adafruit.com/products/578) used to connect the LED strip to other wires.  If you have a LED strip with a JST end, this will make it easy to disconnect things.
* [5V 10A power supply](http://www.adafruit.com/products/658).  The above LED strip can only handle 5V so don't use more.
* [Female DC power adaptor](http://www.adafruit.com/products/368) used to connect the LED strip and Raspberry Pi to the power supply.  For those of us that don't know about these things that well, the `-` should be connected to ground and `+` to the 5V power.
* Some [prototyping wires](http://www.instructables.com/id/Protobloc-prototyping-wires/).
* [4 wire caps](http://en.wikipedia.org/wiki/Twist-on_wire_connector) to connect the JST strand wires to the prototype wires which are solid wires.
* [2 snap action wire blocks to split the power](http://www.adafruit.com/products/866).
* [Cobbler breakout](http://www.adafruit.com/products/914) this is used to connect the Raspberry Pi GPIO to the breadboard.  Note that the ribbon cable came connected but not in a way that was intuitive to me and I ended up breaking things, so double check that the breakout board is aligned correctly with the GPIO diagram.
* [Breadboard](http://www.adafruit.com/products/64).

## Setup

### Raspberry Pi setup

1. Setup your Raspberry Pi.  [Quick start guide](http://www.raspberrypi.org/help/quick-start-guide/).
1. (optional) Setup your wifi.
1. Enable SPI.
    * `sudo raspi-config`
    * Go to `Advanced options` and `enable SPI`.
1. Install python dev tools.
    1. `sudo apt-get install python-dev python-setuptools`
    1. `sudo easy_install pip`
1. Get code: `cd ~ && git clone https://github.com/lumiere-lighting/lumiere-node-raspberry-pi.git && cd lumiere-node-raspberry-pi`
1. Install Python packages: `sudo pip install -r requirements.txt`

*(coming soon) Download this Raspberry Pi image, burn it to a SD card and insert into your Raspberry Pi.*

### Connect lights

Given that you are using an external power source, and you probably should, this diagram shows how you want to hook up the lights to the GPIO pins on the Raspberry Pi.

![Raspberry Pi to LDP8806 diagram](https://raw.github.com/lumiere-lighting/lumiere-node-raspberry-pi/master/images/adafruit-raspberry-pi-ldp8806-diagram.png)

#### Example connection

Here is an example of a near final configuration using the parts listed above.

![Near-final project](https://raw.github.com/lumiere-lighting/lumiere-node-raspberry-pi/master/images/near-final.jpg)

## Running and configuration

This script needs to be run as a user that has root privileges as it needs access to the GPIO pins.  The default `pi` user will work fine.

### Config

To override some of the default config, use a `settings.json` file in the same directory as the `lumiere.py` file.  The defaults are the following:

    {
      "lights": 160,
      "api": "http://lumiere.lighting",
      "poll_interval": 6
    }

### Manual and testing

You can run manually with the following command:

1. `cd ~/lumiere-node-raspberry-pi && python lumiere.py`
1.  Once running, change the lights at [lumiere.lighting](http://lumiere.lighting), or whatever [Lumiere server](https://github.com/lumiere-lighting/lumiere-server) is appropriate.

### Auto start

This adds an `init.d` script so that the lumiere script is run automatically on start up and restarts if something goes wrong.

1. Link the script in to init.  (Update the location of the lumiere code as needed): `sudo cp /home/pi/lumiere-node-raspberry-pi/lumiere.init /etc/init.d/lumiere && sudo chmod +x /etc/init.d/lumiere`
1. Test with `sudo /etc/init.d/lumiere start`
1. Configure to get service to start on startup: `sudo update-rc.d /etc/init.d/lumiere defaults`
1. Restart the Pi: `sudo shutdown -r now`
    * It should start automatically, but you can control the process manually with: `sudo /etc/init.d/lumiere start|restart|status|stop`
1. Uninstall with: `sudo service lumiere uninstall`

### Auto turn off (optional)

If you want to turn off the Raspberry Pi at a specific time, add the following line to cron.  Note that this will not actually turn off the lights or stop power going to the Raspberry Pi, but simply shuts it down so that power can be disconnected.  An option is to then ahve an outlet timer that turns off a bit after the cron shutdown runs.

1. This adds a line to the crontab to shutodwn at `2:45 AM`: `(sudo crontab -l ; echo "45 2 * * * shutdown -h now") | sudo crontab -`
    * If you don't have a crontab for root yet, then you will get a message like `no crontab for root` which is fine.
