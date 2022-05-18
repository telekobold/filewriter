#!/usr/bin/python

import distutils.spawn
import smtplib
# import getpass
#import typing

import filewriter


THUNDERBIRD: str = "Thunderbird"
OUTLOOK: str = "Outlook"


def determine_installed_mail_client() -> str:
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


# TODO: specify return value `typing.Generator[yield_type, send_type, return_type]`
def gen_dict_extract(searched_key: filewriter.ArbitraryType, searched_elem: filewriter.ArbKeyArbValDict):
    """
    Recursively searches the passed `searched_elem` for the passed 
    `searched_key`.
    
    Taken from from https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists 
    
    :searched_key:  the key to search for
    :searched_elem: the element which should be searched. Can contain 
                    arbitrarily nested dictionaries.
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


def send_mail_plain() -> None:
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
    print(f"type(t) = {str(type(t))}") # TODO: is `str` instead of `tuple`!
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

