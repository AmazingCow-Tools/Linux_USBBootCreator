# Linux USBBootCreator

**Made with <3 by [Amazing Cow](http://www.amazingcow.com).**



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Description:

```usb-boot-creator``` - Creates bootable usb sticks with ease.

```usb-boot-creator``` is a small tool to help the easy but very tedious 
task of turning a usb stick into a bootable usb stick.

It's mainly a _wrapper_ of ```dd(1)``` letting you forget about the clumsy 
command line options and providing security checks. 

### DISCLAIMER 

** ```dd(1)``` MUST BE DONE WITH SUPERUSER PRIVILEGES AND YOU'RE MESSING WITH 
YOUR DISKS, SO TAKE A DOUBLE, TRIPLE, 100^100 CHECK BEFORE HIT ENTER :)**


<br>

As usual, you are **very welcomed** to **share** and **hack** it.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Usage:

``` bash
usb-book-creator [-hv] <disk-image-path>

Options:
  *-h --help     : Show this screen.
  *-v --version  : Show app version and copyright.

Notes:
  TAKE [A LOT OF] CARE, this program need perform dd(1) as,
  SUPERUSER so double check your disk name before do anything stupid.

  Options marked with * are exclusive, i.e. the usb-book-creator
  will run that and exit successfully after the operation.

```



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Install:

Use the Mafefile.

``` bash
    make install
```

Or to uninstall

``` bash
    make uninstall
```



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Dependencies:

There is no dependency for ```usb-boot-creator```.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Environment and Files: 

```usb-boot-creator``` do not create / need any other files or environment vars.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## License:

This software is released under GPLv3.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## TODO:

Check the TODO file for general things.

This projects uses the COWTODO tags.   
So install [cowtodo](http://www.github.com/AmazingCow-Tools/COWTODO.html) and run:

``` bash
$ cd path/for/the/project
$ cowtodo 
```

That's gonna give you all things to do :D.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## BUGS:

We strive to make all our code the most bug-free as possible - But we know 
that few of them can pass without we notice ;).

Please if you find any bug report to [bugs_opensource@amazingcow.com]() 
with the name of this project and/or create an issue here in Github.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Source Files:

* AUTHORS.txt
* CHANGELOG.txt
* COPYING.txt
* Makefile
* OLDREADME.md
* README.md
* TODO.txt
* usbbootcreator.py



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
