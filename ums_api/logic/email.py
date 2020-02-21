"""
The logic for sending emails
"""
import smtplib
from email.message import EmailMessage

from .. import APP, APP_LOGGER


def send_email(recipient_address: str, subject: str, body: str):
    """
    Sends a email with the given body and subject the the given address.
    """
    APP_LOGGER.debug("Sending mail to " + recipient_address + " with subject " + subject + " and body " + body)

    host = APP.config["MAIL_SERVER_HOST"]
    port = APP.config["MAIL_SERVER_PORT"]

    smtp: smtplib.SMTP

    if APP.config["MAIL_SERVER_SSL"]:
        print("SSL:" + str(host) + ";" + str(port))
        smtp = smtplib.SMTP_SSL(host, port)
    else:
        print("Normal:" + str(host) + ";" + str(port))
        smtp = smtplib.SMTP(host, port)

    smtp.ehlo_or_helo_if_needed()

    if APP.config["MAIL_SERVER_STARTTLS"]:
        print("STARTTLS")
        smtp.starttls()

    if APP.config["MAIL_SERVER_LOGIN"]:
        print("Login")
        smtp.login(APP.config["MAIL_SERVER_USER"], APP.config["MAIL_SERVER_PW"])

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = APP.config["MAIL_SENDING_ADDRESS"]
    msg['To'] = recipient_address
    print("Sned")
    smtp.send_message(msg)


def send_registraion_email(recipient_address: str, token_url: str):
    """
    Sends the registration email to the given recipient,
    containing the given token_url for mail verification
    """
    send_email(recipient_address, APP.config["REGISTRATION_MAIL_SUBJECT"], APP.config["REGISTRATION_MAIL_BODY"].format(token_url))