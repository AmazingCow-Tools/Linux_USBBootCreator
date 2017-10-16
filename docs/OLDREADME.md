Linux USBBootCreator
====

Made with <3 by [Amazing Cow](http://www.amazingcow.com).

# NOTICE
## THIS IS A OLD README FILE - IT ONLY EXISTS FOR HISTORY SAKE - WE DON'T UPDATE
## THIS ANYMORE - CHECK THE README.MD FOR UPDATED INFO.
# NOTICE

<!-- ####################################################################### -->

## Intro:

To make a Bootable USB Disk on Linux, you normally have to find out which disk 
is your's USB disk, next umount it and after that run ```dd(1)``` to copy the 
contents of the ```.iso``` to the USB disk.

This is a very easy, but tedious task...

We want automate this a little bit, since is very tedious repeat the same 
keystrokes over and over again...

So here is our simple program to automate some tedious parts of creating an USB
boot disk on Linux.


#### Note:

** ```dd(1)``` MUST BE DONE WITH SUPERUSER PRIVILEGES AND YOU'RE MESSING WITH 
YOUR DISKS, SO TAKE A DOUBLE, TRIPLE, 100^100 CHECK BEFORE HIT ENTER :)**



<!-- ####################################################################### -->

## Install:

Use the makefile

```make installl```


<!-- ####################################################################### -->

## Usage:

```
linux_usbbootcreator [-hv] --image=<path>

Options:
 *-h --help         : Show this screen.
 *-v --version      : Show app version and copyright.
     --image <path> : The path of .iso.
 
```

##### Notes:
TAKE A LOT OF CARE, you will need perform ```dd(1)``` as superuser, so double
check your disk name before do anything stupid.

Options marked with * are exclusive, i.e. the ```linux_usbbootcreator``` will run that
and exit successfully after the operation.


<!-- ####################################################################### -->

## License:
This software is released under GPLv3.


<!-- ####################################################################### --> 

## TODO:
Check the TODO file.

<!-- ####################################################################### --> 

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
