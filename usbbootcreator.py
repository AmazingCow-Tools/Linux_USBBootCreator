#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        usbbootcreator.py                         ##
##            █ █        █ █        Linux USBBootCreator                      ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import os;
import os.path;
import getopt;
import sys;
import subprocess;
import shlex;

#Since termcolor isn't a standard package do not force the user to have it.
#But print a *nice* message about the lost features :)
try:
    from termcolor import colored;
except:
    print "termcolor cannot be imported - No colors for you :/";
    def colored(msg, color):
        return msg;


################################################################################
## Classes                                                                    ##
################################################################################
class Globals:
    disk_image_path = None;

class Output:
    @staticmethod
    def log_fatal(msg):
        print "[FATAL] {}".format(msg);
        exit(1);

class USBInfo:
    def __init__(self):
        self._items_list = [];

    def get_number_of_disks(self):
        return len(self._items_list);

    def get_disk_info_at(self, index):
        return self._items_list[index];

    def find_all_usb_disks(self):
        LSBLK_COMMAND="lsblk -inP -o NAME,MODEL,SIZE,TYPE {}";

        for block_item in os.listdir("/sys/block/"):
            if(os.path.exists("/sys/block/" + block_item + "/device")):
                full_block_name = "/dev/{}".format(block_item);
                cmd             = LSBLK_COMMAND.format(full_block_name);

                output = subprocess.check_output(cmd, shell=True);
                output = output.replace("\n",":")
                output = output[0:output.find(":")];

                block_item_info = {};
                for item_info_piece in shlex.split(output):
                    key,value = item_info_piece.split("=");
                    block_item_info[key]=value.lstrip(" ").rstrip(" ");

                if(block_item_info["TYPE"] == "disk"):
                    self._items_list.append(block_item_info);


    def get_info_list(self):
        for item in self._items_list:
            yield item;


################################################################################
## Helper Methods                                                             ##
################################################################################
def check_disk_image_path():
    if(Globals.disk_image_path is None):
        msg = "No Disk Image Path was provided.";
        Output.log_fatal(msg);

    if(not os.path.exists(Globals.disk_image_path)):
        msg = "Disk Image Path isn't valid. ({})".format(Globals.disk_image_path);
        Output.log_fatal(msg);


################################################################################
## Disk Printing                                                              ##
################################################################################
def print_usb_item_info(index, usb_item):
    print "({})  {} : {} : {:6} : {}".format(
        index,
        "/dev/" + usb_item["NAME"],
        usb_item["TYPE"],
        usb_item["SIZE"],
        usb_item["MODEL"]);


def present_usb_info(usb_info):
    print "The following was found:";
    index = 1;
    for usb_item in usb_info.get_info_list():
        print_usb_item_info(index, usb_item);
        index += 1;


################################################################################
## Prompts                                                                    ##
################################################################################
def prompt_install_disk(usb_info):
    while(1):
        present_usb_info(usb_info);
        print "Choose the disk carefully...";
        print;
        print "Please insert the disk number [OR ^C TO CANCEL]";

        prompt = "Disk Number (1-{}):".format(usb_info.get_number_of_disks());
        index = raw_input(prompt);

        if(not index.isdigit() or
           int(index) < 1 or
           int(index) > usb_info.get_number_of_disks()):
            print "Invalid disk number: ({})".format(index);
            raw_input();
        else:
            return int(index);


def prompt_make_sure_that_is_correct_disk(usb_info, selected_disk):
    print
    print "ARE YOU SURE THAT YOU SELECTED THE CORRECT DISK?";
    print "     WE'RE GOING TO A POINT OF NO RETURN";
    print "SO MAKE **SURE** THAT THE DISK INFO IS CORRECT";
    print "IF NOT (OR YOU ARE IN DOUBT PRESS ^C TO CANCEL";
    print
    print "The disk info is:";
    print_usb_item_info(selected_disk,
                        usb_info.get_disk_info_at(selected_disk -1));

    print;
    print "Are you SURE?:";
    value = raw_input("Type 'yes' to continue:");
    if(value != "yes"):
        Output.log_fatal("Invalid values was provided - Canceling...");


################################################################################
## DD                                                                         ##
################################################################################
def create_bootable_disk(out_disk_path):
    in_disk_path = os.path.abspath(Globals.disk_image_path);
    cmd_dd = "sudo dd if={} of={} bs=1m".format(in_disk_path,
                                                out_disk_path);

    print "Creating bootable disk.";
    print "This program uses dd(1) to accomplish the task."
    print "But it generates no output while it's performing the operation";
    print "So take a cup of coffee - When the task is done we show to you :)";
    print "PS: dd(1) requires super user mode!"

    print;
    print "Source is: {}".format(in_disk_path);
    print "Destination is: {}".format(out_disk_path);
    print;

    print "dd(1) command is: {}".format(cmd_dd);
    print





################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    options = getopt.gnu_getopt(sys.argv[1:], "", ["image="]);

    #Parse the options.
    for key, value in options[0]:
        key = key.strip("-");

        if(key in "image"):
            Globals.disk_image_path = value;

    #Perform some sanity checks...
    check_disk_image_path();

    #Get the info about the usb sticks attached to computer.
    usb_info = USBInfo();
    usb_info.find_all_usb_disks();

    selected_disk = prompt_install_disk(usb_info);
    prompt_make_sure_that_is_correct_disk(usb_info, selected_disk);

    name = usb_info.get_disk_info_at(selected_disk-1)["NAME"];
    output_disk_path = os.path.join("/dev/", name);
    create_bootable_disk(output_disk_path);


if __name__ == '__main__':
    main()
