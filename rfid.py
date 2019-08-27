import os
from shutil import copyfile
import time
from getDB import get_db_data, get_rfid_path, get_admin_email
from send_email import send_msg
from send_msg import send_twilio_msg
from log_msg import save_msg_log
from requests import get


do_rec = False
do_save = False
feed = '3'
RFIDpath = get_rfid_path()
ip = get('https://api.ipify.org').text


# This function listens for a fob and then converts the data received to a string. Then calls the proper
# function to send either a pic or a video.
def get_fob():
    global feed
    global activateFob
    fp = open(RFIDpath, 'rb')
    vals = (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40)
    conv = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '')
    result = []



    # Infinite loop waiting for a fob swipe
    while True:
        buffer = fp.read(16)
        print(ip)
        for c in buffer:
          if c > 0:
             for i in range(11):
                if c == vals[i]:
                   result.append(conv[i])
                   if i == 10:
                       fob = ''.join(result)
                       if feed == '1':
                           get_rec_pic(fob)
                       if feed == '2':
                           get_rec_vid(fob)
                       result = []


def set_do_save():  # Sets the global flag do_save.
    global do_save
    do_save = False


def set_feed(feed_in):  # Sets the global flag feed.
    global feed
    feed = feed_in


#  copies the picture from the saved_pic directory over to the saved_sendpic and renames it starting with the
#  fob id value. The original picture will get deleted from the saved_pic directory.
def get_rec_pic(fob):

    saved_pic = "saved_pic/cap_pic.jpg"
    saved_pic_name = str(fob)+"saved_pic.jpg"
    saved_pic_fob = "saved_sendpic/" + str(fob) + "saved_pic.jpg"
    if os.path.isfile(saved_pic):
        copyfile(saved_pic, saved_pic_fob)
        send_pic(fob, saved_pic_name, saved_pic_fob)
    elif os.path.isfile(saved_pic_fob):
        os.remove(saved_pic_fob)


#  This function grabs the fob id and searches the database for the data associated with that id. Checks the comms value
#  to see if SMS or Email is set and then sends the data to the appropriate file / function.
def send_pic(fob, saved_pic_name, saved_pic_fob):

    fname, email, phone, api_key, comms, pic_enable, pic_res, pic_time, video_enable, video_res, video_length, video_time = get_db_data(fob)

    #  Sends data and calls the twilio function to send SMS.
    if comms == 'SMS' or comms == "EMail/SMS":
        myIP = "http://"+ip+":5000/getPic/"
        if str(phone)[0] != '1':
            phone = '1'+str(phone)
        send_twilio_msg("A message from"+fname+".", phone, saved_pic_name, myIP)

    #  Sends emails. Gets data and calls the email function.
    if comms == 'EMail' or comms == "EMail/SMS":
        admin_email = get_admin_email()
        send_msg(admin_email, email, saved_pic_fob, fname)


# Sends video clips via email or SMS.
def get_rec_vid(fob):
    global do_rec
    global do_save

    time_length_variation = 0  # May be needed to tweak time so recording length matches the settings.

    # This try clause checks that data is returned from the database. If not then all it does it print a message. Avoids
    # an error to be displayed.
    try:
        fname, email, phone, api_key, comms, pic_enable, pic_res, pic_time, video_enable, video_res, video_length, video_time = get_db_data(fob)

        do_rec = True  # starts recording
        do_save = False  # don't save yet
        sec = video_length - time_length_variation
        while sec >= 0:
            sec -= 1
            time.sleep(1)
        #after loop executes
        do_rec = False #stop recording
        do_save = True #save the video clip. This happens in the camera class

        saved_vid_name = 'myVideo.mp4'
        vid_url = "saved_vid/myVideo.mp4"

        # Sends video clip via SMS Twilio
        if comms == 'SMS' or comms == "EMail/SMS":
            myIP = "http://"+ip+":5000/getVid/"
            if str(phone)[0] != '1':
                phone = '1'+str(phone)
            send_twilio_msg("A message from"+fname+".", phone, saved_vid_name, myIP)

        # Sends video clip via Email.
        if comms == 'EMail' or comms == "EMail/SMS":
            admin_email = get_admin_email()
            time.sleep(2)
            send_msg(admin_email, email, vid_url, fname)

    except TypeError:
        save_msg_log("Fob not recognized in the database.")

