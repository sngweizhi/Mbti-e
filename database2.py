from bot2 import server
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(server)


def add_queue(self, chat_id, gender, gendermatch, seeking, mbti, message_id): 
    with self.connection:
        return self.cursor.execute("INSERT INTO `queue` (`chat_id`, `gender`, `gendermatch`, `seeking`, `mbti`,`message_id` ) VALUES (?,?,?,?,?,?)", (chat_id, gender, gendermatch, seeking, mbti, message_id))
    
def delete_queue(self, chat_id):
    with self.connection:
        return self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_id,))
    
def delete_chat(self, id_chat):
    with self.connection:
        return self.cursor.execute("DELETE FROM `chats` WHERE `id` = ?", (id_chat,))

def setup_complete(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                if bool(row[1]) and bool(row[2]) and bool(row[3]):
                    return True
            else:
                return False
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

def set_gender(self, chat_id, gender):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)) == False:
            self.cursor.execute("INSERT INTO `users` (`chat_id`, `gender`) VALUES (?,?)", (chat_id, gender))
            return True
        else:
            self.cursor.execute("UPDATE `users` SET `gender` = ? WHERE `chat_id` = ?",(gender, chat_id))
            return True
           

def set_gender_match(self, chat_id, gendermatch):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            self.cursor.execute("UPDATE `users` SET `gendermatch` = ? WHERE `chat_id` = ?",(gendermatch, chat_id))
            return True
        else:
            return False

def set_seeking(self, chat_id, seeking):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            self.cursor.execute("UPDATE `users` SET `seeking` = ? WHERE `chat_id` = ?",(seeking, chat_id))
            return True
        else:
            return False

def set_mbti(self, chat_id, mbti):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            self.cursor.execute("UPDATE `users` SET `mbti` = ? WHERE `chat_id` = ?",(mbti, chat_id))
            return True
        else:
            return False

def set_truth1(self, chat_id, truth1):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            self.cursor.execute("UPDATE `users` SET `truth1` = ? WHERE `chat_id` = ?",(truth1, chat_id))
            return True
        else:
            return False

def set_truth2(self, chat_id, truth2):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            self.cursor.execute("UPDATE `users` SET `truth2` = ? WHERE `chat_id` = ?",(truth2, chat_id))
            return True
        else:
            return False

def set_lie(self, chat_id, lie):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            self.cursor.execute("UPDATE `users` SET `lie` = ? WHERE `chat_id` = ?",(lie, chat_id))
            return True
        else:
            return False

def get_icebreaker(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                if bool(row[6]) and bool(row[7]) and bool(row[8]):
                    return 'Set'
                elif bool(row[6]) | bool(row[7]) | bool(row[8]):
                    return 'Incomplete'
                else:
                    return 'Not set'
        else:
            return False

def get_message_id(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT `message_id` FROM `queue` WHERE `chat_id` = ?", (chat_id,)).fetchone()
        if user != None:
            return user[0]
        else:
            return 0

def get_seeking(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[4]
        else:
            return False

def get_truth1(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[6]
        else:
            return False

def get_truth2(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[7]
        else:
            return False
    
def get_lie(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[8]
        else:
            return False

def get_mbti(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[5]
        else:
            return False

def get_gender_match(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[3]
        else:
            return False

def get_gender(self, chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT `gender` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchone()
##            user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
##            if bool(len(user)):
##                for row in user:
##                    return row[2]
        if user[0] != None:
            return user[0]
        else:
            return False

def get_queue(self,chat_id):
    with self.connection:
        user = self.cursor.execute("SELECT * FROM `queue` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
        if bool(len(user)):
            for row in user:
                return row[1]
        else:
            return False
    
def get_gender_chat(self, gender, gendermatch, seeking):
    with self.connection:
        if gendermatch != 'any':
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE `gendermatch` = ? AND `gender` = ? AND `seeking` = ?", (gender,gendermatch,seeking)).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    user_info = [row[1], row[2],row[3],row[4],row[6]]
                    return user_info
            else:
                return [0,0,0,0,0]

        elif gendermatch == 'any':
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE `gendermatch` = ? AND `seeking` = ?", (gender, seeking)).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    user_info = [row[1], row[2],row[3],row[4],row[6]]
                    return user_info
            else:
                return [0,0,0,0,0]

        else:
            return[0,0,0,0,0]

# def get_chat(self):
#     with self.connection:
#         chat = self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
#         if bool(len(chat)):
#             for row in chat:
#                 user_info = [row[1], row[2]]
#                 return user_info
#         else:
#             return [0]

def create_chat(self, chat_one, chat_two):
    with self.connection:
        if chat_two != 0:
            # Create a chat
            self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_two,))
            self.cursor.execute("INSERT INTO `chats` (`chat_one`, `chat_two`) VALUES (?,?)", (chat_one, chat_two,))
            return True

        else:
            # Join the queue
            return False
    
def get_active_chat(self, chat_id):
    with self.connection:
        chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_one` = ?", (chat_id,))
        id_chat = 0
        for row in chat:
            id_chat = row[0]
            chat_info = [row[0], row[2]]
            
        if id_chat == 0:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_two` = ?", (chat_id,))
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[1]]
            if id_chat == 0:
                return False
            else:
                return chat_info
        else:
            return chat_info

# Admin level functions

def clear_database(self):
    with self.connection:
        self.cursor.execute("DELETE FROM `users`")
        self.cursor.execute("DELETE FROM `queue`")
        self.cursor.execute("DELETE FROM `chats`")

def admin_user_count(self):
    with self.connection:
        count = self.cursor.execute("SELECT COUNT(DISTINCT`chat_id`) FROM `users`").fetchone()
        return count[0]
        
def admin_active_chat(self):
    with self.connection:
        count = self.cursor.execute("SELECT COUNT(DISTINCT `chat_one`) FROM `chats`").fetchone()
        return count[0]
        
def admin_queue(self):
        with self.connection:
            count = self.cursor.execute("SELECT COUNT(DISTINCT `chat_id`) FROM `queue`").fetchone()
            return count[0]
        
def get_all_users(self):
    with self.connection:
        alluser = []
        user = self.cursor.execute("SELECT `chat_id` FROM `users`").fetchall()
        for row in user:
            alluser.append(row[0])
        return alluser

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