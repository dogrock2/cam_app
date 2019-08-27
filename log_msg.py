import datetime


# Saves messages to the text file named log.txt
def save_msg_log(msg):

    current = datetime.datetime.now()

    with open("log.txt", "a") as myfile:
        myfile.write(str(current) +":   -"+msg + "\n")

