import config
import telebot
import random
from telebot import types
from database import Database
import os

from flask import Flask, request

server = Flask(__name__)

db = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)

@server.route('/' + config.TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://mbtinder.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))




userStep = {}
userPoll = {}


def main_menu():
    """
    Create inline menu for new chat
    :return: InlineKeyboardMarkup
    """
    button1 = types.InlineKeyboardButton(text='\U00002709 Start matching!',
                                          callback_data='NewChat')
    button2 = types.InlineKeyboardButton(text='⚙️ Setup',
                                          callback_data='setupback')
    menu = types.InlineKeyboardMarkup()
    menu.add(button1,button2)

    return menu

def gender_menu():
  """
  Create a menu for setting up profile
  """
  male_button = types.InlineKeyboardButton(text='👦🏻 Male',
                                          callback_data='Male')
  female_button = types.InlineKeyboardButton(text='👧🏻 Female',
                                          callback_data='Female')
  markup = types.InlineKeyboardMarkup()
  markup.add(male_button, female_button)
  return markup

def match_gender_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='👦🏻 Male',
                                          callback_data='Malematch')
  button2 = types.InlineKeyboardButton(text='👧🏻 Female',
                                          callback_data='Femalematch')
  button3 = types.InlineKeyboardButton(text='👦🏻👧🏻 Any',
                                          callback_data='Anymatch')
  markup.add(button1,button2,button3)

  return markup 

def mbti_menu():
  mbti_list = ['ISFP', 'ISFJ', 'ISTP', 'ISTJ','ESFP', 'ESFJ', 'ESTP', 'ESTJ', 'INFP', 'INFJ', 'INTP', 'INTJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ']
  button_list = []
  row_list = []
  
  i = 0
  for mbti in mbti_list:
      row_list.append(types.InlineKeyboardButton(text=mbti, callback_data = mbti))
      i += 1
      if i%4 == 0:
        button_list.append(row_list)
        row_list = []
  markup = types.InlineKeyboardMarkup(button_list)
  return markup

def seeking_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='💌 Dating',
                                          callback_data='Dating')
  button2 = types.InlineKeyboardButton(text='🤝 Friendship',
                                          callback_data='Friendship')
  markup.add(button1,button2)

  return markup

def setup_menu():
  
  button1 = types.InlineKeyboardButton(text='Edit Gender',
                                          callback_data='Gender')
  button2 = types.InlineKeyboardButton(text='Edit Match Gender',
                                          callback_data='Match Gender')
  button3 = types.InlineKeyboardButton(text='Edit Purpose',
                                          callback_data='Purpose')
  button4 = types.InlineKeyboardButton(text='Edit MBTI',
                                          callback_data='MBTI')
  button5 = types.InlineKeyboardButton(text='Edit Ice Breaker',
                                          callback_data='icebreaker')                                        
  button6 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='Bot')
  markup = types.InlineKeyboardMarkup([[button1,button2],[button3,button4],[button5,button6]])                                   
  return markup

def icebreaker_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='2Truth1Lie',
                                          callback_data='icebreaker_setup')
  button2 = types.InlineKeyboardButton(text='» Skip ',
                                          callback_data='complete')
  markup.add(button1,button2)

  return markup

def icebreaker_first():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Edit',
                                          callback_data='icebreaker')
  button2 = types.InlineKeyboardButton(text='» Complete ',
                                          callback_data='complete')
  markup.add(button1,button2)

  return markup

def icebreaker_setup_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Truth 1',
                                          callback_data='truth1')
  button2 = types.InlineKeyboardButton(text='Truth 2',
                                          callback_data='truth2')
  button3 = types.InlineKeyboardButton(text='Lie',
                                          callback_data='lie')
  button4 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='Bot')
  markup.add(button1,button2,button3,button4)

  return markup

def setup_settings():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='« Back to profile setup',
                                          callback_data='setupback')
  button2 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='Bot')
  markup.add(button1, button2)
  return markup

def stop_search():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Stop searching',
                                          callback_data='Stop')
  markup.add(button1)

  return markup

@bot.message_handler(commands = ['start'])
def start(message):
    if db.set_user(message.chat.id) != False:
      bot.send_message(message.chat.id, config.welcome, parse_mode = 'MarkdownV2')
      return
      
    if db.get_active_chat(message.chat.id) != False:
       bot.send_message(message.chat.id, '❌ You are still in a chat!')
       return

    elif db.get_queue(message.chat.id) != False:
      bot.send_message(message.chat.id, '❌ You are already in the queue!')
      return

    elif db.setup_complete(message.chat.id) == False:
      bot.send_message(message.chat.id, 'Please setup your profile first! /setup')

    else:
      bot.send_message(message.chat.id, 'Click the button below to start matching!',reply_markup=main_menu())

