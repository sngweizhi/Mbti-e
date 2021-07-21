import messages
import telebot
import random
from telebot import types
from database2 import *
import os

import logging
import time

from decouple import config

from flask import Flask, request

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
telebot.logging.basicConfig(filename='filename.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(config('TOKEN'))

admins = config('ADMIN', cast=lambda v: [int(s.strip()) for s in v.split(',')])
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

def report_confirm():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='✏ Re-type reason',
                                          callback_data='retype_report')
  button2 = types.InlineKeyboardButton(text='» Submit ',
                                          callback_data='confirm_report')
  markup.add(button1,button2)
  return markup

def report_make():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='cancel_report')
  button2 = types.InlineKeyboardButton(text='⚠ Make a report ',
                                          callback_data='make_report')
  markup.add(button1,button2)
  return markup

def icebreaker_first():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='✏ Edit',
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
  button5 = types.InlineKeyboardButton(text='« Back to profile setup',
                                          callback_data='setupback')
  markup.add(button1,button2,button3,button4,button5)

  return markup

#def setup_settings():
#  markup = types.InlineKeyboardMarkup()
#  button1 = types.InlineKeyboardButton(text='« Back to profile setup',
#                                          callback_data='setupback')
#  button2 = types.InlineKeyboardButton(text='« Back to Bot',
#                                          callback_data='Bot')
#  markup.add(button1, button2)
#  return markup

def stop_search():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Stop searching',
                                          callback_data='Stop')
  markup.add(button1)

  return markup

@bot.message_handler(commands = ['start'])
def start(message):
    if set_user(message.chat.id) != False:
        bot.send_message(message.chat.id, messages.welcome, parse_mode = 'MarkdownV2')
        return

    elif setup_complete(message.chat.id) == False:
      bot.send_message(message.chat.id, '❗ Please setup your profile first! /setup')
      
    elif get_active_chat(message.chat.id) != None:
        print(get_active_chat(message.chat.id))
        bot.send_message(message.chat.id, '❗ You are still in a chat!')

    elif get_queue(message.chat.id) != None:
      bot.send_message(message.chat.id, '❗ You are already in the queue!')

    else:
      bot.send_message(message.chat.id, 'Click the button below to start matching!',reply_markup=main_menu())

