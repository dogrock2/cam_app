import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from log_msg import save_msg_log

# Uses gmail acct to send emails. Gets called from the rfid file.

EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']  # gets email password store in an env variable.

def send_msg(email_from, emailTo, mult_file, name):

    multimedia_file = "./" + mult_file
    msg = MIMEMultipart()
    msg['Subject'] = "School Multimedia Message"
    msg['From'] = email_from
    msg['To'] = emailTo

    msg.attach(MIMEText("A multimedia message from "+name+"'s school.", 'plain'))

    filename = os.path.basename(multimedia_file)
    attachment = open(multimedia_file, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_from, EMAIL_PASSWORD)
        smtp.send_message(msg)

    save_msg_log("Email Sent - No errors sending email.")