@bot.message_handler(commands = ['stop'])
def stop(message):
    if db.get_queue(message.chat.id) != False:
      bot.delete_message(call.message.chat.id, call.message.message_id -1)
      db.delete_queue(call.message.chat.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❌ Search stopped.', reply_markup = main_menu())
      return
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        bot.send_message(chat_info[1], '❌ Your match has ended the chat. Input /start to start searching for another match!')
        bot.send_message(message.chat.id, '❌ You have ended the chat. Input /start to start searching for another match!')
    else:
        bot.send_message(message.chat.id, '❌ You have not started a chat!')


@bot.message_handler(commands=['setup'])
def echo(message):
    """
    Make the user setup their profile
    :param message:
    :return:
    """
    if db.get_active_chat(message.chat.id) != False:
       bot.send_message(message.chat.id, '❌ You are still in a chat!')
       return
    if db.get_gender(message.chat.id) == False:
      bot.send_message(message.chat.id, 'Welcome to MBTInder! Please select your gender!', reply_markup=gender_menu())
    else:
      mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
      gender = db.get_gender(message.chat.id)
      gendermatch = db.get_gender_match(message.chat.id)
      seeking = db.get_seeking(message.chat.id)
      mbti = db.get_mbti(message.chat.id)
      iceb = db.get_icebreaker(message.chat.id)
      bot.send_message(message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

@bot.message_handler(commands=['icebreaker'])
def echo(message):
    if bool(db.get_active_chat(message.chat.id)):
      chat_info = db.get_active_chat(message.chat.id)
      statements = [db.get_truth1(message.chat.id),db.get_truth2(message.chat.id),db.get_lie(message.chat.id)]
      random.shuffle(statements)
      ans = statements.index(db.get_lie(message.chat.id))
      userPoll[chat_info[1]] = [ans,statements]
      bot.send_poll(chat_info[1], '2Truths1Lie. Select the Lie.', options = statements, correct_option_id=ans, type = 'quiz', is_anonymous= False)
      bot.send_message(message.chat.id, '2Truths1Lie sent!')
    else:
      bot.send_message(message.chat.id, 'You have not started a chat!')

@bot.poll_answer_handler(func=lambda message: True)
def poll_answer(message):
  user_ans = message.option_ids[0]
  chat_info = db.get_active_chat(message.user.id)
  ans = userPoll[str(message.user.id)][0]
  statement = userPoll[str(message.user.id)][1]
  if user_ans == ans:
    bot.send_message(message.user.id, 'Hooray! You selected the right answer!')
    bot.send_message(chat_info[1], "User selected the right answer\! '*{}*'".format(statement[user_ans]), parse_mode = 'MarkdownV2')
  else:
    bot.send_message(message.user.id, 'You selected the wrong answer!')
    bot.send_message(chat_info[1], "User selected the wrong answer\! '*{}*'".format(statement[user_ans]), parse_mode = 'MarkdownV2')
  userPoll.pop(message.user.id, None) #reset


@bot.message_handler(commands=['deletedb'])
def echo(message):
    """
    delete database
    """
    db.clear_database()
    bot.send_message(message.chat.id,'Deleting database...')

def get_user_step(uid):
    if uid in userStep:
      return userStep[uid]
    else:
      return 0


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) > 0)
def icebreakerset(message):
  step = get_user_step(message.chat.id)
  if step < 4:
    if step == 1:
      if db.set_truth1(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 1 set!')
    elif step == 2:
      if db.set_truth2(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 2 set!')
    elif step == 3:
      if db.set_lie(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Lie set!')
    mess = "Edit your 2Truth1Lie\.\n \n*Truth 1*: {}\n*Truth 2*: {}\n*Lie*: {}"
    truth1 = db.get_truth1(message.chat.id)
    truth2 = db.get_truth2(message.chat.id)
    lie = db.get_lie(message.chat.id)
    bot.send_message(message.chat.id, mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu(), parse_mode = 'MarkdownV2')
    userStep.pop(message.chat.id,None)

  elif step == 4:
    if db.set_truth1(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 1 set!')
    bot.send_message(message.chat.id, 'Now send me your *Truth 2* statement', parse_mode ='MarkdownV2')
    userStep[message.chat.id] = 5

  elif step == 5:
    if db.set_truth2(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 2 set!')
    bot.send_message(message.chat.id, 'Now send me your *Lie* statement', parse_mode ='MarkdownV2')
    userStep[message.chat.id] = 6

  elif step == 6:
    if db.set_lie(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Lie set!')
    mess = "Your 2Truth1Lie is set\!\n \n*Truth 1*: {}\n*Truth 2*: {}\n*Lie*: {}"
    truth1 = db.get_truth1(message.chat.id)
    truth2 = db.get_truth2(message.chat.id)
    lie = db.get_lie(message.chat.id)
    bot.send_message(message.chat.id, mess.format(truth1, truth2, lie),reply_markup=icebreaker_first(), parse_mode = 'MarkdownV2')
    userStep.pop(message.chat.id,None)
  else:
    userStep[message.chat.id]=0
    

@bot.message_handler(content_types=['text', 'sticker', 'video', 'photo', 'audio', 'voice','video_note'])
def echo(message):

    if message.content_type == 'sticker':
        if db.get_active_chat(message.chat.id) != False:
          chat_info = db.get_active_chat(message.chat.id)          
          bot.send_sticker(chat_info[1], message.sticker.file_id)
          print(message.sticker.file_id)

        else:
          return

    elif message.content_type == 'photo':
      if db.get_active_chat(message.chat.id) != False:
          chat_info = db.get_active_chat(message.chat.id)     
          
          file_id = None

          for item in message.photo:
            file_id = item.file_id

          bot.send_photo(chat_info[1],
                       file_id,
                       caption=message.caption)

      else:
          return

    elif message.content_type == 'audio':
        if db.get_active_chat(message.chat.id) != False:
          chat_info = db.get_active_chat(message.chat.id)          
          bot.send_audio(chat_info[1],
                       message.audio.file_id,
                       caption=message.caption)

        else:
          return

        
    elif message.content_type == 'video':
        if db.get_active_chat(message.chat.id) != False:
          chat_info = db.get_active_chat(message.chat.id)  
          bot.send_video(chat_info[1],
                        message.video.file_id,
                        caption=message.caption)
        else:
          return

    elif message.content_type == 'voice':
        if db.get_active_chat(message.chat.id) != False:
          chat_info = db.get_active_chat(message.chat.id)  
          bot.send_voice(chat_info[1],
                        message.voice.file_id)

        else:
          return

    elif message.content_type == 'video_note':
      if db.get_active_chat(message.chat.id) != False:
          chat_info = db.get_active_chat(message.chat.id)  
          bot.send_video_note(chat_info[1],
                        message.video_note.file_id)
                        
    elif message.content_type == 'text':
        

        if message.text != '/start' and message.text != '/stop' and \
                    message.text != '/setup' and message.text != '/icebreaker' and message.text != '/help':

            if db.get_active_chat(message.chat.id) != False:
              chat_info = db.get_active_chat(message.chat.id)
              text = 'User: ' + message.text
              if message.reply_to_message is None:
                  bot.send_message(chat_info[1],
                                  text)
              elif message.from_user.id != message.reply_to_message.from_user.id:
                  bot.send_message(
                      chat_info[1],
                      text,
                      reply_to_message_id=message.reply_to_message.message_id -1)
              else:
                  bot.send_message(message.chat.id, '❌ You cannot forward your own message!')
            else:
              bot.send_message(message.chat.id, '❌ You are not currently in a chat with anyone!')
  

@bot.callback_query_handler(func=lambda call: True)
def echo(call):

    if call.data == 'Male':
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_gender(call.message.chat.id)):
        if db.set_gender(call.message.chat.id, 'Male'):
            # bot.send_message(call.message.chat.id, 'You updated your gender to *Male*\.', reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your gender to *Male*\.', reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_gender(call.message.chat.id, 'Male'):
          # bot.send_message(call.message.chat.id, 'You selected *Male* as your gender\.',  parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Male* as your gender\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Who would you like to match with?', reply_markup = match_gender_menu())
        else:
          return
        
    elif call.data == 'Female':
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_gender(call.message.chat.id)):
        if db.set_gender(call.message.chat.id, 'Female'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your gender to *Female*\.', reply_markup = setup_settings(), parse_mode = 'MarkdownV2')
      else:
        if db.set_gender(call.message.chat.id, 'Female'):
          # bot.send_message(call.message.chat.id, 'You selected *Female* as your gender\.',  parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Female* as your gender\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Who would you like to match with?', reply_markup =match_gender_menu())
        else:
          return

    elif call.data == 'Malematch': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_gender_match(call.message.chat.id)):
        if db.set_gender_match(call.message.chat.id, 'Male'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Males*\.', reply_markup=setup_settings(),  parse_mode = 'MarkdownV2')
            # bot.send_message(call.message.chat.id, 'You chose to match with *Males*\.', reply_markup=setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_gender_match(call.message.chat.id, 'Male'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Males*\.', parse_mode = 'MarkdownV2')
          # bot.send_message(call.message.chat.id, 'You chose to match with *Males*\.',  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
        else:
          return

    elif call.data == 'Femalematch': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_gender_match(call.message.chat.id)):
        if db.set_gender_match(call.message.chat.id, 'Female'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Females*\.',reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
            # bot.send_message(call.message.chat.id, 'You chose to match with *Females*\.',reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_gender_match(call.message.chat.id, 'Female'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Females*\.', parse_mode = 'MarkdownV2')
          # bot.send_message(call.message.chat.id, 'You chose to match with *Females*\.',  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
        else:
          return

    elif call.data == 'Anymatch': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_gender_match(call.message.chat.id)):
        if db.set_gender_match(call.message.chat.id, 'Any'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Everyone*\.', reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
            # bot.send_message(call.message.chat.id, 'You chose to match with *Everyone*\.', reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_gender_match(call.message.chat.id, 'Any'):
          # bot.send_message(call.message.chat.id, 'You chose to match with *Everyone*\.',  parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Everyone*\.',  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
        else:
          return

    elif call.data == 'Dating': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_seeking(call.message.chat.id)):
        if db.set_seeking(call.message.chat.id, 'Dating'):
          # bot.send_message(call.message.chat.id, 'You updated your purpose to *Dating*\.', reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your purpose to *Dating*\.', reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_seeking(call.message.chat.id, 'Dating'):
          # bot.send_message(call.message.chat.id, 'You selected *Dating* as your purpose\.',  parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Dating* as your purpose\.',  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Select your MBTI type!', reply_markup = mbti_menu())
        else:
          return

    elif call.data == 'Friendship': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_seeking(call.message.chat.id)):
        if db.set_seeking(call.message.chat.id, 'Friendship'):
            # bot.send_message(call.message.chat.id, 'You updated your purpose to *Friendship*\.',reply_markup=setup_settings(),  parse_mode = 'MarkdownV2')
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your purpose to *Friendship*\.',reply_markup=setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_seeking(call.message.chat.id, 'Friendship'):
          # bot.send_message(call.message.chat.id, 'You selected *Friendship* as your purpose\.', parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Friendship* as your purpose\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Select your MBTI type!', reply_markup = mbti_menu())
        else:
          return

    elif call.data == 'Purpose': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      # bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'What are you seeking?', reply_markup = seeking_menu())
    
    elif call.data == 'Gender': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      # bot.send_message(call.message.chat.id, 'Select your gender.', reply_markup = gender_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Select your gender.', reply_markup = gender_menu())

    elif call.data == 'Match Gender': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      # bot.send_message(call.message.chat.id, 'Who would you like to match with?', reply_markup = match_gender_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Who would you like to match with?', reply_markup = match_gender_menu())

    elif call.data == 'MBTI': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      # bot.send_message(call.message.chat.id, 'Select your MBTI type!', reply_markup = mbti_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Select your MBTI type!', reply_markup = mbti_menu())

    elif call.data == 'icebreaker':
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      mess = "Edit your 2Truth1Lie\.\n \n*Truth 1*: {}\n*Truth 2*: {}\n*Lie*: {}"
      truth1 = db.get_truth1(call.message.chat.id)
      truth2 = db.get_truth2(call.message.chat.id)
      lie = db.get_lie(call.message.chat.id)
      if bool(db.get_truth1(call.message.chat.id)):
        # bot.send_message(call.message.chat.id, mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu(), parse_mode = 'MarkdownV2')
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu(), parse_mode = 'MarkdownV2')
      else:
        # bot.send_message(call.message.chat.id, 'Setup your 2 Truths and 1 Lie!', reply_markup=icebreaker_setup_menu())
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Setup your 2 Truths and 1 Lie!', reply_markup=icebreaker_setup_menu())

    elif call.data in ['truth1','truth2','lie']:
        bot.answer_callback_query(call.id)
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        if call.data == 'truth1':
          statement = 'Truth 1'
          userStep[call.message.chat.id] = 1
        if call.data == 'truth2':
          statement = 'Truth 2'
          userStep[call.message.chat.id] = 2
        if call.data == 'lie':
          statement = 'Lie'
          userStep[call.message.chat.id] = 3
        # bot.send_message(call.message.chat.id, 'Send me your *{}* statement'.format(statement), parse_mode ='MarkdownV2')
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *{}* statement'.format(statement), parse_mode ='MarkdownV2')

    elif call.data == 'icebreaker_setup':
        bot.answer_callback_query(call.id)
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        # bot.send_message(call.message.chat.id, 'Send me your *Truth 1* statement', parse_mode ='MarkdownV2')
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *Truth 1* statement', parse_mode ='MarkdownV2')
        userStep[call.message.chat.id] = 4

    elif call.data == 'complete':
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      # bot.send_message(call.message.chat.id, 'Your profile is complete! Press the button below to start matching!',reply_markup=main_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Your profile is complete! Press the button below to start matching!',reply_markup=main_menu())

    elif call.data == 'Bot':
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      # bot.send_message(call.message.chat.id, 'Click the button below to start matching!',reply_markup=main_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Click the button below to start matching!',reply_markup=main_menu())

    elif call.data == 'setupback': 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
      gender = db.get_gender(call.message.chat.id)
      gendermatch = db.get_gender_match(call.message.chat.id)
      seeking = db.get_seeking(call.message.chat.id)
      mbti = db.get_mbti(call.message.chat.id)
      iceb = db.get_icebreaker(call.message.chat.id)
      # bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

    elif call.data in ['ISFP', 'ISFJ', 'ISTP', 'ISTJ','ESFP', 'ESFJ', 'ESTP', 'ESTJ', 'INFP', 'INFJ', 'INTP', 'INTJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ']: 
      bot.answer_callback_query(call.id)
      # bot.delete_message(call.message.chat.id, call.message.message_id)
      if bool(db.get_mbti(call.message.chat.id)):
        if db.set_mbti(call.message.chat.id, call.data):
            # bot.send_message(call.message.chat.id, 'You updated your MBTI type to *{}*\.'.format(call.data), reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your MBTI type to *{}*\.'.format(call.data), reply_markup = setup_settings(),  parse_mode = 'MarkdownV2')
      else:
        if db.set_mbti(call.message.chat.id, call.data):
          # bot.send_message(call.message.chat.id, 'You selected *{}* as your MBTI type\.'.format(call.data),  parse_mode = 'MarkdownV2')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *{}* as your MBTI type\.'.format(call.data),  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'You may choose to set an ice breaker!', reply_markup = icebreaker_menu())
        else:
          return

    elif call.data == 'NewChat':
      if db.get_queue(call.message.chat.id) != False:
        bot.answer_callback_query(call.id)
        # bot.send_message(call.message.chat.id, '❌ You are already in the queue!')
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❌ You are already in the queue!')
      
      elif db.setup_complete(call.message.chat.id) == False:
        bot.answer_callback_query(call.id)
        # bot.send_message(call.message.chat.id, 'Your profile is incomplete!')
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Your profile is incomplete!')

      elif db.get_active_chat(call.message.chat.id) == False:
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        gendermatch = db.get_gender_match(call.message.chat.id)
        gender = db.get_gender(call.message.chat.id)
        seeking = db.get_seeking(call.message.chat.id)
        mbti = db.get_mbti(call.message.chat.id)
        user_info = db.get_gender_chat(gender, gendermatch, seeking)
        chat_two = user_info[0]
        gender2 = user_info[1]
        seeking2 = user_info[3]
        mbti2 = user_info[4]
        msg = db.get_message_id(chat_two)
        if db.create_chat(call.message.chat.id, chat_two) == False:
                  bot.send_sticker(call.message.chat.id, config.search_sticker)
                  sent = bot.send_message(call.message.chat.id, 'Searching for a suitable match...', reply_markup = stop_search())
                  db.add_queue(call.message.chat.id, gender, gendermatch, seeking, mbti, sent.message_id)
        else:
                  mess = 'A match is found!\n\nGender: {}\nPurpose: {}\nMBTI: {}\n\nInput /stop to end the chat.'
                  bot.delete_message(chat_two, msg)
                  bot.delete_message(chat_two, int(msg)-1)
                  bot.send_sticker(call.message.chat.id, config.match_sticker)
                  bot.send_message(call.message.chat.id, mess.format(gender2,seeking2,mbti2))
                  bot.send_sticker(chat_two, config.match_sticker)
                  bot.send_message(chat_two, mess.format(gender,seeking,mbti))
      else:
        print('error')
        bot.send_message(call.message.chat.id, 'Error.')
        return

    elif call.data == 'Stop':
      bot.answer_callback_query(call.id)
      bot.delete_message(call.message.chat.id, call.message.message_id -1)
      db.delete_queue(call.message.chat.id)
      # bot.send_message(call.message.chat.id, '❌ Search stopped.', reply_markup = main_menu())
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❌ Search stopped.', reply_markup = main_menu())

##bot.polling(none_stop = True)
