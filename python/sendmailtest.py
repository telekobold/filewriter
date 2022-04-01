#!/usr/bin/python

import os
import smtplib
import email
import distutils.spawn
import re
# import getpass

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE # Value: ", "

import filewriter


# ----- constants: -----
THUNDERBIRD = "Thunderbird"
OUTLOOK = "Outlook"
SSL = "SSL"
TLS = "TLS"
STARTTLS = "STARTTLS"


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
    
    # thunderbird_dirname = os.path.join(users_home_dir(), ".thunderbird")
    # TODO: Substitute temporary `thunderbird_dirname` for testing purposes:
    thunderbird_dirname = os.path.join(users_home_dir(), "thunderbird-Kopie")
    # The name of the profile directory consists of 8 letters or digits, 
    # followed by the string ".default-release":
    profile_dir_regex = re.compile("[0-9a-z]{8}\.default-release")
    user_name = None
    user_email = None

    # Search the user's home directory for a file "prefs.js", contained in the 
    # user's default Thunderbird profile directory:
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
                profile_dir = absolute_filename
                prefs_js_filename = os.path.join(profile_dir, "prefs.js")
                if os.path.isfile(prefs_js_filename):
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
                                break # Break the loop since the searched user 
                                      # name was found.
                    # Search the file "prefs.js" for the users' email address:
                    for i in lines:
                        if "mail.identity.id1.useremail" in lines[i]:
                            user_email_match = re.search(email_regex_incl, lines[i])
                            if user_email_match:
                                user_email_raw = user_email_match.group()
                                user_email = user_email_raw[3:len(user_email_raw)-3:1]
                                break # Break the loop since the search user 
                                      # email address was found.
                # Break the loop through the content of `thunderbird_dirname`.
                break
                
    return (user_name, user_email)


def read_sender_password_thunderbird():
    # TODO
    pass


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
    print(determine_installed_mail_client())
    print(read_sender_name_and_email_thunderbird())
    print(read_sender_name_and_email_thunderbird()[0])
    print(read_sender_name_and_email_thunderbird()[1])
    
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

