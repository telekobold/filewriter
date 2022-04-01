#!/usr/bin/python

import shutil
import os
import time


def copy_itself(destination):
    """
    Makes a copy of this script and writes it to `destination`.
    
    Writes the current date and time as prefix to the file name of the created 
    copy (including year, month, day, hours, minutes and seconds). This should 
    avoid that multiple calls to this function always overwrite the copy
    from the previous call.
    
    :destination: the absolute file path where the copy should be placed;
                  has type `str`
    """
    copy_name = time.strftime("%Y-%m-%d_%H%M%S") + "_" + os.path.basename(__file__)
    shutil.copy(__file__, os.path.join(destination, copy_name))


if __name__ == "__main__":
    copy_itself("/home/telekobold/TestVerzeichnis")
