from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_
from flask import Flask
from decouple import config

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+config('DATABASE_URL').split('//')[1]
db = SQLAlchemy(server)


def add_queue(chat_id, gender, gendermatch, age, agefilter_ll, agefilter_ul, seeking, mbti, message_id):
    user = Queue(chat_id=chat_id,gender=gender,gendermatch=gendermatch,age=age,agefilter_ll=agefilter_ll, agefilter_ul=agefilter_ul, seeking=seeking,mbti=mbti,message_id=message_id)
    db.session.add(user)
    db.session.commit()
    
def delete_queue(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    db.session.delete(user)
    db.session.commit()
    
def delete_chat(id_chat):
    user = Chats.query.filter_by(id=id_chat).first()
    chatone = user.chat_one
    chattwo = user.chat_two
    if get_last_chat(chatone) == None:
        user2 = Lastchat(user=chatone,match=chattwo) #lastchat entry for chatone person
        db.session.add(user2)
    else:
        user2 = Lastchat.query.filter_by(user=chatone).first()
        user2.user = chatone
        user2.match = chattwo

    if get_last_chat(chattwo) == None:
        user3 = Lastchat(user=chattwo,match=chatone) #lastchat entry for chattwo person
        db.session.add(user3)
    else:
        user3 = Lastchat.query.filter_by(user=chattwo).first()
        user3.user = chattwo
        user3.match = chatone
     
    db.session.delete(user)
    db.session.commit()

def setup_complete(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if bool(user.chat_id) and bool(user.gender) and bool(user.age) and bool(user.gendermatch) and bool(user.seeking) and bool(user.mbti) and bool(user.agefilter_ll) and bool(user.agefilter_ul):
        return True
    else:
        return False
        
def set_user(chat_id):
        user = Users.query.filter_by(chat_id=chat_id).first()           
        if user == None:
            user = Users(chat_id=chat_id, agefilter_ll=18, agefilter_ul=99)
            db.session.add(user)
            db.session.commit()
            return True
        else:
            return False

def set_gender(chat_id, gender):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.gender = gender
        db.session.commit()
        return True
    else:
        return False

def set_age(chat_id, age):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.age = int(age)
        db.session.commit()
        return True
    else:
        return False

def set_agefilter(chat_id, agefilter_ll, agefilter_ul):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.agefilter_ll = agefilter_ll
        user.agefilter_ul = agefilter_ul
        db.session.commit()
        return True
    else:
        return False

def set_gender_match(chat_id, gendermatch):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.gendermatch = gendermatch
        db.session.commit()
        return True
    else:
        return False


def set_seeking(chat_id, seeking):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.seeking = seeking
        db.session.commit()
        return True
    else:
        return False


def set_mbti(chat_id, mbti):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.mbti = mbti
        db.session.commit()
        return True
    else:
        return False

def set_truth1(chat_id, truth1):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        user.truth1_1 = truth1
        db.session.commit()
        return True
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        user.truth1_2 = truth1
        db.session.commit()
        return True


def set_truth2(chat_id, truth2):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        user.truth2_1 = truth2
        db.session.commit()
        return True
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        user.truth2_2 = truth2
        db.session.commit()
        return True

def set_lie(chat_id, lie):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        user.lie_1 = lie
        db.session.commit()
        return True
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        user.lie_2 = lie
        db.session.commit()
        return True

def set_game_message(chat_id, message_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        user.message_id_1 = message_id
        db.session.commit()
        return True
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        user.message_id_2 = message_id
        db.session.commit()
        return True

def set_tiktok_url(chat_id, url):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        user.tiktok_url_1 = url
        db.session.commit()
        return True
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        user.tiktok_url_2 = url
        db.session.commit()
        return True

def get_message_id(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    if user != None:
        return user.message_id
    else:
        return 0


def get_seeking(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if user.seeking != None:
            return user.seeking
        else:
            return 
    else:
        return


def get_icebreaker(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        if bool(user.truth1_1) and bool(user.truth2_1) and bool(user.lie_1):
            return True
        else:
            return
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        if bool(user.truth1_2) and bool(user.truth2_2) and bool(user.lie_2):
            return True
        else:
            return

def get_truth1(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        if user.truth1_1 != None:
            return user.truth1_1
        else:
            return
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        if user.truth1_2 != None:
            return user.truth1_2
        else:
            return
  
def get_truth2(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        if user.truth2_1 != None:
            return user.truth2_1
        else:
            return
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        if user.truth2_2 != None:
            return user.truth2_2
        else:
            return

def get_lie(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        if user.lie_1 != None:
            return user.lie_1
        else:
            return
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        if user.lie_2 != None:
            return user.lie_2
        else:
            return

def get_game_message(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        if user.message_id_1 != None:
            return user.message_id_1
        else:
            return
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        if user.message_id_2 != None:
            return user.message_id_2
        else:
            return

def get_tiktok_url(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user != None:
        if user.tiktok_url_1 != None:
            return user.tiktok_url_1
        else:
            return
    else:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        if user.tiktok_url_2 != None:
            return user.tiktok_url_2
        else:
            return

def get_mbti(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if user.mbti != None:
            return user.mbti
        else:
            return 
    else:
        return

def get_gender_match(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if user.gendermatch != None:
            return user.gendermatch
        else:
            return 
    else:
        return

def get_user(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
            return user.chat_id
    else:
        return

def get_gender(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if user.gender != None:
            return user.gender
        else:
            return
    else:
        return

def get_age(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if user.age != None:
            return user.age
        else:
            return
    else:
        return

def get_agefilter(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if user.agefilter_ll != None and user.agefilter_ul != None:
            return [user.agefilter_ll, user.agefilter_ul]
        else:
            return
    else:
        return

def get_queue(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    if user != None:
        return user.chat_id
    else:
        return
    


def get_gender_chat(gender, gendermatch, age, agefilter_ll, agefilter_ul, seeking):
    if gendermatch != 'Any':
        user = Queue.query.filter(Queue.seeking==seeking, Queue.gender==gendermatch).filter(Queue.age>=agefilter_ll, Queue.age<=agefilter_ul, Queue.agefilter_ll<=age, Queue.agefilter_ul>=age).filter(or_(Queue.gendermatch==gender, Queue.gendermatch=='Any')).first()
        if user != None:
            user_info = [user.chat_id,user.gender,user.age,user.seeking,user.mbti]
            return user_info
        else:
            return [0,0,0,0,0]
    elif gendermatch == 'Any':
        user = Queue.query.filter(Queue.seeking==seeking, Queue.age>=agefilter_ll, Queue.age<=agefilter_ul, Queue.agefilter_ll<=age, Queue.agefilter_ul>=age).filter(or_(Queue.gendermatch==gender, Queue.gendermatch==gendermatch)).first()
        if user != None:
            user_info = [user.chat_id,user.gender,user.age,user.seeking,user.mbti]
            return user_info
        else:
            return [0,0,0,0,0]
    else:
        return [0,0,0,0,0]

def create_chat(chat_one, chat_two):
    if chat_two != 0:
        delete = Queue.query.filter_by(chat_id=chat_two).first()
        insert = Chats(chat_one=chat_one, chat_two=chat_two)
        try:
            db.session.delete(delete)
        except:
            pass
        db.session.add(insert)
        db.session.commit()
        return True
    else:
        return False
    
def get_active_chat(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    try:
        id_chat=user.id
        chat_info = [id_chat, user.chat_two]
    except:
        id_chat = None

    if id_chat == None:
        user2 = Chats.query.filter_by(chat_two=chat_id).first()
        try:
            id_chat = user2.id
            chat_info = [id_chat, user2.chat_one]
            return chat_info
        except:
            return None
    else:
        return chat_info

def get_last_chat(chat_id):
    user = Lastchat.query.filter_by(user=chat_id).first()
    try:
        userchat = user.user
        match = user.match
        chat_info = [userchat, match]
        return chat_info
    except:
        return None

def set_tiktok_win(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user == None:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        try:
            user.tiktok_two +=1
        except:
            user.tiktok_two = 1
        db.session.commit()
    else:
        try:
            user.tiktok_one +=1
        except:
            user.tiktok_one= 1
        db.session.commit()

def set_tiktok_round(chat_id):
    user = Chats.query.filter(or_(Chats.chat_one==chat_id, Chats.chat_two==chat_id)).first()
    try:
        user.tiktok_round += 1
    except:
        user.tiktok_round = 1
    db.session.commit()
    return user.tiktok_round

def get_tiktok_win(chat_id):
    user = Chats.query.filter_by(chat_one=chat_id).first()
    if user == None:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        tiktok = user.tiktok_two
        if tiktok == None:
            return 0
        else:
            return tiktok
    else:
        tiktok = user.tiktok_one
        if tiktok == None:
            return 0
        else:
            return tiktok

def get_tiktok_round(chat_id):
    user = Chats.query.filter(or_(Chats.chat_one==chat_id, Chats.chat_two==chat_id)).first()
    return user.tiktok_round

##### ADMIN LEVEL #####  

def clear_database():
    db.session.query(Users).delete()
    db.session.query(Queue).delete()
    db.session.query(Chats).delete()
    db.session.query(Banned).delete()
    db.session.query(Lastchat).delete()
    db.session.commit()

def admin_user_count():
    count = db.session.query(Users.chat_id).count()
    return count
 
        
def admin_active_chat():
    count = db.session.query(Chats.chat_one).count()
    return count

        
def admin_queue():
    count = db.session.query(Queue.chat_id).count()
    return count

def banned_user_count():
    count = db.session.query(Banned.chat_id).count()
    return count
        
def get_all_users():
    user = [value[0] for value in db.session.query(Users.chat_id)]
    return user

def get_banned():
    user = [value[0] for value in db.session.query(Banned.chat_id)]
    return user

def get_banned_reason(chat_id):
    user = Banned.query.filter_by(chat_id=chat_id).first()
    return user.reason

def set_banned(chat_id, reason):
    user  = Banned(chat_id=chat_id, reason=reason)
    db.session.add(user)
    db.session.commit()

def del_banned(chat_id):
    user  = Banned.query.filter_by(chat_id=chat_id).first()
    db.session.delete(user)
    db.session.commit()

#Create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True) #change to bigint to support larger chat_id 
    gender = db.Column(db.String(60))
    gendermatch = db.Column(db.String(60))
    seeking = db.Column(db.String(60))
    mbti = db.Column(db.String(60))
    truth1 = db.Column(db.String(300))
    truth2 = db.Column(db.String(300))
    lie = db.Column(db.String(300))
    age = db.Column(db.Integer)
    agefilter_ll = db.Column(db.Integer)
    agefilter_ul = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_one = db.Column(db.Integer, unique=True) 
    chat_two = db.Column(db.Integer, unique=True)
    tiktok_one = db.Column(db.Integer)
    tiktok_two = db.Column(db.Integer)
    tiktok_round = db.Column(db.Integer)
    truth1_1 = db.Column(db.String(500))
    truth2_1 = db.Column(db.String(500))
    lie_1 = db.Column(db.String(500))
    truth1_2 = db.Column(db.String(500))
    truth2_2 = db.Column(db.String(500))
    lie_2 = db.Column(db.String(500))
    message_id_1 = db.Column(db.String(255))
    message_id_2 = db.Column(db.String(255))
    tiktok_url_1 = db.Column(db.String(500))
    tiktok_url_2 = db.Column(db.String(500))
    
class Lastchat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, unique=True) 
    match = db.Column(db.Integer)

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)  
    gender = db.Column(db.String(60))
    gendermatch = db.Column(db.String(60))
    seeking = db.Column(db.String(60))
    message_id = db.Column(db.String(255))
    mbti = db.Column(db.String(60))
    age = db.Column(db.Integer)
    agefilter_ll = db.Column(db.Integer)
    agefilter_ul = db.Column(db.Integer)

class Banned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)
    reason = db.Column(db.String(255))