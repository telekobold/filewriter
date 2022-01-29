import os, smtplib, email
# import getpass

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE # ", "


def send_mail_mime():
    """
    Sends a plaintext email containing this script as attachment.
    """
    smtp_server_name = "smtp.gmail.com"
    port = 465
    # sender_email = "s@s"
    # password = ""
    password = input("Email password:")
    # password = getpass.getpass("Email password:")
    # to = ["a@s", "b@s", "c@s"]
    subject = "Test"
    body = "This is a test mail"
    error_thrown = False
    
    msg = MIMEMultipart()
    
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
    
    whole_text = msg.as_string() # Convert the whole email to a single string
    
    smtp_server = smtplib.SMTP_SSL(smtp_server_name, port)
    # smtp_server.ehlo()

    try:
        l = smtp_server.login(sender_email, password)
        print("l = {}\n".format(l)) # test output
    except Exception as l_ex:
        print("Exception thrown when trying to login!", l_ex) # test output
        error_thrown = True

    try:
        smtp_server.sendmail(sender_email, to, whole_text)
    except Exception as s_ex:
        print("Exception thrown when trying to send mail!", s_ex)
        error_thrown = True

    smtp_server.close()
    if not error_thrown:
        print ("Email sent successfully!")


def send_mail_plain():
    """
    Sends a plaintext email.
    """
    smtp_server_name = "smtp.gmail.com"
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

    smtp_server = smtplib.SMTP_SSL(smtp_server_name, port)
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
    send_mail_mime()

