from bot2 import server
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(server)


def add_queue(chat_id, gender, gendermatch, seeking, mbti, message_id):
    user = Queue(chat_id=chat_id,gender=gender,gendermatch=gendermatch,seeking=seeking,mbti=mbti,message_id=message_id)
    db.session.add(user)
    db.session.commit()
    
def delete_queue(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    db.session.delete(user)
    db.session.commit()
    
def delete_chat(chat_id):
    user = Chats.query.filter_by(chat_id=chat_id).first()
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

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)) == False:
    #        self.cursor.execute("INSERT INTO `users` (`chat_id`, `gender`) VALUES (?,?)", (chat_id, gender))
    #        return True
    #    else:
    #        self.cursor.execute("UPDATE `users` SET `gender` = ? WHERE `chat_id` = ?",(gender, chat_id))
    #        return True
           

def set_gender_match(chat_id, gendermatch):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.gendermatch = gendermatch
        db.session.commit()
        return True
    else:
        return False
        #user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        #if bool(len(user)):
        #    self.cursor.execute("UPDATE `users` SET `gendermatch` = ? WHERE `chat_id` = ?",(gendermatch, chat_id))
        #    return True
        #else:
        #    return False

def set_seeking(chat_id, seeking):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.seeking = seeking
        db.session.commit()
        return True
    else:
        return False

        #user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        #if bool(len(user)):
        #    self.cursor.execute("UPDATE `users` SET `seeking` = ? WHERE `chat_id` = ?",(seeking, chat_id))
        #    return True
        #else:
        #    return False

def set_mbti(chat_id, mbti):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.mbti = mbti
        db.session.commit()
        return True
    else:
        return False

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        self.cursor.execute("UPDATE `users` SET `mbti` = ? WHERE `chat_id` = ?",(mbti, chat_id))
    #        return True
    #    else:
    #        return False

def set_truth1(chat_id, truth1):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user != None:
        user.truth1 = truth1
        db.session.commit()
        return True
    else:
        return False

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        self.cursor.execute("UPDATE `users` SET `truth1` = ? WHERE `chat_id` = ?",(truth1, chat_id))
    #        return True
    #    else:
    #        return False

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

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            if bool(row[6]) and bool(row[7]) and bool(row[8]):
    #                return 'Set'
    #            elif bool(row[6]) | bool(row[7]) | bool(row[8]):
    #                return 'Incomplete'
    #            else:
    #                return 'Not set'
    #    else:
    #        return False

def get_message_id(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    if user != None:
        return user.message_id
    else:
        return 0
    #with self.connection:
    #    user = self.cursor.execute("SELECT `message_id` FROM `queue` WHERE `chat_id` = ?", (chat_id,)).fetchone()
    #    if user != None:
    #        return user[0]
    #    else:
    #        return 0

def get_seeking(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.seeking != None:
        return user.seeking
    else:
        return 

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[4]
    #    else:
    #        return False

def get_truth1(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.truth1 != None:
        return user.truth1
    else:
        return 
    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[6]
    #    else:
    #        return False

def get_truth2(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.truth2 != None:
        return user.truth2
    else:
        return

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[7]
    #    else:
    #        return False
    
def get_lie(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.lie != None:
        return user.lie
    else:
        return

    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[8]
    #    else:
    #        return False

def get_mbti(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.mbti != None:
        return user.mbti
    else:
        return 
    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[5]
    #    else:
    #        return False

def get_gender_match(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.gendermatch != None:
        return user.gendermatch
    else:
        return 
    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[3]
    #    else:
    #        return False

def get_gender(chat_id):
    user = Users.query.filter_by(chat_id=chat_id).first()
    if user.gender != None:
        return user.gender
    else:
        return 

    #with self.connection:
    #    user = self.cursor.execute("SELECT `gender` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchone()
    #    if user[0] != None:
    #        return user[0]
    #    else:
    #        return False

def get_queue(chat_id):
    user = Queue.query.filter_by(chat_id=chat_id).first()
    if user != None:
        return user.chat_id
    else:
        return
    #with self.connection:
    #    user = self.cursor.execute("SELECT * FROM `queue` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
    #    if bool(len(user)):
    #        for row in user:
    #            return row[1]
    #    else:
    #        return False
    
def get_gender_chat(gender, gendermatch, seeking):
    if gendermatch != 'Any':
        user = Queue.query.filter(Queue.gender==gendermatch,Queue.gendermatch==gender,Queue.seeking==seeking).first()
        if user != None:
            user_info = [user.chat_id,user.gender,user.gendermatch,user.seeking,user.mbti]
            return user_info
        else:
            return [0,0,0,0,0]
    elif gendermatch == 'Any':
        user = db.session.query(Queue).filter(Queue.seeking==seeking).filter((Queue.gendermatch==gender | Queue.gendermatch==gendermatch)).first()
        if user != None:
            user_info = [user.chat_id,user.gender,user.gendermatch,user.seeking,user.mbti]
            return user_info
        else:
            return [0,0,0,0,0]
    else:
        return [0,0,0,0,0]

    #with self.connection:
    #    if gendermatch != 'Any':
    #        chat = self.cursor.execute("SELECT * FROM `queue` WHERE `gendermatch` = ? AND `gender` = ? AND `seeking` = ?", (gender,gendermatch,seeking)).fetchmany(1)
    #        if bool(len(chat)):
    #            for row in chat:
    #                user_info = [row[1], row[2],row[3],row[4],row[6]]
    #                return user_info
    #        else:
    #            return [0,0,0,0,0]

    #    elif gendermatch == 'Any':
    #        chat = self.cursor.execute("SELECT * FROM `queue` WHERE `gendermatch` = ? AND `seeking` = ?", (gender, seeking)).fetchmany(1)
    #        if bool(len(chat)):
    #            for row in chat:
    #                user_info = [row[1], row[2],row[3],row[4],row[6]]
    #                return user_info
    #        else:
    #            return [0,0,0,0,0]

    #    else:
    #        return[0,0,0,0,0]

# def get_chat(self):
#     with self.connection:
#         chat = self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
#         if bool(len(chat)):
#             for row in chat:
#                 user_info = [row[1], row[2]]
#                 return user_info
#         else:
#             return [0]

def create_chat(chat_one, chat_two):
    if chat_two != 0:
        delete = Queue.query.filter_by(chat_id=chat_id).first()
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
        chat_info = user.chat_two
    except:
        id_chat = None

    if id_chat == None:
        user = Chats.query.filter_by(chat_two=chat_id).first()
        try:
            id_chat = user.id
            chat_info = user.chat_one
        except:
            if id_chat == None:
                return None
            else:
                return chat_info
    else:
        return chat_info


    #with self.connection:
    #    chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_one` = ?", (chat_id,))
    #    id_chat = 0
    #    for row in chat:
    #        id_chat = row[0]
    #        chat_info = [row[0], row[2]]
            
    #    if id_chat == 0:
    #        chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_two` = ?", (chat_id,))
    #        for row in chat:
    #            id_chat = row[0]
    #            chat_info = [row[0], row[1]]
    #        if id_chat == 0:
    #            return False
    #        else:
    #            return chat_info
    #    else:
    #        return chat_info

# Admin level functions

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
        
def get_all_users():
    user = [value[0] for value in db.session.query(Users.chat_id)]
    return user

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