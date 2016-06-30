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
import getopt;
import os.path;
import os;
import shlex;
import subprocess;
import sys;

################################################################################
## Classes                                                                    ##
################################################################################
class Constants:
    #Flags.
    ALL_FLAGS_SHORT = "hv";
    ALL_FLAGS_LONG  = ["help", "version"];

    FLAG_HELP    = "h", "help";
    FLAG_VERSION = "v", "version";

    #App
    APP_NAME      = "usb-boot-creator";
    APP_VERSION   = "0.4.1";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015, 2016 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));

class Output:
    @staticmethod
    def log_fatal(msg):
        print "[FATAL] {}".format(msg);
        exit(1);

    @staticmethod
    def show_help():
        msg = """Usage:
usb-boot-creator [-hv] <disk-image-path>

Options:
  *-h --help    : Show this screen.
  *-v --version : Show app version and copyright.

Notes:
  TAKE [A LOT OF] CARE, this program need perform dd(1) as,
  SUPERUSER so double check your disk name before do anything stupid.

  Options marked with * are exclusive, i.e. the usb-boot-creator
  will run that and exit successfully after the operation.
  """;
        print msg;
        exit(0);

    @staticmethod
    def show_version():
        print "{} - {} - {}".format(Constants.APP_NAME,
                                    Constants.APP_VERSION,
                                    Constants.APP_AUTHOR);
        print Constants.APP_COPYRIGHT;
        print
        exit(0);


class DiskInfo:
    def __init__(self):
        self._items_list = [];

    def get_number_of_disks(self):
        return len(self._items_list);

    def get_disk_info_at(self, index):
        return self._items_list[index];

    def find_all_disks(self):
        #Constants...
        LSBLK_COMMAND     = "lsblk -inP -o NAME,MODEL,SIZE,TYPE {}";
        BLOCK_DIR_PATH    = "/sys/block/";
        DEVICE_DIR_SUFFIX = "device";
        DEV_DIR_PATH      = "/dev/";

        #Iterate for all "block devices".
        for block_item in os.listdir(BLOCK_DIR_PATH):
            full_block_device_path = os.path.join(BLOCK_DIR_PATH,
                                                  block_item,
                                                  DEVICE_DIR_SUFFIX);

            if(os.path.exists(full_block_device_path)):
                full_block_name = os.path.join(DEV_DIR_PATH, block_item);
                cmd             = LSBLK_COMMAND.format(full_block_name);

                #Execute the command as a subprocess and capture the output.
                output = subprocess.check_output(cmd, shell=True);

                #Clean up the output
                DUMMY_CHAR = ":";
                output = output.replace("\n", DUMMY_CHAR)
                output = output[0:output.find(DUMMY_CHAR)];

                #The output came as string composed of KEY=VALUES pairs.
                #So split them into a manageable piece of information
                #And set it to the block_item_info.
                block_item_info = {};
                for item_info_piece in shlex.split(output):
                    key,value = item_info_piece.split("=");
                    block_item_info[key]=value.lstrip(" ").rstrip(" ");

                #We're only interested in disk devices, so discard all that
                #doesn't match the criteria.
                if(block_item_info["TYPE"] == "disk"):
                    self._items_list.append(block_item_info);


    def get_info_list(self):
        for item in self._items_list:
            yield item;


################################################################################
## Helper Methods                                                             ##
################################################################################
def canonize_path(path):
    return os.path.abspath(os.path.expanduser(path));

def check_disk_image_path(disk_image_path):
    if(disk_image_path is None):
        msg = "No Disk Image Path was provided.";
        Output.log_fatal(msg);

    if(not os.path.exists(disk_image_path)):
        msg = "Disk Image Path isn't valid. ({})".format(disk_image_path);
        Output.log_fatal(msg);


################################################################################
## Disk Printing                                                              ##
################################################################################
def print_disk_item_info(index, usb_item):
    print "({})  {} : {} : {:6} : {}".format(index,
                                             "/dev/" + usb_item["NAME"],
                                             usb_item["TYPE"],
                                             usb_item["SIZE"],
                                             usb_item["MODEL"]);

def present_disk_info(disk_info):
    print "Found the following disk(s):";
    index = 1;
    for usb_item in disk_info.get_info_list():
        print_disk_item_info(index, usb_item);
        index += 1;