@bot.message_handler(commands = ['stop'])
def stop(message):
    if get_queue(message.chat.id) != None:
      bot.delete_message(call.message.chat.id, call.message.message_id -1)
      delete_queue(call.message.chat.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Search stopped.', reply_markup = main_menu())
      return
    chat_info = get_active_chat(message.chat.id)
    if chat_info != None:
        delete_chat(chat_info[0])
        bot.send_message(chat_info[1], 'Your match has ended the chat. Input /start to start searching for another match!')
        bot.send_message(message.chat.id, 'You have ended the chat. Input /start to start searching for another match!')
    else:
        bot.send_message(message.chat.id, '❗ You have not started a chat!')


@bot.message_handler(commands=['setup'])
def echo(message):
    """
    Make the user setup their profile
    :param message:
    :return:
    """
    if get_active_chat(message.chat.id) != None:
       bot.send_message(message.chat.id, '❗ You are still in a chat!')
       return

    if set_gender(message.chat.id) == None: # Means no user id in database, direct them to /start
        bot.send_message(message.chat.id, 'Please enter /start first!', reply_markup=gender_menu())
        return

    if get_gender(message.chat.id) == None:
      bot.send_message(message.chat.id, 'Welcome to MBTInder! Please select your gender!', reply_markup=gender_menu())
      
    else:
      mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
      gender = get_gender(message.chat.id)
      gendermatch = get_gender_match(message.chat.id)
      seeking = get_seeking(message.chat.id)
      mbti = get_mbti(message.chat.id)
      iceb = get_icebreaker(message.chat.id)
      bot.send_message(message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

@bot.message_handler(commands=['icebreaker'])
def echo(message):
    if bool(get_active_chat(message.chat.id)):
      chat_info = get_active_chat(message.chat.id)
      if get_icebreaker(message.chat.id) == 'Set':
          statements = [get_truth1(message.chat.id),get_truth2(message.chat.id),get_lie(message.chat.id)]
          random.shuffle(statements)
          ans = statements.index(get_lie(message.chat.id))
          userPoll[chat_info[1]] = [ans,statements]
          bot.send_poll(chat_info[1], '2 Truths 1 Lie. Select the Lie!', options = statements, correct_option_id=ans, type = 'quiz', is_anonymous= False)
          bot.send_message(message.chat.id, '2 Truths 1 Lie sent!')
      else:
          bot.send_message(message.chat.id, '❗ You have not set an ice breaker!')
    else:
      bot.send_message(message.chat.id, '❗ You have not started a chat!')


@bot.message_handler(commands=['report'])
def echo(message):
    if get_active_chat(message.chat.id) != None:
        bot.send_message(message.chat.id, 'Do you wish to make a report\? You will be asked to enter your reason for reporting \(e\.g\. Harassment, impersonation, advertising services\)\. Misuse of the reporting system will *result in a ban*\.', reply_markup=report_make(),parse_mode='MarkdownV2')
    elif get_last_chat(message.chat.id) != None:
        bot.send_message(message.chat.id, 'Do you wish to make a report\? You will be asked to enter your reason for reporting \(e\.g\. Harassment, impersonation, advertising services\)\. Misuse of the reporting system will *result in a ban*\.', reply_markup=report_make(),parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, '❗ Chat history not found! Please contact the admin @zeigarnik for assistance.')

@bot.poll_answer_handler(func=lambda message: True)
def poll_answer(message):
  user_ans = message.option_ids[0]
  chat_info = get_active_chat(message.user.id)
  ans = userPoll[message.user.id][0]
  statement = userPoll[message.user.id][1]
  if user_ans == ans:
    bot.send_message(message.user.id, 'Hooray! You selected the right answer!')
    bot.send_message(chat_info[1], "User selected the right answer! '{}'".format(statement[user_ans]))
  else:
    bot.send_message(message.user.id, 'You selected the wrong answer!')
    bot.send_message(chat_info[1], "User selected the wrong answer! '{}'".format(statement[user_ans]))
  userPoll.pop(message.user.id, None) #reset

##### ADMIN COMMANDS #####

@bot.message_handler(commands=['deletedb'])
def echo(message):
    """
    delete database
    """
    if message.chat.id in admins:
        clear_database()
        bot.send_message(message.chat.id,'Deleting database...')
    else:
        return

@bot.message_handler(commands=['broadcast'])
def echo(message):
    """
    broadcast message to all users
    """
    if message.chat.id in admins:
        bot.send_message(message.chat.id,'Send message to broadcast:')
        userStep[message.chat.id] = 99
    else:
        return

@bot.message_handler(commands=['stats'])
def echo(message):
    """
    Generate stats of users
    """
    if message.chat.id in admins:
        user = admin_user_count()
        active = admin_active_chat()
        queue = admin_queue()
        banned_users = banned_user_count()
        msg = '*MBTInder Bot stats*\n\nTotal Users: *{}*\nActive chats: *{}*\nIn queue: *{}*\nBanned: *{}*'.format(user,active,queue,banned_users)
        bot.send_message(message.chat.id, msg,parse_mode='MarkdownV2')
    else:
        return

@bot.message_handler(commands=['ban'])
def echo(message):
    """
    Ban a user
    """
    if message.chat.id in admins:
        bot.send_message(message.chat.id,'Send chat_id to ban:')
        userStep[message.chat.id] = 98
    else:
        return

@bot.message_handler(commands=['unban'])
def echo(message):
    """
    Unban a user
    """
    if message.chat.id in admins:
        bot.send_message(message.chat.id,'Send chat_id to unban:')
        userStep[message.chat.id] = 985
    else:
        return

def get_user_step(uid):
    if uid in userStep:
      return userStep[uid]
    else:
      return 0

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) > 0)
def messagestop(message):
  step = get_user_step(message.chat.id)
  if step < 4:
    if step == 1: #1,2,3 is for setup settings
      if set_truth1(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 1 set!')
    elif step == 2:
      if set_truth2(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 2 set!')
    elif step == 3:
      if set_lie(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Lie set!')
    mess = "Edit your 2 Truth 1 Lie.\n \nTruth 1: {}\nTruth 2: {}\nLie: {}"
    truth1 = get_truth1(message.chat.id)
    truth2 = get_truth2(message.chat.id)
    lie = get_lie(message.chat.id)
    bot.send_message(message.chat.id, mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu())
    userStep.pop(message.chat.id,None)

  elif step == 4: #4,5,6 is for first time setup process
    if set_truth1(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 1 set!')
    bot.send_message(message.chat.id, 'Now send me your *Truth 2* statement\.', parse_mode ='MarkdownV2')
    userStep[message.chat.id] = 5

  elif step == 5:
    if set_truth2(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 2 set!')
    bot.send_message(message.chat.id, 'Now send me your *Lie* statement\.', parse_mode ='MarkdownV2')
    userStep[message.chat.id] = 6

  elif step == 6:
    if set_lie(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Lie set!')
    mess = "Your 2 Truth 1 Lie is set!\n \nTruth 1: {}\nTruth 2: {}\nLie: {}"
    truth1 = get_truth1(message.chat.id)
    truth2 = get_truth2(message.chat.id)
    lie = get_lie(message.chat.id)
    bot.send_message(message.chat.id, mess.format(truth1, truth2, lie),reply_markup=icebreaker_first())
    userStep.pop(message.chat.id,None)
    
  elif step == 99: #Admin broadcast
      alluser = get_all_users()
      for user in alluser:
          bot.send_message(user, '\📢*Admin: ' + message.text+'*', parse_mode = 'MarkdownV2')
      userStep.pop(message.chat.id,None)

  elif step == 98: #Ban user
      set_banned(int(message.text))
      bot.send_message(message.chat.id,'Banned user {}'.format(message.text))
      userStep.pop(message.chat.id,None)

  elif step == 985:
      del_banned(int(message.text))
      bot.send_message(message.chat.id,'Unbanned user {}'.format(message.text))
      userStep.pop(message.chat.id,None)

  elif step == 91: #Reporting
    user_reporting = [message.chat.id, message.chat.username]
    if bool(get_active_chat(message.chat.id)):
        user_reported = get_active_chat(message.chat.id)[1]
    elif bool(get_last_chat(message.chat.id)):
        user_reported = get_last_chat(message.chat.id)[1]
    else:
        user_reported = 'Unidentified'
    mess = 'Report\n\nReason: {}'
    bot.send_message(message.chat.id, mess.format(message.text))
    bot.send_message(message.chat.id, "⚠ Please verify if the above information is accurate before submitting your report.", reply_markup = report_confirm())
        
    for admin in admins:
        mess = 'Report:\n\nUser reporting: {}\nUser reported: {}\nReason: {}'
        bot.send_message(admin, mess.format(user_reporting, user_reported, message.text))
    
  else:
    userStep[message.chat.id]=0

  


@bot.message_handler(content_types=['text', 'sticker', 'video', 'photo', 'audio', 'voice','video_note'])
def echo(message):

    if message.content_type == 'sticker':
        if get_active_chat(message.chat.id) != None:
          chat_info = get_active_chat(message.chat.id)          
          bot.send_sticker(chat_info[1], message.sticker.file_id)

        else:
          return

    elif message.content_type == 'photo':
      if get_active_chat(message.chat.id) != None:
          chat_info = get_active_chat(message.chat.id)     
          
          file_id = None

          for item in message.photo:
            file_id = item.file_id

          bot.send_photo(chat_info[1],
                       file_id,
                       caption=message.caption)

      else:
          return

    elif message.content_type == 'audio':
        if get_active_chat(message.chat.id) != None:
          chat_info = get_active_chat(message.chat.id)          
          bot.send_audio(chat_info[1],
                       message.audio.file_id,
                       caption=message.caption)

        else:
          return

        
    elif message.content_type == 'video':
        if get_active_chat(message.chat.id) != None:
          chat_info = get_active_chat(message.chat.id)  
          bot.send_video(chat_info[1],
                        message.video.file_id,
                        caption=message.caption)
        else:
          return

    elif message.content_type == 'voice':
        if get_active_chat(message.chat.id) != None:
          chat_info = get_active_chat(message.chat.id)  
          bot.send_voice(chat_info[1],
                        message.voice.file_id)

        else:
          return

    elif message.content_type == 'video_note':
      if get_active_chat(message.chat.id) != None:
          chat_info = get_active_chat(message.chat.id)  
          bot.send_video_note(chat_info[1],
                        message.video_note.file_id)
                        
    elif message.content_type == 'text':
        

        if message.text != '/start' and message.text != '/stop' and \
                    message.text != '/setup' and message.text != '/icebreaker' and message.text != '/help'\
                    and message.text != '/ban' and message.text != '/unban' and message.text != '/broadcast' \
                    and message.text != '/report':

            if get_active_chat(message.chat.id) != None:
              chat_info = get_active_chat(message.chat.id)
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
                  bot.send_message(message.chat.id, '❗ You cannot forward your own message!')
            else:
              bot.send_message(message.chat.id, '❗ You are not currently in a chat with anyone!')

@bot.callback_query_handler(func=lambda call: True)
def echo(call):

    if call.data == 'Male':
      bot.answer_callback_query(call.id)
      if bool(get_gender(call.message.chat.id)):
        if set_gender(call.message.chat.id, 'Male'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your gender to *Male*\.',  parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch = get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti = get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender(call.message.chat.id, 'Male'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Male* as your gender\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Who would you like to match with?', reply_markup = match_gender_menu())
        else:
          return
        
    elif call.data == 'Female':
      bot.answer_callback_query(call.id)
      if bool(get_gender(call.message.chat.id)):
        if set_gender(call.message.chat.id, 'Female'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your gender to *Female*\.', parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch = get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti = get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender(call.message.chat.id, 'Female'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Female* as your gender\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Who would you like to match with?', reply_markup =match_gender_menu())
        else:
          return

    elif call.data == 'Malematch': 
      bot.answer_callback_query(call.id)
      if bool(get_gender_match(call.message.chat.id)):
        if set_gender_match(call.message.chat.id, 'Male'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Males*\.',  parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch = get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti = get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender_match(call.message.chat.id, 'Male'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Males*\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
        else:
          return

    elif call.data == 'Femalematch': 
      bot.answer_callback_query(call.id)
      if bool(get_gender_match(call.message.chat.id)):
        if set_gender_match(call.message.chat.id, 'Female'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Females*\.',  parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch = get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti =get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender_match(call.message.chat.id, 'Female'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Females*\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
        else:
          return

    elif call.data == 'Anymatch': 
      bot.answer_callback_query(call.id)
      if bool(get_gender_match(call.message.chat.id)):
        if set_gender_match(call.message.chat.id, 'Any'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Everyone*\.',  parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch =get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti = get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender_match(call.message.chat.id, 'Any'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Everyone*\.',  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'What are you seeking?', reply_markup = seeking_menu())
        else:
          return

    elif call.data == 'Dating': 
      bot.answer_callback_query(call.id)
      if bool(get_seeking(call.message.chat.id)):
        if set_seeking(call.message.chat.id, 'Dating'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your purpose to *Dating*\.',  parse_mode = 'MarkdownV2')
          mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
          gender = get_gender(call.message.chat.id)
          gendermatch = get_gender_match(call.message.chat.id)
          seeking = get_seeking(call.message.chat.id)
          mbti = get_mbti(call.message.chat.id)
          iceb = get_icebreaker(call.message.chat.id)
          bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')         
      else:
        if set_seeking(call.message.chat.id, 'Dating'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Dating* as your purpose\.',  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Select your MBTI type!', reply_markup = mbti_menu())
        else:
          return

    elif call.data == 'Friendship': 
      bot.answer_callback_query(call.id)
      if bool(get_seeking(call.message.chat.id)):
        if set_seeking(call.message.chat.id, 'Friendship'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your purpose to *Friendship*\.',  parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch = get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti = get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_seeking(call.message.chat.id, 'Friendship'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Friendship* as your purpose\.', parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'Select your MBTI type!', reply_markup = mbti_menu())
        else:
          return

    elif call.data == 'Purpose': 
      bot.answer_callback_query(call.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'What are you seeking?', reply_markup = seeking_menu())
    
    elif call.data == 'Gender': 
      bot.answer_callback_query(call.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Select your gender.', reply_markup = gender_menu())

    elif call.data == 'Match Gender': 
      bot.answer_callback_query(call.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Who would you like to match with?', reply_markup = match_gender_menu())

    elif call.data == 'MBTI': 
      bot.answer_callback_query(call.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Select your MBTI type!', reply_markup = mbti_menu())

    elif call.data == 'icebreaker':
      bot.answer_callback_query(call.id)
      mess = "Edit your 2 Truth 1 Lie.\n \nTruth 1: {}\nTruth 2: {}\nLie: {}"
      truth1 = get_truth1(call.message.chat.id)
      truth2 = get_truth2(call.message.chat.id)
      lie = get_lie(call.message.chat.id)
      if bool(get_truth1(call.message.chat.id)):
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu())
      else:
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Setup your 2 Truths and 1 Lie!', reply_markup=icebreaker_setup_menu())

    elif call.data in ['truth1','truth2','lie']:
        bot.answer_callback_query(call.id)
        if call.data == 'truth1':
          statement = 'Truth 1'
          userStep[call.message.chat.id] = 1
        if call.data == 'truth2':
          statement = 'Truth 2'
          userStep[call.message.chat.id] = 2
        if call.data == 'lie':
          statement = 'Lie'
          userStep[call.message.chat.id] = 3
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *{}* statement\.'.format(statement), parse_mode ='MarkdownV2')

    elif call.data == 'icebreaker_setup':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *Truth 1* statement\.', parse_mode ='MarkdownV2')
        userStep[call.message.chat.id] = 4

    elif call.data == 'complete':
      bot.answer_callback_query(call.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Your profile is complete! Press the button below to start matching!',reply_markup=main_menu())

    elif call.data == 'Bot':
      bot.answer_callback_query(call.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Click the button below to start matching!',reply_markup=main_menu())

    elif call.data == 'setupback': 
      bot.answer_callback_query(call.id)
      mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
      gender = get_gender(call.message.chat.id)
      gendermatch = get_gender_match(call.message.chat.id)
      seeking = get_seeking(call.message.chat.id)
      mbti = get_mbti(call.message.chat.id)
      iceb = get_icebreaker(call.message.chat.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

    elif call.data in ['ISFP', 'ISFJ', 'ISTP', 'ISTJ','ESFP', 'ESFJ', 'ESTP', 'ESTJ', 'INFP', 'INFJ', 'INTP', 'INTJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ']: 
      bot.answer_callback_query(call.id)
      if bool(get_mbti(call.message.chat.id)):
        if set_mbti(call.message.chat.id, call.data):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your MBTI type to *{}*\.'.format(call.data),  parse_mode = 'MarkdownV2')
            mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Purpose*: {}\n*MBTI*: {}\n*Ice breaker*: {}"
            gender = get_gender(call.message.chat.id)
            gendermatch = get_gender_match(call.message.chat.id)
            seeking = get_seeking(call.message.chat.id)
            mbti = get_mbti(call.message.chat.id)
            iceb = get_icebreaker(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess.format(gender, gendermatch, seeking, mbti, iceb), reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_mbti(call.message.chat.id, call.data):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *{}* as your MBTI type\.'.format(call.data),  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id, 'You may choose to set an ice breaker!', reply_markup = icebreaker_menu())
        else:
          return

    elif call.data == 'cancel_report':
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == 'make_report':
        bot.answer_callback_query(call.id)
        userStep[call.message.chat.id] = 91
        bot.send_message(call.message.chat.id, 'Please enter your reason for reporting.')

    elif call.data == 'retype_report':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Re-type your reason for reporting.')

    elif call.data == 'confirm_report':
        bot.answer_callback_query(call.id)
        userStep.pop(call.message.chat.id,None)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Report succesfully submitted! An admin will contact you should further information be required.')
        for admin in admins:
            user_reporting = call.message.chat.id
            bot.send_message(admin, 'Latest report from {} confirmed'.format(user_reporting))

    elif call.data == 'NewChat':

      if get_queue(call.message.chat.id) != None:
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❗ You are already in the queue!')
      
      elif setup_complete(call.message.chat.id) == False:
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❗ Your profile is incomplete!')

      elif call.message.chat.id in get_banned():
          bot.answer_callback_query(call.id)
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❗ You have been banned!')

      elif get_active_chat(call.message.chat.id) == None:
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        gendermatch = get_gender_match(call.message.chat.id)
        gender = get_gender(call.message.chat.id)
        seeking = get_seeking(call.message.chat.id)
        mbti = get_mbti(call.message.chat.id)
        user_info = get_gender_chat(gender, gendermatch, seeking)
        chat_two = user_info[0]
        gender2 = user_info[1]
        seeking2 = user_info[3]
        mbti2 = user_info[4]
        msg = get_message_id(chat_two)
        if create_chat(call.message.chat.id, chat_two) == False:
                  bot.send_sticker(call.message.chat.id, messages.search_sticker)
                  sent = bot.send_message(call.message.chat.id, 'Searching for a suitable match...', reply_markup = stop_search())
                  add_queue(call.message.chat.id, gender, gendermatch, seeking, mbti, sent.message_id)
        else:
                  mess = 'Gender: {}\nPurpose: {}\nMBTI: {}\n\nInput /stop to end the chat.'
                  bot.delete_message(chat_two, msg)
                  bot.delete_message(chat_two, int(msg)-1)
                  bot.send_sticker(call.message.chat.id, messages.match_sticker)
                  bot.send_message(call.message.chat.id, mess.format(gender2,seeking2,mbti2))
                  bot.send_sticker(chat_two, messages.match_sticker)
                  bot.send_message(chat_two, mess.format(gender,seeking,mbti))
      else:
        print('error')
        bot.send_message(call.message.chat.id, '❗ Error.')
        return

    elif call.data == 'Stop':
      bot.answer_callback_query(call.id)
      bot.delete_message(call.message.chat.id, call.message.message_id -1)
      delete_queue(call.message.chat.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Search stopped.', reply_markup = main_menu())

#bot.polling(none_stop = True)

@server.route('/' + config('TOKEN'), methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://mbtinder.herokuapp.com/' + config('TOKEN')) #changeback when not in testing
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
