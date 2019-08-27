from twilio.rest import Client
from log_msg import save_msg_log


# Uses the twilio API to send a text message.
# Gets called from the rfid file and after it executes it sends results message to log file.


def send_twilio_msg(msg, dest, media_url, myIP):
    from getDB import get_twilio
    global phone

    account_sid, auth_token, phone = get_twilio()

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+"+str(dest),
        from_="+"+str(phone),
        body=msg,
        media_url=myIP+media_url)

    save_msg_log(message.sid)  # sends result message to log file.