################################################################################
## Prompts                                                                    ##
################################################################################
def prompt_install_disk(disk_info):
    #Continue while the user cancels or enter a valid input...
    while(1):
        #Print the info to user.
        present_disk_info(disk_info);

        print "Choose the disk carefully...\n";
        print "Please insert the disk number [OR ^C TO CANCEL]";

        prompt = "Disk Number (1-{}):".format(disk_info.get_number_of_disks());

        #Get the input.
        index = raw_input(prompt);


        #The input is not a digit - Inform the user and go
        #straight to begin of loop.
        if(not index.isdigit()):
            msg = "{} ({}) - {}".format("Invalid input:", index,
                                         "Enter the number of the desired disk");
            print msg;
            raw_input();
            continue;


        index = int(index);

        #Check if the index is valid.
        if(index >= 1 and index <= disk_info.get_number_of_disks()):
            return index;
        else:
            msg = "{} ({}) - {}".format("Invalid index:", index,
                                        "Make sure that index is inside the range");
            print msg;
            raw_input();
            continue;


def prompt_make_sure_that_is_correct_disk(disk_info, selected_disk):
    ## Define the messages...
    warning_msg = """
+-------------------  WARNING  --------------------+
| ARE YOU SURE THAT YOU SELECTED THE CORRECT DISK? |
|       WE ARE GOING TO A POINT OF NO RETURN       |
|  SO MAKE **SURE** THAT THE DISK INFO IS CORRECT  |
|  IF NOT OR YOU ARE IN DOUBT PRESS ^C TO CANCEL!  |
+--------------------------------------------------+
""";

    #Print the info to user.
    print warning_msg;

    print "The disk info is:";
    print_disk_item_info(selected_disk,
                         disk_info.get_disk_info_at(selected_disk -1));

    #Get the input.
    print "\nAre you SURE?:";
    value = raw_input("Type 'yes' to continue: ");

    #Do some sanity checks...
    if(value != "yes"):
        Output.log_fatal("You need type [yes] to continue - Canceling...");


################################################################################
## DD                                                                         ##
################################################################################
def create_bootable_disk(disk_image_path, out_disk_path):
    #Build the commands that will be executed...
    in_disk_path = canonize_path = disk_image_path;
    cmd_dd       = "sudo dd if=\"{}\" of=\"{}\" bs=1M && sync".format(in_disk_path,
                                                                      out_disk_path);

    ## Define the messages...
    start_msg = """
+-------------------  Creating bootable disk  --------------------+
|    This program uses dd(1) to create the boot disk but dd(1)    |
|  does not generate output while performing its the operation.   |
|                                                                 |
|                     So take a cup of coffee                     |
|       When the dd(1) operation is done we show to you :)        |
|                                                                 |
|                PS: dd(1) requires super user mode               |
|                So enter your password if requested.             |
+-----------------------------------------------------------------+
""";

    end_msg = "\n\nEverything is done...\nEnjoy your Linux installation :)";


    #Print the info to user.
    print start_msg;

    print "Source is        : ({})".format(in_disk_path);
    print "Destination is   : ({})".format(out_disk_path);
    print "dd(1) command is : ({})".format(cmd_dd);


    #Execute the dd command.
    if(os.system(cmd_dd) != 0):
        Output.log_fatal("Error while executing dd(1)");

    #Just print a goodbye...
    print end_msg;



################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    try:
        #Get the command line options.
        options = getopt.gnu_getopt(sys.argv[1:],
                                    Constants.ALL_FLAGS_SHORT,
                                    Constants.ALL_FLAGS_LONG);
    except Exception, e:
        Output.log_fatal(str(e));


    #Parse the options.
    for key, value in options[0]:
        key = key.strip("-");
        if  (key in Constants.FLAG_HELP    ): Output.show_help();
        elif(key in Constants.FLAG_VERSION ): Output.show_version();

    disk_image_path = None if (len(options[1]) == 0) else options[1][0];

    if(disk_image_path is None):
        Output.log_fatal("Missing disk image path");

    #Perform some sanity checks...
    disk_image_path = canonize_path(disk_image_path);
    check_disk_image_path(disk_image_path);

    #Get the info about the usb sticks attached to computer.
    disk_info = DiskInfo();
    disk_info.find_all_disks();

    #Prompt user.
    try:
        selected_disk = prompt_install_disk(disk_info);
        prompt_make_sure_that_is_correct_disk(disk_info, selected_disk);
    except KeyboardInterrupt, e:
        print "\n\nCanceled...";
        exit(0);

    #We show to user ONE-BASED list but python is ZERO-BASED so the -1.
    name = disk_info.get_disk_info_at(selected_disk-1)["NAME"];
    output_disk_path = canonize_path(os.path.join("/dev/", name));
    create_bootable_disk(disk_image_path, output_disk_path);


if __name__ == '__main__':
    main()
