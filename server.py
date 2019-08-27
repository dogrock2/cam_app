import os
from flask import Flask, render_template, flash, session, redirect, url_for, request, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from flask_bcrypt import Bcrypt
from camera import Camera as cam
import threading
import rfid     #comment when recreating db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "elgatoloko"

db = SQLAlchemy(app)
Migrate(app,db)
bcrypt = Bcrypt()
feed = '1'


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', title="Home", H_or_P="Profiles", link="profiles", icon="fa-users")


@app.route("/profiles")
def profiles():
    from create_db import Profiles_Table
    profiles = Profiles_Table.query.all()
    profiles = get_all_frmt(profiles)
    return render_template('profiles.html', title="Profiles", H_or_P="Home", link="home", icon="fa-home", profiles=profiles)


@app.route("/settings")
def getSettings():
    from create_db import Admin_Table
    if 'admin' in session:
        settings = db.session.query(Admin_Table).one()
        settingsDict = {'uname':settings.uname, 'phone':settings.phone, 'email':settings.email, 'picEnable':settings.pic_enable, 'picRes':settings.pic_res, 'picTime':settings.pic_time, 'videoEnable':settings.video_enable, 'videoRes':settings.video_res, 'videoTime':settings.video_time, 'videoLength':settings.video_length, 'apiKey':settings.api_key, 'tokenKey':settings.twToken, 'twPhone':settings.twPhone,'rfidLocation':settings.rfid_loc}
        return json.dumps(settingsDict)
    return "None"


@app.route("/updatePic", methods=['POST'])
def updatePic():
    from create_db import Admin_Table
    picData = request.get_json()
    chk = db.session.query(Admin_Table).filter_by(id=1).first()
    chk.pic_res = picData['picRes']
    chk.pic_time = picData['picTime']
    chk.pic_enable = picData['picChk']
    db.session.add(chk)
    db.session.commit()
    return 'updated'


@app.route("/updateVid", methods=['POST'])
def updateVid():
    from create_db import Admin_Table
    vidData = request.get_json()
    chk = db.session.query(Admin_Table).filter_by(id=1).first()
    chk.video_res = vidData['vidRes']
    chk.video_time = vidData['vidTime']
    chk.video_enable = vidData['vidChk']
    chk.video_length = vidData['vidLength']
    db.session.add(chk)
    db.session.commit()
    return 'updated'


@app.route("/updateAdmin", methods=['POST'])
def updateAdmin():
    from create_db import Admin_Table
    adminData = request.get_json()
    chk = db.session.query(Admin_Table).filter_by(id=1).first()
    chk.email = adminData['adminEmail']
    chk.phone = adminData['adminPhone']
    chk.api_key = adminData['adminApiKey']
    chk.rfid_loc = adminData['adminRFID']
    chk.twToken = adminData['adminToken']
    chk.twPhone = adminData['twilioPhone']
    db.session.add(chk)
    db.session.commit()
    return 'updated'


@app.route('/frmProfileSave', methods=['POST'])
def frm_Save():
    from create_db import Profiles_Table
    if 'admin' in session:
        frmData = request.get_json()
        try:
            phone = int(frmData["phone"])
        except ValueError:
            phone = 0

        #Check if fob_id already in the system.
        chk = db.session.query(Profiles_Table).filter_by(fob_id=frmData['fob_id']).first()
        if chk == None:
            data_in = Profiles_Table(frmData["fob_id"],frmData["fname"],frmData["lname"],phone,frmData["email"],frmData["comms"],None,None,None,None,None,None)
            db.session.add(data_in)
            db.session.commit()
            return 'added'
        else:
            return 'confirm'
    else:
        return "login"


@app.route('/update_profile', methods=['POST'])
def updateDb_Profile():
    from create_db import Profiles_Table 
    frmData = request.get_json()
    chk = db.session.query(Profiles_Table).filter_by(fob_id=frmData['fob_id']).first()
    try:
        phone = int(frmData["phone"])
    except ValueError:
        phone = 0
   
    chk.fob_id = frmData["fob_id"]
    chk.fname = frmData["fname"]
    chk.lname = frmData["lname"]
    chk.phone = phone
    chk.email = frmData["email"]
    chk.comms = frmData["comms"]
    db.session.add(chk)
    db.session.commit()
    return 'updated'


@app.route('/delete_profile', methods=['POST'])
def deleteProfile():    
    from create_db import Profiles_Table
    if 'admin' in session:
        db_id = request.get_json()
        db.session.query(Profiles_Table).filter_by(id=db_id['id']).delete()
        db.session.commit()
        return 'deleted'
    else:
        return "login"


@app.route('/getOne_profile', methods=['POST'])
def updateProfile():    
    from create_db import Profiles_Table 
    db_id = request.get_json() 
    user = Profiles_Table.query.get(db_id['id'])   
    res_dict = {'id':user.id,'fob_id':user.fob_id,'fname':user.fname,'lname':user.lname,'phone':user.phone,'email':user.email,'comms':user.comms}
    j = json.dumps(res_dict)
    return j


