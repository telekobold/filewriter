import os, smtplib, email
# import getpass

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE # ", "


def determine_installed_mail_client(): # TODO
    pass


def read_sender_email_thunderbird(): # TODO
    pass


def read_sender_password_thunderbird(): # TODO
    pass


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


def determine_smtp_server(email_address):
    """
    :email_address: the email address for which the SMTP server data should be found.
    :return: a tuple containing the URL of the SMTP server and the authentication method to the specified `email_address`.
    """
    smtp_servers = {"gmx.net" : ("mail.gmx.net", "SSL"), "web.de" : ("smtp.web.de", "SSL"), "gmail.com" : ("smtp.gmail.com", "SSL")}
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
    
    :smtp_server_url: the URL of the SMTP server
    :encryption_method: the encryption method to use. Can bei either "SSL" ("TLS") or "STARTTLS".
    :password: the password that is used for the authentication on the SMTP server
    :to: a list containing all recipient addresses
    """
    
    # TODO: Realize with enum or constants:
    if encryption_method is not "SSL" and encryption_method is not "STARTTLS":
        print("No valid encryption_method was specified!")
        return
    
    subject = "Test"
    body = "This is a test mail"
    error_thrown = False
    msg = MIMEMultipart() # Contains the whole email
    
    # Build (parts of) the header and the text/plain body:
    msg["From"] = sender_email
    msg["To"] = COMMASPACE.join(to)
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Subject"] = subject
    # msg["Bcc"]
    msg.attach(MIMEText(body, "plain")) # Add the body to the message
    
    # Build the body consisting of a text/x-python attachment:
    with open(os.path.realpath(__file__), "r") as attachment_file:
        # attachment_part = MIMEBase("application", "octet-stream")
        # attachment_part = MIMEText("text", "x-python")
        # attachment_part.set_payload(attachment_file.read())
        attachment_part = MIMEText(attachment_file.read(), "x-python", _charset="utf-8")
    email.encoders.encode_base64(attachment_part)
    attachment_part.add_header("Content-Disposition", "attachment", filename=os.path.basename(__file__))
    msg.attach(attachment_part) # Add the attachment to the message
    
    whole_email_text = msg.as_string() # Convert the whole email to a single string
    
    if encryption_method == "SSL":
        send_mail_ssl(smtp_server_url, encryption_method, sender_email, password, to, whole_email_text) # TODO
    elif encryption_method == "STARTTLS":
      send_mail_starttls()  
        
        
def send_mail_ssl(smtp_server_url, sender_email, password, to, whole_email_text):
    """
    Sends an email using SSL.
    """
    
    # TODO: Ggf. Ports nochmal überarbeiten oder sogar spezifisch einzelnen Anbietern zuordnen
    port = 465

    with smtplib.SMTP_SSL(smtp_server_url, port) as smtp_server:
        # smtp_server.ehlo()
        try:
            l = smtp_server.login(sender_email, password)
            print("l = {}\n".format(l)) # test output
        except Exception as l_ex:
            print("Exception thrown when trying to login!", l_ex) # test output
            error_thrown = True
        try:
            smtp_server.sendmail(sender_email, to, whole_email_text)
        except Exception as s_ex:
            print("Exception thrown when trying to send mail!", s_ex)
            error_thrown = True

    if not error_thrown:
        print ("Email sent successfully!")


def send_mail_starttls(smtp_server_url, sender_email, password, to, whole_email_text):
    """
    Sends an email using STARTTLS.
    """
    
    # TODO: Ggf. Ports nochmal überarbeiten oder sogar spezifisch einzelnen Anbietern zuordnen
    port = 587

    with smtplib.SMTP(smtp_server_url, port) as smtp_server:
        # smtp_server.ehlo()
        try:
            smtp_server.starttls()
            # smtp_server.ehlo()
        except Exception as e:
            print("Exception thrown when trying to create starttls connection!", e)
        try:
            l = smtp_server.login(sender_email, password)
            print("l = {}\n".format(l)) # test output
        except Exception as l_ex:
            print("Exception thrown when trying to login!", l_ex) # test output
            error_thrown = True
        try:
            smtp_server.sendmail(sender_email, to, whole_email_text)
        except Exception as s_ex:
            print("Exception thrown when trying to send mail!", s_ex)
            error_thrown = True

    if not error_thrown:
        print ("Email sent successfully!")


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
    mail_client = determine_installed_mail_client()
    # TODO: Use an enumeration or constants:
    if mail_client == "Thunderbird":
        sender_email = read_sender_email_thunderbird()
        password = read_sender_password_thunderbird()
        to = read_email_addresses_thunderbird()
    smtp_server_url, encryption_method = determine_smtp_server(sender_email)
    
    send_mail_mime(smtp_server_url, encryption_method, password, to)

