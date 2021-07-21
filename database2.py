from datetime import datetime
from sqlalchemy import or_

def add_queue(chat_id, gender, gendermatch, seeking, mbti, message_id):
    user = Queue(chat_id=chat_id,gender=gender,gendermatch=gendermatch,seeking=seeking,mbti=mbti,message_id=message_id)
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
        user2 = Lastchat(user=chatone,partner=chattwo) #lastchat entry for chatone person
        db.session.add(user2)
    else:
        user2 = Lastchat.query.filter_by(user=chatone)
        user2.user = chatone
        user2.partner = chattwo

    if get_last_chat(chattwo) == None:
        user3 = Lastchat(user=chattwo,partner=chatone) #lastchat entry for chattwo person
        db.session.add(user3)
    else:
        user3 = Lastchat.query.filter_by(user=chattwo)
        user3.user = chattwo
        user3.partner = chatone
    db.session.delete(user)
    db.session.commit()

def setup_complete(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if bool(user.chat_id) and bool(user.gender) and bool(user.gendermatch) and bool(user.seeking) and bool(user.mbti):
        return True
    else:
        return False
        
def set_user(chat_id):
        user = Users.query.filter_by(chat_id=chat_id).first()           
        if user == None:
            user = Users(chat_id=chat_id)
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
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.truth1 = truth1
        db.session.commit()
        return True
    else:
        return False


def set_truth2(chat_id, truth2):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.truth2 = truth2
        db.session.commit()
        return True
    else:
        return False

def set_lie(chat_id, lie):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.lie = lie
        db.session.commit()
        return True
    else:
        return False

def get_icebreaker(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        if bool(user.truth1) and bool(user.truth2) and bool(user.lie):
            return 'Set'
        elif bool(user.truth1) | bool(user.truth2) | bool(user.lie):
            return 'Incomplete'
        else:
            return 'Not set'
    else:
        return



def get_message_id(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    if user != None:
        return user.message_id
    else:
        return 0


def get_seeking(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.seeking != None:
        return user.seeking
    else:
        return 

 
def get_truth1(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.truth1 != None:
        return user.truth1
    else:
        return 
  
def get_truth2(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.truth2 != None:
        return user.truth2
    else:
        return

def get_lie(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.lie != None:
        return user.lie
    else:
        return



def get_mbti(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.mbti != None:
        return user.mbti
    else:
        return 


def get_gender_match(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.gendermatch != None:
        return user.gendermatch
    else:
        return 
 

def get_gender(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.gender != None:
        return user.gender
    else:
        return 

 

def get_queue(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    if user != None:
        return user.chat_id
    else:
        return
 
    
def get_gender_chat(gender, gendermatch, seeking):
    if gendermatch != 'Any':
        user = Queue.query.filter(Queue.seeking==seeking, Queue.gender==gendermatch).filter(or_(Queue.gendermatch==gender, Queue.gendermatch=='Any')).first()
        if user != None:
            user_info = [user.chat_id,user.gender,user.gendermatch,user.seeking,user.mbti]
            return user_info
        else:
            return [0,0,0,0,0]
    elif gendermatch == 'Any':
        user = Queue.query.filter(Queue.seeking==seeking).filter(or_(Queue.gendermatch==gender, Queue.gendermatch==gendermatch)).first()
        if user != None:
            user_info = [user.chat_id,user.gender,user.gendermatch,user.seeking,user.mbti]
            return user_info
        else:
            return [0,0,0,0,0]
    else:
        return [0,0,0,0,0]

def create_chat(chat_one, chat_two):
    if chat_two != 0:
        delete = Queue.query.filter_by(chat_id=chat_two).first()
        insert = Chats(chat_one=chat_one, chat_two=chat_two)
        db.session.delete(delete)
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
        partner = user.partner
        chat_info = [userchat, partner]
        return chat_info
    except:
        return None

def clear_database():
    db.session.query(Users).delete()
    db.session.query(Queue).delete()
    db.session.query(Chats).delete()
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

def set_banned(chat_id):
    user  = Banned(chat_id=chat_id)
    db.session.add(user)
    db.session.commit()

def del_banned(chat_id):
    user  = Banned(chat_id=chat_id)
    db.session.delete(user)
    db.session.commit()

#Create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True) 
    gender = db.Column(db.String(60))
    gendermatch = db.Column(db.String(60))
    seeking = db.Column(db.String(60))
    mbti = db.Column(db.String(60))
    truth1 = db.Column(db.String(300))
    truth2 = db.Column(db.String(300))
    lie = db.Column(db.String(300))
    age = db.Column(db.Integer)
    agefilter = db.Column(db.String(60))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_one = db.Column(db.Integer, unique=True) 
    chat_two = db.Column(db.Integer, unique=True)
    
class Lastchat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, unique=True) 
    match = db.Column(db.Integer, unique=True)

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)  
    gender = db.Column(db.String(60))
    gendermatch = db.Column(db.String(60))
    seeking = db.Column(db.String(60))
    message_id = db.Column(db.String(255))
    mbti = db.Column(db.String(60))
    age = db.Column(db.Integer)
    agefilter = db.Column(db.String(60))

class Banned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)