@app.route('/close_session')
def closeSession():
    session.clear()
    return 'ok'


@app.route('/is_session')
def chkSession():
    if 'admin' in session:
        return 'true'
    else:
        return 'false'


@app.route('/verify_login', methods=['POST'])
def verifyLogin():
    pwd_obj = request.get_json()
    pwd = pwd_obj['pwd']
    if verify_password(pwd):
        session['admin'] = 'admin'
        return 'login_success'
    else:
        return "login_fail"


@app.route('/chng_pwd', methods=['POST'])
def changePwd():
    from create_db import Admin_Table
    if 'admin' in session:
        pwd_obj = request.get_json()
        print(pwd_obj)
        get_table = db.session.query(Admin_Table).filter_by(uname='admin').first()
        if bcrypt.check_password_hash(get_table.pwd, pwd_obj['pwd']):
            get_table.pwd = encode_pwd(pwd_obj['pwd2'])
            db.session.add(get_table)
            db.session.commit()
            return "Password changed"
        else:
            return "mismatch"
    else:
        return "Not logged in."


@app.route('/video_feed')
def video_feed():
    global feed
    if feed == '1':
        if get_pic_stat():
            return Response(gen(cam(get_frames())),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            flash("Pictures have been disabled. Check your settings.")
            return render_template('index.html', mess="LOL")

    if feed == '2':
        if get_vid_stat():
            return Response(rec(cam(get_frames())),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            flash("Videos have been disabled. Check your settings.")
            return render_template('index.html', mess="LOL2")

    if feed == '3':
        return Response("Server stopped!")


@app.route('/set_global_feed', methods=['POST'])
def set_global_feed():
    from rfid import set_feed
    global feed
    feedSet = request.get_json()
    feed_in = feedSet['dataIn']
    print(feed_in)
    if feed_in:
        set_feed(feed_in)
        feed = feed_in
    return 'ok'


@app.route('/get_feed_status')
def get_feed_status():
    global feed
    if feed == '1':
        if get_pic_stat():
            return 'true'
        else:
            return 'false1'
    if feed == '2':
        if get_vid_stat():
            return 'true'
        else:
            return 'false2'
    return 'false'


@app.route('/getPic/<name>')
def get_pic(name):
    name_url = 'saved_sendpic/'+name
    return send_file(name_url, mimetype='image/jpg')


@app.route('/getVid/<name>')
def get_vid(name):
    name_url = 'saved_vid/'+name
    return send_file(name_url, mimetype='video/mp4')

# *********************** Helper Functions *************************************
# ******************************************************************************


# converts the result from the Profile Table in db to a dictionary and returns it
def get_all_frmt(result):
    end_result = []
    for user in result:
        res_dict = {'id':user.id,'fob_id':user.fob_id,'fname':user.fname,'lname':user.lname,'phone':user.phone,'email':user.email,'comms':user.comms}
        end_result.append(res_dict)
    return end_result


# hashes the password and returns it
def encode_pwd(inputPwd):
    hashed = bcrypt.generate_password_hash(inputPwd)
    return hashed


# verifies if the password is in the database
def verify_password(pwd):
    from create_db import Admin_Table
    db_pwd = db.session.query(Admin_Table).filter_by(uname="admin").first()
    return bcrypt.check_password_hash(db_pwd.pwd, pwd)


# Live streams the camera's video when using camera picture function
def gen(camera):
    global feed
    while True:
        frame = camera.get_frame()
       # print("running video feed ")
        if feed == '3':
            camera.end_video()
        #    print("Video feed stopped... ")
            break
        if feed == '2':
            camera.end_video()
            break
        else:
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')


# Live streams the camera's video when using camera video function and will call
# the function to record when the option is selected and the fob is used.
def rec(camera):
    global feed
    while True:
        from rfid import do_rec, do_save, set_do_save
        frame = camera.captureVideo(do_rec)
        #print("running video rec... "+str(do_rec))
        if do_save:
            camera.save_video()
            set_do_save()
        if feed == '3':
            camera.end_video()
            #print("Video rec stopped... ")
            break
        elif feed == '1':
            camera.end_video()
            break
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')


# Grabs the frames settings from the database
def get_frames():
    from create_db import Admin_Table
    tbl = db.session.query(Admin_Table).one()
    return tbl.video_res


# Checks in the database if the picture feature is enabled.
def get_pic_stat():
    from create_db import Admin_Table
    tbl = db.session.query(Admin_Table).one()
    return tbl.pic_enable


# Checks in the database if the video feature is enabled.
def get_vid_stat():
    from create_db import Admin_Table
    tbl = db.session.query(Admin_Table).one()
    return tbl.video_enable



# *********************************************************************************
# *********************************************************************************

if __name__ == "__main__":

    def go():
        app.run(host="0.0.0.0", port="5000")


    #app.run(debug=True)

    t1 = threading.Thread(target=go)
    t2 = threading.Thread(target=rfid.get_fob)

    t2.start()
    t1.start()





##source <desired-path>/bin/activate
##source deactivate