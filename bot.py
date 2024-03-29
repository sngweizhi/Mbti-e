import messages
import telebot
import random
from telebot import types
from database import *
import os
import re
import requests
import logging
from time import sleep

from decouple import config

from flask import Flask, request

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
telebot.logging.basicConfig(filename='filename.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(config('TOKEN'))

admins = config('ADMIN', cast=lambda v: [int(s.strip()) for s in v.split(',')])
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
  button1 = types.InlineKeyboardButton(text='Skip »',
                                          callback_data='mbti_skip')
  i = 0
  for mbti in mbti_list:
      row_list.append(types.InlineKeyboardButton(text=mbti, callback_data = mbti))
      i += 1
      if i%4 == 0:
        button_list.append(row_list)
        row_list = []
  markup = types.InlineKeyboardMarkup(button_list)
  markup.add(button1)
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
  button3 = types.InlineKeyboardButton(text='Edit Age',
                                          callback_data='Age')
  button4 = types.InlineKeyboardButton(text='Edit Age Filter',
                                          callback_data='Age filter')
  button5 = types.InlineKeyboardButton(text='Edit Purpose',
                                          callback_data='Purpose')
  button6 = types.InlineKeyboardButton(text='Edit MBTI',
                                          callback_data='MBTI')
  button7 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='Bot')
  markup = types.InlineKeyboardMarkup([[button1,button2],[button3,button4],[button5,button6],[button7]])                                   
  return markup

#def icebreaker_menu():
#  markup = types.InlineKeyboardMarkup()
#  button1 = types.InlineKeyboardButton(text='2Truth1Lie',
#                                          callback_data='icebreaker_setup')
#  button2 = types.InlineKeyboardButton(text='Skip »',
#                                          callback_data='complete')
#  markup.add(button1,button2)

#  return markup

def report_confirm():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='✏ Re-type reason',
                                          callback_data='retype_report')
  button2 = types.InlineKeyboardButton(text='Submit »',
                                          callback_data='confirm_report')
  markup.add(button1,button2)
  return markup

def report_make():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='cancel_report')
  button2 = types.InlineKeyboardButton(text='⚠ Report user',
                                          callback_data='make_report')
  markup.add(button1,button2)
  return markup

#def icebreaker_first():
#  markup = types.InlineKeyboardMarkup()
#  button1 = types.InlineKeyboardButton(text='✏ Edit',
#                                          callback_data='icebreaker')
#  button2 = types.InlineKeyboardButton(text='Complete »',
#                                          callback_data='complete')
#  markup.add(button1,button2)

#  return markup

def icebreaker_setup_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Truth 1',
                                          callback_data='truth1')
  button2 = types.InlineKeyboardButton(text='Truth 2',
                                          callback_data='truth2')
  button3 = types.InlineKeyboardButton(text='Lie',
                                          callback_data='lie')
  button4 = types.InlineKeyboardButton(text='Confirm and Submit »',
                                          callback_data='ttol_quiz')
  
  markup.add(button1,button2,button3,button4)

  return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('/ttol')
    item2 = types.KeyboardButton('/tiktok')
    item3 = types.KeyboardButton('/topic')
    item4 = types.KeyboardButton('/stop')
    item5 = types.KeyboardButton('/report')
    markup.add(item1, item2, item3, item4)
    return markup

def feedback_make():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='« Back to Bot',
                                              callback_data='cancel_report') #Reuse cancel report to remove message.
    button2 = types.InlineKeyboardButton(text='⭐ Give feedback!',
                                              callback_data='make_feedback')
    markup.add(button1,button2)
    return markup

def stop_chat():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='« Back to Chat',
                                          callback_data='cancel_report')
  button2 = types.InlineKeyboardButton(text='⚠ End Chat',
                                          callback_data='endchat')
  markup.add(button1,button2)

  return markup

def help_menu():
  button1 = types.InlineKeyboardButton(text='⭐ Give feedback!',
                                              callback_data='make_feedback')
  button2 = types.InlineKeyboardButton(text='⚠ Report user',
                                          callback_data='make_report')
  button3 = types.InlineKeyboardButton(text='About Mbtie Bot',
                                          callback_data='about')
  button4 = types.InlineKeyboardButton(text='« Back to Bot',
                                          callback_data='cancel_report')
  markup = types.InlineKeyboardMarkup([[button1,button2],[button3],[button4]])
  return markup

def about_menu():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='« Back to Help',
                                          callback_data='backtohelp')
    markup.add(button1)
    return markup

def ttol_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text="Let's play! ☺",
                                          callback_data='ttol_accept')
  button2 = types.InlineKeyboardButton(text='Decline',
                                          callback_data='ttol_decline')
  markup.add(button1,button2)
  return markup

def ttol_tutorial(number):
    markup = types.InlineKeyboardMarkup()
    if number == 1:
        button1 = types.InlineKeyboardButton(text="Start", callback_data = 'ttol_start')
        button2 = types.InlineKeyboardButton(text="How to play »", callback_data = 'ttol_step1')
        markup.add(button1, button2)
    elif number == 2:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'ttol_step0')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'ttol_step2')
        markup.add(button1, button2)
    elif number == 3:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'ttol_step1')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'ttol_step3')
        markup.add(button1, button2)
    elif number == 4:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'ttol_step2')
        button2 = types.InlineKeyboardButton(text="« Back to start", callback_data = 'ttol_step0')
        markup.add(button1, button2)

    elif number == 11:
        button1 = types.InlineKeyboardButton(text="How to play »", callback_data = 'ttol_step11')
        markup.add(button1)
  
    elif number == 12:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'ttol_step10')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'ttol_step12')
        markup.add(button1, button2)
    elif number == 13:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'ttol_step11')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'ttol_step13')
        markup.add(button1, button2)
    elif number == 14:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'ttol_step12')
        button2 = types.InlineKeyboardButton(text="« Back to start", callback_data = 'ttol_step10')
        markup.add(button1, button2)

    return markup

def tiktok_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Bring it on! 😈',
                                          callback_data='tiktok_accept')
  button2 = types.InlineKeyboardButton(text='Decline',
                                          callback_data='tiktok_decline')
  markup.add(button1,button2)
  return markup

def tiktok_encore_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Another round!',
                                          callback_data='tiktok_encore')
  button2 = types.InlineKeyboardButton(text='No thanks!',
                                          callback_data='tiktok_decline_encore')
  markup.add(button1,button2)
  return markup

def stop_search():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Stop searching',
                                          callback_data='Stop')
  markup.add(button1)

  return markup

def tiktok_rating(chat_id):
    button1 = types.InlineKeyboardButton(text='1',
                                          callback_data='ttbattle-{}-1'.format(chat_id))
    button2 = types.InlineKeyboardButton(text='2',
                                          callback_data='ttbattle-{}-2'.format(chat_id))
    button3 = types.InlineKeyboardButton(text='3',
                                          callback_data='ttbattle-{}-3'.format(chat_id))
    button4 = types.InlineKeyboardButton(text='4',
                                          callback_data='ttbattle-{}-4'.format(chat_id))
    button5 = types.InlineKeyboardButton(text='5',
                                          callback_data='ttbattle-{}-5'.format(chat_id))
    button6 = types.InlineKeyboardButton(text='6',
                                          callback_data='ttbattle-{}-6'.format(chat_id))
    button7 = types.InlineKeyboardButton(text='7',
                                          callback_data='ttbattle-{}-7'.format(chat_id))
    button8 = types.InlineKeyboardButton(text='8',
                                          callback_data='ttbattle-{}-8'.format(chat_id))
    button9 = types.InlineKeyboardButton(text='9',
                                          callback_data='ttbattle-{}-9'.format(chat_id))
    button10 = types.InlineKeyboardButton(text='10',
                                          callback_data='ttbattle-{}-91'.format(chat_id))
    button11 = types.InlineKeyboardButton(text='😂💯❤️',
                                          callback_data='ttbattle-{}-92'.format(chat_id))
    markup = types.InlineKeyboardMarkup([[button1,button2,button3,button4,button5],[button6,button7,button8,button9,button10],[button11]])
    return markup

def tiktok_url_menu(url):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Watch User's TikTok!",
                                          url=url)
    markup.add(button1)
    return markup

def tiktok_tutorial(number):
    markup = types.InlineKeyboardMarkup()
    if number == 1:
        button1 = types.InlineKeyboardButton(text="How to play »", callback_data = 'tiktok_step1')
        markup.add(button1)
    elif number == 2:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'tiktok_step0')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'tiktok_step2')
        markup.add(button1, button2)
    elif number == 3:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'tiktok_step1')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'tiktok_step3')
        markup.add(button1, button2)
    elif number == 4:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'tiktok_step2')
        button2 = types.InlineKeyboardButton(text="« Back to start", callback_data = 'tiktok_step0')
        markup.add(button1, button2)
  
    return markup

def topics_menu():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text="Let's go! ☺",
                                          callback_data='topics_accept')
  button2 = types.InlineKeyboardButton(text='Decline',
                                          callback_data='topics_decline')
  markup.add(button1,button2)
  return markup

def topics_tutorial(number):
    markup = types.InlineKeyboardMarkup()
    if number == 1:
        button1 = types.InlineKeyboardButton(text="Generate Topic", callback_data = 'topics_start')
        button2 = types.InlineKeyboardButton(text="How to play »", callback_data = 'topics_step1')
        markup.add(button1, button2)
    elif number == 2:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'topics_step0')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'topics_step2')
        markup.add(button1, button2)
    elif number == 3:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'topics_step1')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'topics_step3')
        markup.add(button1, button2)
    elif number == 4:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'topics_step2')
        button2 = types.InlineKeyboardButton(text="« Back to start", callback_data = 'topics_step0')
        markup.add(button1, button2)

    elif number == 11:
        button1 = types.InlineKeyboardButton(text="How to play »", callback_data = 'topics_step11')
        markup.add(button1)
  
    elif number == 12:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'topics_step10')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'topics_step12')
        markup.add(button1, button2)
    elif number == 13:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'topics_step11')
        button2 = types.InlineKeyboardButton(text="Next step »", callback_data = 'topics_step13')
        markup.add(button1, button2)
    elif number == 14:
        button1 = types.InlineKeyboardButton(text="« Back", callback_data = 'topics_step12')
        button2 = types.InlineKeyboardButton(text="« Back to start", callback_data = 'topics_step10')
        markup.add(button1, button2)

    return markup

def topics_reroll():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text="Generate another topic!",
                                          callback_data='topics_start')
  markup.add(button1)
  return markup

######## BASIC COMMANDS #########

@bot.message_handler(commands = ['start'])
def start(message):
    if set_user(message.chat.id) != False:
        bot.send_message(message.chat.id, messages.welcome, parse_mode = 'MarkdownV2')
        return

    elif setup_complete(message.chat.id) == False:
      bot.send_message(message.chat.id, '❗ Please setup your profile first! /setup')
      
    elif get_active_chat(message.chat.id) != None:
        bot.send_message(message.chat.id, '❗ You are still in a chat!')

    elif get_queue(message.chat.id) != None:
      bot.send_message(message.chat.id, '❗ You are already in the queue!')

    else:
      bot.send_message(message.chat.id, 'Click the button below to start matching!',reply_markup=main_menu())

@bot.message_handler(commands = ['stop']) # add confirmatioun
def stop(message):
    if get_queue(message.chat.id) != None:
      bot.delete_message(call.message.chat.id, call.message.message_id -1)
      delete_queue(call.message.chat.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Search stopped.', reply_markup = main_menu())
      return

    if get_active_chat(message.chat.id) != None:
        chat_info = get_active_chat(message.chat.id)
        if chat_info[1] in admins:
            bot.send_message(message.chat.id, "*You cannot end a chat with an admin\. The admin will end it\.*", parse_mode='MarkdownV2')
            return
        else:
            bot.send_message(message.chat.id, "*You will lose contact with your match after you end the chat*\.\n\nAre you sure you want to end the chat?",reply_markup=stop_chat(), parse_mode='MarkdownV2')
            return
    else:
        bot.send_message(message.chat.id, '❗ You have not yet started a chat!')


@bot.message_handler(commands=['setup'])
def echo(message):
    """
    Make the user setup their profile
    :param message:
    :return:
    """
    if get_active_chat(message.chat.id) != None:
       bot.send_message(message.chat.id, "⚠ You are entering setup while in a chat! Simply press 'Back to Bot' to resume your chat!")
       mess = mbtinder_settings(message.chat.id)
       bot.send_message(message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
       return

    if get_user(message.chat.id) == None: # Just using random function to check existence of user id in database
        bot.send_message(message.chat.id, 'Please enter /start first!')
        return

    if get_gender(message.chat.id) == None:
      bot.send_message(message.chat.id, 'Welcome to MBTInder! Please select your gender!', reply_markup=gender_menu())
      
    else:
      mess = mbtinder_settings(message.chat.id)
      bot.send_message(message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

@bot.message_handler(commands=['ttol'])
def echo(message):
    if bool(get_active_chat(message.chat.id)):
        chat_info = get_active_chat(message.chat.id)

        if get_game_message(message.chat.id) != None and get_game_message(message.chat.id) != 'topics':
       
            if get_game_message(message.chat.id).isdigit():
                bot.send_message(message.chat.id, '❗ You have already sent a request for a game!')
                return

            else:
                bot.send_message(message.chat.id, '❗ You are already in a game!')

        elif get_game_message(chat_info[1]) != None and get_game_message(message.chat.id) != 'topics':

                if get_game_message(chat_info[1]).isdigit():
                    bot.send_message(message.chat.id, '❗ Other user has already sent you a request for a game!.')
                    return

                else:
                    bot.send_message(message.chat.id, '❗ You are already in a game!')
        else:
            bot.send_message(chat_info[1], 'User has sent you a request for a game of *2Truths1Lie™*\.', reply_markup=ttol_menu(), parse_mode='MarkdownV2')
            sent = bot.send_message(message.chat.id, 'You have sent a request for a *2Truths1Lie™*\. You will be notified when user accepts or declines your request\.', parse_mode='MarkdownV2')
            set_game_message(message.chat.id,sent.message_id)

    else:
        bot.send_message(message.chat.id, '❗ You have not started a chat!')

#@bot.message_handler(commands=['icebreakers'])
#def echo(message):
#    if bool(get_active_chat(message.chat.id)):
#      chat_info = get_active_chat(message.chat.id)
#      if get_icebreaker(message.chat.id) == 'Set':
#          statements = [get_truth1(message.chat.id),get_truth2(message.chat.id),get_lie(message.chat.id)]
#          random.shuffle(statements)
#          ans = statements.index(get_lie(message.chat.id))
#          userPoll[chat_info[1]] = [ans,statements]
#          bot.send_poll(chat_info[1], '2 Truths 1 Lie. Select the Lie!', options = statements, correct_option_id=ans, type = 'quiz', is_anonymous= False)
#          bot.send_message(message.chat.id, '2 Truths 1 Lie sent! You will be notified when user picks an answer.')
#      else:
#          bot.send_message(message.chat.id, '❗ Your 2 Truths 1 Lie is incomplete!')
#    else:
#      bot.send_message(message.chat.id, '❗ You have not started a chat!')

def mbti_cognitive_match(mbti1,mbti2): # Check for match in cognitive functions btw 2 MBTI types
    if mbti1 == 'Not set':
        mbti1 = 'ABCD' 
    else: 
        mbti1 = messages.mbti_cf[mbti1]
    if mbti2 == 'Not set':
        mbti2 = 'WXYZ' 
    else: 
        mbti2 = messages.mbti_cf[mbti2]
    match = []
    for c in mbti1:
        if c in mbti2:
            match.append(c)
    return match

@bot.message_handler(commands=['topic'])
def echo(message):
    if bool(get_active_chat(message.chat.id)):
        chat_info = get_active_chat(message.chat.id)
        
        if get_game_message(message.chat.id) != None:

            if get_game_message(message.chat.id) == 'topics':
                 chat_info = get_active_chat(message.chat.id)
                 bot.send_message(message.chat.id, 'You have rolled the dice for a random topic.')
                 bot.send_message(chat_info[1], 'User has rolled the dice for a random topic.')
                 mbti1 = get_mbti(message.chat.id)
                 mbti2 = get_mbti(chat_info[1])
                 match = mbti_cognitive_match(mbti1,mbti2)
                 if len(match) == 0:
                     if mbti1 == 'Not set':
                         match = ['Ni','Ne','Si','Se','Ti','Te','Fi','Fe']
                     else:
                         match = messages.mbti_cf[mbti1]
                 cognitive_func = random.choice(match)
                 msg = bot.send_dice(message.chat.id)
                 topic = messages.topics[cognitive_func][msg.dice.value]
                 sleep(3)
                 bot.send_message(message.chat.id, '__Cognitive function: {}__\nTopic: *{}*'.format(messages.cf[cognitive_func],topic), parse_mode='MarkdownV2', reply_markup = topics_reroll())
                 bot.send_message(chat_info[1], '__Cognitive function: {}__\nTopic: *{}*'.format(messages.cf[cognitive_func],topic), parse_mode='MarkdownV2')
                 return

            else:
                bot.send_message(message.chat.id, '❗ You have already sent a request for a game.')
                return
        
        if get_game_message(chat_info[1]) != None:
            bot.send_message(message.chat.id, '❗ Other user has already sent you a request for a game.')
            return

        bot.send_message(chat_info[1], 'User has sent you a request for *MBTI Topics™*\.', reply_markup=topics_menu(), parse_mode='MarkdownV2')
        sent = bot.send_message(message.chat.id, 'You have sent a request for a *MBTI Topics™*\. You will be notified when user accepts or declines your request\.', parse_mode='MarkdownV2')
        set_game_message(message.chat.id,sent.message_id)

    else:
        bot.send_message(message.chat.id, '❗ You have not started a chat!')


   #if bool(get_active_chat(message.chat.id)):
   #  chat_info = get_active_chat(message.chat.id)
   #  bot.send_message(message.chat.id, 'You have rolled the dice for a random topic.')
   #  bot.send_message(chat_info[1], 'User has rolled the dice for a random topic.')
   #  mbti1 = get_mbti(message.chat.id)
   #  mbti1 = get_mbti(message.chat.id)
   #  mbti2 = get_mbti(chat_info[1])
   #  match = mbti_cognitive_match(mbti1,mbti2)
   #  if len(match) == 0:
   #      if mbti1 == 'Not set':
   #          match = ['Ni','Ne','Si','Se','Ti','Te','Fi','Fe']
   #      else:
   #          match = messages.mbti_cf[mbti1]
   #  cognitive_func = random.choice(match)
   #  msg = bot.send_dice(message.chat.id)
   #  topic = messages.topics[cognitive_func][msg.dice.value]
   #  sleep(3)
   #  bot.send_message(message.chat.id, 'Cognitive function: *{}*\nRandom topic: *{}*'.format(messages.cf[cognitive_func],topic), parse_mode='MarkdownV2')
   #  bot.send_message(chat_info[1], 'Cognitive function: *{}*\nRandom topic: *{}*'.format(messages.cf[cognitive_func],topic), parse_mode='MarkdownV2')
   #else:
   #  bot.send_message(message.chat.id, '❗ You have not started a chat!')

@bot.message_handler(commands=['tiktok'])
def echo(message):
    if bool(get_active_chat(message.chat.id)):
        chat_info = get_active_chat(message.chat.id)
        
        if get_game_message(message.chat.id) != None and get_game_message(message.chat.id) != 'topics' and get_game_message(message.chat.id) != 'cancel':
            bot.send_message(message.chat.id, '❗ You have already sent a request for a game.')
            return
        
        if get_game_message(chat_info[1]) != None and get_game_message(chat_info[1]) != 'topics' and get_game_message(chat_info[1]) != 'cancel':
            bot.send_message(message.chat.id, '❗ Other user has already sent you a request for a game.')
            return
        
        if get_tiktok_url(chat_info[1]) != None:
            bot.send_message(message.chat.id, '❗ You are already in a TikTokBattle™!')
            return
        
        if get_tiktok_url(message.chat.id) != None:
            bot.send_message(message.chat.id, '❗ You are already in a TikTokBattle™!')
            return
        
        bot.send_message(chat_info[1], 'User has sent you a request for a *TikTokBattle™*\.', reply_markup=tiktok_menu(), parse_mode='MarkdownV2')
        sent = bot.send_message(message.chat.id, 'You have sent a request for a *TikTokBattle™*\. You will be notified when user accepts or declines your request\.', parse_mode='MarkdownV2')
        set_game_message(message.chat.id,sent.message_id)
    else:
        bot.send_message(message.chat.id, '❗ You have not started a chat!')


@bot.message_handler(commands=['report'])
def echo(message):
    if get_active_chat(message.chat.id) != None:
        bot.send_message(message.chat.id, 'Do you wish to make a report\? You will be asked to enter your reason for reporting \(e\.g\. harassment, impersonation, advertising services\)\.\n\n*Misuse of the reporting system will result in a ban*\.', reply_markup=report_make(),parse_mode='MarkdownV2')
    elif get_last_chat(message.chat.id) != None:
        bot.send_message(message.chat.id, 'Do you wish to make a report\? You will be asked to enter your reason for reporting \(e\.g\. harassment, impersonation, advertising services\)\.\n\n*Misuse of the reporting system will result in a ban*\.', reply_markup=report_make(),parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, '❗ Chat history not found! Please contact the admin @designsynergy for assistance.')


@bot.message_handler(commands=['feedback'])
def echo(message):
    if get_active_chat(message.chat.id) != None:
        bot.send_message(message.chat.id, '❗ You are still in a chat!')
    else:
        bot.send_message(message.chat.id, 'Hey there! Hope you are enjoying the bot so far! If you have any feedback for us to improve to bot (e.g. bug, typo, new feature suggestions) you are welcome to write your feedback here!', reply_markup= feedback_make())
        

@bot.message_handler(commands=['help'])
def echo(message):
    bot.send_message(message.chat.id, messages.help, reply_markup=help_menu() ,parse_mode = 'MarkdownV2')


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
        msg = bot.send_message(message.chat.id,'Send message to broadcast:')
        bot.register_next_step_handler(msg, broadcast_step)
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
        msg = bot.send_message(message.chat.id,'Send format [chat_id - reason] for ban:')
        bot.register_next_step_handler(msg, ban_user_step)
    else:
        return

@bot.message_handler(commands=['unban'])
def echo(message):
    """
    Unban a user
    """
    if message.chat.id in admins:
        msg = bot.send_message(message.chat.id,'Send chat_id to unban:')
        bot.register_next_step_handler(msg, unban_user_step)
    else:
        return

@bot.message_handler(commands=['directmessage']) #allows users to direct message friends
def echo(message):
    #if message.chat.id in admins:
    if setup_complete(message.chat.id) == False:
      bot.send_message(message.chat.id, '❗ Please setup your profile first! /setup')
      return
    else:
        msg = bot.send_message(message.chat.id,'Send Mbtie user id to create chat with:')
        bot.register_next_step_handler(msg, direct_message_step)
    #else:
        #return

@bot.message_handler(commands=['userid'])
def echo(message):
    bot.send_message(message.chat.id,'Your Mbtie User ID is:')
    bot.send_message(message.chat.id, '{}'.format(message.chat.id))
  

#### Next Step Handlers ####
def set_truth1_step(message):
     if set_truth1(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 1 set!')
        end_icebreaker_setup(message.chat.id)
     else:
        bot.send_message(message.chat.id,'Error!')
  
def set_truth2_step(message):
      if set_truth2(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 2 set!')
        end_icebreaker_setup(message.chat.id)
      else: 
        bot.send_message(message.chat.id,'Error!')

def set_lie_step(message):
      if set_lie(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Lie set!')
        end_icebreaker_setup(message.chat.id)
      else:
        bot.send_message(message.chat.id,'Error!')

def set_truth1_new(message):
    if set_truth1(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 1 set!')
    msg = bot.send_message(message.chat.id, 'Now send me your *Truth 2* statement\.', parse_mode ='MarkdownV2')
    bot.register_next_step_handler(msg, set_truth2_new)

def set_truth2_new(message):
    if set_truth2(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Truth 2 set!')
    msg = bot.send_message(message.chat.id, 'Now send me your *Lie* statement\.', parse_mode ='MarkdownV2')
    bot.register_next_step_handler(msg, set_lie_new)

def set_lie_new(message):
    if set_lie(message.chat.id,message.text):
        bot.send_message(message.chat.id,'Lie set!')
        end_icebreaker_setup(message.chat.id)

def end_icebreaker_setup(id):
    mess = "Edit your 2 Truth 1 Lie.\n \nTruth 1: {}\nTruth 2: {}\nLie: {}"
    truth1 = get_truth1(id)
    truth2 = get_truth2(id)
    lie = get_lie(id)
    bot.send_message(id, mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu())

def set_age_step(message):
    if (message.text).isdigit():
        if int(message.text) < 100 and int(message.text)>=18:
            if bool(get_age(message.chat.id)):
                set_age(message.chat.id, int(message.text))
                bot.send_message(message.chat.id,'age updated to *{}*\!'.format(message.text), parse_mode='markdownv2')
                mess = mbtinder_settings(message.chat.id)
                bot.send_message(message.chat.id, mess,reply_markup=setup_menu(), parse_mode='markdownv2')
            else:
                set_age(message.chat.id, int(message.text))
                bot.send_message(message.chat.id,'your age is set as *{}*\!'.format(message.text), parse_mode='markdownv2')
                bot.send_message(message.chat.id, 'who would you like to match with?', reply_markup = match_gender_menu())
        else:
            msg = bot.send_message(message.chat.id,'❗ invalid number! please enter a number from 18 to 99.')
            bot.register_next_step_handler(msg, set_age_step)
    else:
        msg = bot.send_message(message.chat.id,'❗ invalid entry! please enter a number!')
        bot.register_next_step_handler(msg, set_age_step)

def set_agefilter_step(message):
      x = re.fullmatch('\d\d-\d\d', message.text)
      if x:
          age_filter = x.group(0).split('-')
          if int(age_filter[0]) < 18:
              msg = bot.send_message(message.chat.id,'❗ Lower age limit cannot be below 18!')
              bot.register_next_step_handler(msg, set_agefilter_step)
          elif int(age_filter[1]) < int(age_filter[0]):
              msg =bot.send_message(message.chat.id,'❗ Upper age limit cannot be below lower limit!')
              bot.register_next_step_handler(msg, set_agefilter_step)
          elif int(age_filter[0]) == int(age_filter[1]):
              msg = bot.send_message(message.chat.id,'❗ Lower and Upper age limit cannot be the same!')
              bot.register_next_step_handler(msg, set_agefilter_step)
          else:
              set_agefilter(message.chat.id, int(age_filter[0]), int(age_filter[1]))
              agefilter = age_filter[0]+' to '+age_filter[1]
              bot.send_message(message.chat.id,'Age filter updated to *{}*\!'.format(agefilter), parse_mode='MarkdownV2')
              mess = mbtinder_settings(message.chat.id)
              bot.send_message(message.chat.id, mess, reply_markup=setup_menu(),parse_mode='MarkdownV2')
      else:
          msg = bot.send_message(message.chat.id,'❗ Invalid entry! Please enter age limits in the form of XX-XX e.g. 18-35!')
          bot.register_next_step_handler(msg, set_agefilter_step)

def broadcast_step(message):
      newtext = ''
      for i in message.text:
        if i in ['!','?','.','-']:
            i = "\\"+i
        newtext+=i
      alluser = get_all_users()
      for user in alluser:
        bot.send_message(user, '*📢 Admin: ' + newtext+'*', parse_mode='MarkdownV2')

def ban_user_step(message):
      try:
          banned = message.text
          banned = banned.split('-')
          chat_id = banned[0]
          reason = banned[1]
          set_banned(int(chat_id), reason)
          bot.send_message(message.chat.id,'Banned user {} for {}'.format(chat_id, reason))
       
      except:
          bot.send_message(message.chat.id,'Error. Try again.')
          
def unban_user_step(message):
      del_banned(int(message.text))
      bot.send_message(message.chat.id,'Unbanned user {}'.format(message.text))

def report_user_step(message):
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

def give_feedback_step(message):
    user_feedback = [message.chat.id, message.chat.username]
    bot.send_message(message.chat.id, 'Your feedback has been sent! Thank you for helping us improve MBTInder! ☺')
    for admin in admins:
        mess = 'Feedback:\n\nUser: {}\nFeedback: {}'
        bot.send_message(admin, mess.format(user_feedback, message.text))

def direct_message_step(message):
      user = int(message.text)
      if get_active_chat(user) == None:
          if user != message.chat.id:
              if bool(get_user(user)):
                  if get_active_chat(user) == None:
                      if get_queue(user) != None:
                          msg = get_message_id(user)
                          bot.delete_message(user, msg)
                          bot.delete_message(user, int(msg)-1)
                      create_chat(message.chat.id, user)
                      bot.send_message(user, '*You have entered a chat with {}\.*'.format(message.chat.id), parse_mode='MarkdownV2')
                      bot.send_message(message.chat.id, '*You have entered a chat with {}\.*'.format(message.text), parse_mode='MarkdownV2')
          
                  else:
                      bot.send_message(message.chat.id, 'User is currently in a chat!')
              else:
                  bot.send_message(message.chat.id, 'User does not exist!')
          else:
              bot.send_message(message.chat.id, 'You cannot message yourself!')
      else:
          bot.send_message(message.chat.id, 'You are already in a chat!')

def tiktok_url_step(message):
    chat_info = get_active_chat(message.chat.id)

    if get_game_message(message.chat.id)=='cancel':
        bot.send_message(message.chat.id, 'User has cancelled the TikTokBattle™')
        set_game_message(message.chat.id,None)
        set_game_message(chat_info[1],None)
        return

    if message.text == 'cancel' or message.text == 'Cancel':
        bot.send_message(message.chat.id,'You have cancelled the TikTokBattle™')
        set_game_message(chat_info[1],'cancel')
        set_tiktok_url(chat_info[1],None)
        set_game_message(message.chat.id,'cancel')
        set_tiktok_url(message.chat.id,None)
        return
    url = re.match(r'^https://vt.tiktok.com/' ,message.text)
    if url == None:
        url = re.match(r'^https://www.tiktok.com/' ,message.text)
    if url:
        url = message.text
        session = requests.Session()
        resp = session.head(url, allow_redirects=True)
        url = resp.url.split('?')[0]
        set_tiktok_url(message.chat.id,url)
       
        if get_tiktok_url(chat_info[1]) != None:
            bot.delete_message(chat_id=chat_info[1], message_id = get_game_message(chat_info[1]))
            set_game_message(chat_info[1],None)
            round = set_tiktok_round(message.chat.id)
            if round == 1:
                mess = "*TikTokBattle™ Round {}*"
            elif round == 2:
                mess = "🌚 *TikTokBattle™ Round {}* 🌝"
            elif round == 3:
                mess = "⚡ *TikTokBattle™ Round {}* ⚡"
            elif round == 4:
                mess = "❄ *TikTokBattle™ Round {}* ❄"
            elif 5 <= round < 10: 
                mess = "🔥 *TikTokBattle™ Round {}* 🔥"
            elif round >= 10:
                mess = "🔥🔥 *TikTokBattle™ Round {}* 🔥🔥"

            bot.send_message(chat_info[1], mess.format(round), reply_markup=tiktok_url_menu(url), parse_mode = 'MarkdownV2' )
            bot.send_message(message.chat.id, mess.format(round), reply_markup=tiktok_url_menu(get_tiktok_url(chat_info[1])), parse_mode = 'MarkdownV2')
            sleep(10)
            bot.send_message(chat_info[1], "Rate User's TikTok!", reply_markup=tiktok_rating(message.chat.id))
            bot.send_message(message.chat.id, "Rate User's TikTok!", reply_markup=tiktok_rating(chat_info[1]))
    
        else:
            sent = bot.send_message(message.chat.id, 'TikTok submitted. Waiting for user to submit theirs...')
            set_game_message(message.chat.id,sent.message_id)
    else:
        msg =bot.send_message(message.chat.id, "Invalid URL\! Please ensure it is in the format of vt\.tiktok\.com or tiktok\.com\. Type '_cancel_' to exit game\.",parse_mode = 'MarkdownV2')
        bot.register_next_step_handler(msg, tiktok_url_step)

@bot.message_handler(content_types=['location'])
def check_location(message):
    print(message.location.latitude)
    print(message.location.longitude)

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
            file_id = item.file_id # remove later
            print(file_id)
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
                    message.text != '/setup' and message.text != '/ttol' and message.text != '/help'\
                    and message.text != '/ban' and message.text != '/unban' and message.text != '/broadcast' \
                    and message.text != '/report' and message.text != '/feedback' and message.text != '/tiktok' and message.text != '/topic':

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

def mbtinder_settings(id):
    mess = "Edit your MBTInder profile\.\n \n*Gender*: {}\n*Match Gender*: {}\n*Age*: {}\n*Age filter*: {}\n*Purpose*: {}\n*MBTI*: {}"
    gender = get_gender(id)
    gendermatch = get_gender_match(id)
    age = get_age(id)
    agefilter = ' to '.join([str(x) for x in get_agefilter(id)])
    seeking = get_seeking(id)
    mbti = get_mbti(id)
    return mess.format(gender, gendermatch, age, agefilter, seeking, mbti)

@bot.callback_query_handler(func=lambda call: True)
def echo(call):

    if call.data == 'Male':
      bot.answer_callback_query(call.id)
      if bool(get_gender(call.message.chat.id)):
        if set_gender(call.message.chat.id, 'Male'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your gender to *Male*\.',  parse_mode = 'MarkdownV2')
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender(call.message.chat.id, 'Male'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Male* as your gender\.', parse_mode = 'MarkdownV2')
          msg = bot.send_message(call.message.chat.id, 'Please enter your age:')
          bot.register_next_step_handler(msg, set_age_step)
        else:
          return
        
    elif call.data == 'Female':
      bot.answer_callback_query(call.id)
      if bool(get_gender(call.message.chat.id)):
        if set_gender(call.message.chat.id, 'Female'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your gender to *Female*\.', parse_mode = 'MarkdownV2')
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
      else:
        if set_gender(call.message.chat.id, 'Female'):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *Female* as your gender\.', parse_mode = 'MarkdownV2')
          msg = bot.send_message(call.message.chat.id, 'Please enter your age:')
          bot.register_next_step_handler(msg, set_age_step)
        else:
          return

    elif call.data == 'Malematch': 
      bot.answer_callback_query(call.id)
      if bool(get_gender_match(call.message.chat.id)):
        if set_gender_match(call.message.chat.id, 'Male'):
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to match with *Males*\.',  parse_mode = 'MarkdownV2')
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
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
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
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
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
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
          mess = mbtinder_settings(call.message.chat.id)
          bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')         
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
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')
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

    elif call.data == 'Age':
      bot.answer_callback_query(call.id)
      msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Enter Age:')
      bot.register_next_step_handler(msg, set_age_step)

    elif call.data == 'Age filter':
      bot.answer_callback_query(call.id)
      msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Enter Age Filter in the form 'XX-XX':")
      bot.register_next_step_handler(msg, set_agefilter_step)

    #elif call.data == 'icebreaker':
    #  bot.answer_callback_query(call.id)
    #  mess = "Edit your 2 Truth 1 Lie.\n \nTruth 1: {}\nTruth 2: {}\nLie: {}"
    #  truth1 = get_truth1(call.message.chat.id)
    #  truth2 = get_truth2(call.message.chat.id)
    #  lie = get_lie(call.message.chat.id)
    #  if bool(get_truth1(call.message.chat.id)):
    #    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = mess.format(truth1, truth2, lie), reply_markup=icebreaker_setup_menu())
    #  else:
    #    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Setup your 2 Truths and 1 Lie!', reply_markup=icebreaker_setup_menu())

    elif call.data in ['truth1','truth2','lie']:
        bot.answer_callback_query(call.id)
        if call.data == 'truth1':
          msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *Truth 1* statement\.', parse_mode ='MarkdownV2')
          bot.register_next_step_handler(msg, set_truth1_step)
        elif call.data == 'truth2':
          msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *Truth 2* statement\.', parse_mode ='MarkdownV2')
          bot.register_next_step_handler(msg, set_truth2_step)
        elif call.data == 'lie':
          msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *Lie* statement\.', parse_mode ='MarkdownV2')
          bot.register_next_step_handler(msg, set_lie_step)

    #elif call.data == 'icebreaker_setup':
    #    bot.answer_callback_query(call.id)
    #    msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Send me your *Truth 1* statement\.', parse_mode ='MarkdownV2')
    #    bot.register_next_step_handler(msg, set_truth1_new)

    #elif call.data == 'complete':
    #  bot.answer_callback_query(call.id)
    #  bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Your icebreaker has been *set*\!', parse_mode='MarkdownV2')
    #  bot.send_message(call.message.chat.id,'Your profile is complete! Press the button below to start matching!',reply_markup=main_menu())

    elif call.data == 'Bot':
      bot.answer_callback_query(call.id)
      if get_active_chat(call.message.chat.id) != None:
          bot.delete_message(call.message.chat.id, call.message.message_id)
          bot.delete_message(call.message.chat.id, call.message.message_id-1)
          bot.send_message(call.message.chat.id, '*Setup exited\. You may resume your chat\!*', parse_mode='MarkdownV2')
      else:
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Click the button below to start matching!',reply_markup=main_menu())

    elif call.data == 'setupback': 
      bot.answer_callback_query(call.id)
      mess = mbtinder_settings(call.message.chat.id)
      bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

    elif call.data in ['ISFP', 'ISFJ', 'ISTP', 'ISTJ','ESFP', 'ESFJ', 'ESTP', 'ESTJ', 'INFP', 'INFJ', 'INTP', 'INTJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'mbti_skip']: 
      bot.answer_callback_query(call.id)
      if bool(get_mbti(call.message.chat.id)):
        if call.data == 'mbti_skip':
            set_mbti(call.message.chat.id, 'Not set')
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to skip setting of MBTI type'.format(call.data))
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

        else: 
            set_mbti(call.message.chat.id, call.data)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You updated your MBTI type to *{}*\.'.format(call.data),  parse_mode = 'MarkdownV2')
            mess = mbtinder_settings(call.message.chat.id)
            bot.send_message(call.message.chat.id, mess, reply_markup=setup_menu(), parse_mode = 'MarkdownV2')

      elif call.data == 'mbti_skip':
          set_mbti(call.message.chat.id, 'Not set')
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You chose to skip setting of MBTI type'.format(call.data))
          bot.send_message(call.message.chat.id,'Your profile is complete! Press the button below to start matching!',reply_markup=main_menu())

      else:
        if set_mbti(call.message.chat.id, call.data):
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You selected *{}* as your MBTI type\.'.format(call.data),  parse_mode = 'MarkdownV2')
          bot.send_message(call.message.chat.id,'Your profile is complete! Press the button below to start matching!',reply_markup=main_menu())
        else:
          return

    elif call.data == 'cancel_report':
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == 'make_report':
        bot.answer_callback_query(call.id)
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Please enter your reason for reporting:')
        bot.register_next_step_handler(msg, report_user_step)

    elif call.data == 'retype_report':
        bot.answer_callback_query(call.id)
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Re-type your reason for reporting.')
        bot.register_next_step_handler(msg, report_user_step)

    elif call.data == 'confirm_report':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Report succesfully submitted! An admin will contact you should further information be required.')
        for admin in admins:
            user_reporting = call.message.chat.id
            bot.send_message(admin, 'Latest report from {} confirmed'.format(user_reporting))

    elif call.data == 'make_feedback':
        bot.answer_callback_query(call.id)
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Enter your feedback:')
        bot.register_next_step_handler(msg, give_feedback_step)

    elif call.data == 'endchat':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        if chat_info[1] in admins:
            return
        else:
            delete_chat(chat_info[0])
            bot.send_message(chat_info[1], 'Your match has ended the chat. Input /start to start searching for another match!', reply_markup = types.ReplyKeyboardRemove())
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'You have ended the chat. Input /start to start searching for another match!', reply_markup = types.ReplyKeyboardRemove())

    elif call.data == 'topics_accept':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        bot.delete_message(chat_id = chat_info[1], message_id = get_game_message(chat_info[1]))
        msg1 = bot.send_photo(chat_id = call.message.chat.id, photo = messages.topics_step0, caption = "Welcome to *MBTI Topics™\!* Press 'Generate Topic' button or use \/topic to generate a random MBTI Topic\.", parse_mode='MarkdownV2', reply_markup = topics_tutorial(1))
        msg2 = bot.send_photo(chat_id = chat_info[1], photo = messages.topics_step0, caption = "Welcome to *MBTI Topics™\!* Press 'Generate Topic' button or use \/topic to generate a random MBTI Topic\.", parse_mode='MarkdownV2', reply_markup = topics_tutorial(1))
        set_game_message(chat_info[1],'topics')
        set_game_message(call.message.chat.id,'topics') #In-game identifier

    elif call.data == 'topics_start':
         bot.answer_callback_query(call.id)
         chat_info = get_active_chat(call.message.chat.id)
         bot.send_message(call.message.chat.id, 'You have rolled the dice for a random topic.')
         bot.send_message(chat_info[1], 'User has rolled the dice for a random topic.')
         mbti1 = get_mbti(call.message.chat.id)
         mbti2 = get_mbti(chat_info[1])
         match = mbti_cognitive_match(mbti1,mbti2)
         if len(match) == 0:
             if mbti1 == 'Not set':
                 match = ['Ni','Ne','Si','Se','Ti','Te','Fi','Fe']
             else:
                 match = messages.mbti_cf[mbti1]
         cognitive_func = random.choice(match)
         msg = bot.send_dice(call.message.chat.id)
         topic = messages.topics[cognitive_func][msg.dice.value]
         sleep(3)
         bot.send_message(call.message.chat.id, '__Cognitive function: {}__\nTopic: *{}*'.format(messages.cf[cognitive_func],topic), parse_mode='MarkdownV2', reply_markup = topics_reroll())
         bot.send_message(chat_info[1], '__Cognitive function: {}__\nTopic: *{}*'.format(messages.cf[cognitive_func],topic), parse_mode='MarkdownV2')

    elif call.data == 'topics_step0':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.topics_step0, caption = "Welcome to *MBTI Topics™\!* Press 'Generate Topic' button or use \/topic to generate a random MBTI Topic\.", parse_mode='MarkdownV2'), reply_markup = topics_tutorial(1))

    elif call.data == 'topics_step1':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.topics_step1, caption = 'Click the button below to generate a topic. Topics are generated based on the MBTI cognitive functions that you and your match have in common.'), reply_markup = topics_tutorial(2))

    elif call.data == 'topics_step2':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.topics_step2, caption = "You may generate another topic using /topic."), reply_markup = topics_tutorial(3))

    elif call.data == 'topics_step3':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.topics_step3,  caption = "For more information about the 8 cognitive functions visit https://www.psychologyjunkie.com/2018/02/23/introduction-cognitive-functions-myers-briggs-theory/"), reply_markup = topics_tutorial(4))

    elif call.data == 'ttol_accept':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        bot.delete_message(chat_id = chat_info[1], message_id = get_game_message(chat_info[1]))
        msg1 = bot.send_photo(chat_id = call.message.chat.id, photo = messages.ttol, caption = "Welcome to *2Truths1Lie™\!*\nPress 'start' to play\!", parse_mode='MarkdownV2', reply_markup = ttol_tutorial(1))
        msg2 = bot.send_photo(chat_id = chat_info[1], photo = messages.ttol, caption = "Welcome to *2Truths1Lie™\!*\nPress 'start' to play\!", parse_mode='MarkdownV2', reply_markup = ttol_tutorial(1))
        set_game_message(chat_info[1],'game')
        set_game_message(call.message.chat.id,'game') #In-game identifier

    elif call.data == 'ttol_start':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol, caption = "Welcome to *2Truths1Lie™\!*\nPress 'start' to play\!",parse_mode='MarkdownV2'), reply_markup = ttol_tutorial(11))
        msg = bot.send_message(call.message.chat.id, 'Send me your *Truth 1* statement\.', parse_mode ='MarkdownV2')
        bot.register_next_step_handler(msg, set_truth1_new)

    elif call.data == 'ttol_step0':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol, caption = "Welcome to *2Truths1Lie™\!*\nPress 'start' to play\!",parse_mode='MarkdownV2'), reply_markup = ttol_tutorial(1))

    elif call.data == 'ttol_step1':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol_step1, caption = 'Send your truth and lie statements to the bot, one by one.'), reply_markup = ttol_tutorial(2))

    elif call.data == 'ttol_step2':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol_step2, caption = "Check if your statements are correct. Edit them if necessary. Hit 'Confirm and Submit' when you're done."), reply_markup = ttol_tutorial(3))

    elif call.data == 'ttol_step3':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol_step3,  caption = "Finally, you will be sent a quiz. Try to guess your match's lie statement! Chat about your guesses and get to know one another!"), reply_markup = ttol_tutorial(4))

    elif call.data == 'ttol_step10':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol, caption = "Welcome to *2Truths1Lie™\!*\nPress 'start' to play\!",parse_mode='MarkdownV2'), reply_markup = ttol_tutorial(11))

    elif call.data == 'ttol_step11':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol_step1, caption = 'Send your truth and lie statements to the bot, one by one.'), reply_markup = ttol_tutorial(12))

    elif call.data == 'ttol_step12':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol_step2, caption = "Check if your statements are correct. Edit them if necessary. Hit 'Confirm and Submit' when you're done."), reply_markup = ttol_tutorial(13))

    elif call.data == 'ttol_step13':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.ttol_step3,  caption = "Finally, you will be sent a quiz. Try to guess your match's lie statement! Chat about your guesses and get to know one another!"), reply_markup = ttol_tutorial(14))

    elif call.data == 'ttol_quiz':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id = call.message.message_id)
        if get_icebreaker(call.message.chat.id):
            
            if get_game_message(chat_info[1]).isdigit():
                bot.delete_message(chat_id=chat_info[1], message_id = get_game_message(chat_info[1]))
                set_game_message(chat_info[1],None)
                set_game_message(call.message.chat.id,None)
                truth1_1 = get_truth1(chat_info[1])
                truth2_1 = get_truth2(chat_info[1])
                lie_1 = get_lie(chat_info[1])
                statements1 = [truth1_1 ,truth2_1,lie_1]
                random.shuffle(statements1)
                ans1 = statements1.index(lie_1)
                userPoll[call.message.chat.id] = [ans1,statements1]

                truth1_2 = get_truth1(call.message.chat.id)
                truth2_2 = get_truth2(call.message.chat.id)
                lie_2 = get_lie(call.message.chat.id)
                statements2 = [truth1_2 ,truth2_2,lie_2]
                random.shuffle(statements2)
                ans2 = statements2.index(lie_2)
                userPoll[chat_info[1]] = [ans2,statements2]

                bot.send_poll(chat_info[1], '2Truths1Lie™. Select the Lie! 🙊', options = statements2, correct_option_id=ans2, type = 'quiz', is_anonymous= False)
                bot.send_poll(call.message.chat.id, '2Truths1Lie™. Select the Lie! 🙊', options = statements1, correct_option_id=ans1, type = 'quiz', is_anonymous= False)
 
            else:
                sent = bot.send_message(call.message.chat.id, '2Truths1Lie™ submitted. Waiting for user to submit theirs...')
                set_game_message(call.message.chat.id,sent.message_id)
        else:
            bot.send_message(call.message.chat.id, '❗ You have not set an ice breaker!')

    elif call.data == 'ttol_decline':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You have declined their request for a game of 2Truths1Lie™.')
        bot.edit_message_text(chat_id = chat_info[1],message_id = get_game_message(chat_info[1]), text= 'User has declined your request for a game of 2Truths1Lie™.')
        set_game_message(chat_info[1],None)

    elif call.data == 'tiktok_step0':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.tiktokbattle, caption = "Welcome to *TikTokBattle™\!*\nSubmit your TikTok URL for battle\.\nType '_cancel_' to exit\.",parse_mode='MarkdownV2'), reply_markup = tiktok_tutorial(1))

    elif call.data == 'tiktok_step1':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.tiktok_step1, caption = 'Press the share button on your TikTok video. Copy the link and paste it in this chat. Should you encounter inappropriate material, please make a /report.'), reply_markup = tiktok_tutorial(2))

    elif call.data == 'tiktok_step2':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.tiktok_step2, caption = "Click the button to watch your opponent's TikTok."), reply_markup = tiktok_tutorial(3))

    elif call.data == 'tiktok_step3':
        bot.answer_callback_query(call.id)
        message_id = call.message.message_id
        chat_id = call.message.chat.id
        bot.edit_message_media(chat_id = chat_id, message_id = message_id, media = types.InputMediaPhoto(messages.tiktok_step3,  caption = "Finally, rate your opponent's TikTok on a scale of 1-10. If their TikTok is exceptionally good you may select 😂💯❤️"), reply_markup = tiktok_tutorial(4))


    elif call.data == 'tiktok_accept':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        bot.delete_message(chat_id = chat_info[1], message_id = get_game_message(chat_info[1]))
        msg1 = bot.send_photo(chat_id = call.message.chat.id, photo = messages.tiktokbattle, caption = "Welcome to *TikTokBattle™\!*\nSubmit your TikTok URL for battle\.\nType '_cancel_' to exit\.", parse_mode='MarkdownV2', reply_markup = tiktok_tutorial(1))
        msg2 = bot.send_photo(chat_id = chat_info[1], photo = messages.tiktokbattle, caption = "Welcome to *TikTokBattle™\!*\nSubmit your TikTok URL for battle\.\nType '_cancel_' to exit\.", parse_mode='MarkdownV2', reply_markup = tiktok_tutorial(1))
        set_game_message(chat_info[1],'game')
        set_game_message(call.message.chat.id,'game')
        bot.register_next_step_handler(msg1, tiktok_url_step)
        bot.register_next_step_handler(msg2, tiktok_url_step)

    elif call.data == 'tiktok_help': # Add in help menu
        bot.send_photo(chat_id = call.message.chat.id, photo = messages.tiktokbattle, caption = "Welcome to *TikTokBattle™\* Tutorial", parse_mode='MarkdownV2', reply_markup = tiktok_tutorial(1))


    elif call.data == 'tiktok_encore':
        bot.answer_callback_query(call.id)
        bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id)
        chat_info = get_active_chat(call.message.chat.id)
       
        if get_game_message(chat_info[1]) == 'cancel':
            bot.send_message(call.message.chat.id, 'User did not want another round.')
            set_game_message(chat_info[1],None)
            set_game_message(call.message.chat.id,None)

        elif get_game_message(chat_info[1]) != None:

            if get_game_message(chat_info[1]).isdigit():
                msg1 = bot.send_message(call.message.chat.id,  "Yay another round\!\nSubmit your next TikTok URL for battle:\nType '_cancel_' to exit\." ,parse_mode='markdownv2')
                bot.register_next_step_handler(msg1, tiktok_url_step)
                msg2 = bot.edit_message_text(chat_id = chat_info[1], message_id = get_game_message(chat_info[1]), text = "Another round\!\nSubmit your next TikTok URL for battle:\nType '_cancel_' to exit\.",parse_mode='markdownv2')
                bot.register_next_step_handler(msg2, tiktok_url_step)
                set_game_message(chat_info[1],'game')
                set_game_message(call.message.chat.id,'game')

        else:
            sent = bot.send_message(call.message.chat.id, 'You have asked for another round. Waiting for user to reply...')
            set_game_message(call.message.chat.id, sent.message_id)
        

    elif call.data == 'tiktok_decline_encore':
        bot.answer_callback_query(call.id)
        bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.send_message(call.message.chat.id, 'You chose not to have another round.')
        set_game_message(call.message.chat.id,'cancel')
        
        if get_game_message(chat_info[1]) == 'cancel':
            bot.send_message(call.message.chat.id, 'User also did not want another round.')
            set_game_message(chat_info[1],None)
            set_game_message(call.message.chat.id,None)

        elif get_game_message(chat_info[1]).isdigit():
            bot.edit_message_text(chat_id = chat_info[1], message_id = get_game_message(chat_info[1]), text = 'User did not want another round.')
            set_game_message(chat_info[1],None)
            set_game_message(call.message.chat.id,None)
            

    elif call.data == 'tiktok_decline':
        bot.answer_callback_query(call.id)
        chat_info = get_active_chat(call.message.chat.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'You have declined their request for a TikTokBattle™.')
        bot.edit_message_text(chat_id = chat_info[1],message_id = get_game_message(chat_info[1]), text= 'User has declined your request for a TikTokBattle™.')
        set_game_message(chat_info[1],None)

    elif call.data[:8] == 'ttbattle':
        bot.answer_callback_query(call.id)
        info = call.data
        player_id = int(info.split('-')[1])
        score = int(info.split('-')[2])
        set_tiktok_url(player_id,score)
        
        if get_tiktok_url(call.message.chat.id).isdigit():
            bot.delete_message(chat_id=player_id, message_id=get_game_message(player_id))
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            set_game_message(player_id,None)
            set_game_message(call.message.chat.id,None)
            user = get_tiktok_url(call.message.chat.id)
            other = get_tiktok_url(player_id)
            scoreconversion = {"1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","91":"10","92":"100"} #this is because database of score is str based, 10 and 100 needs to be converted to 91 and 92 respectively
            if other > user:
                set_tiktok_win(player_id)
                user = scoreconversion[user]
                other = scoreconversion[other]
                bot.send_message(call.message.chat.id, 'User rated your TikTok *{}*\.\nYou rated their TikTok *{}*\.\n\n*🙊 User won the battle\!*'.format(user,other), parse_mode='MarkdownV2')
                bot.send_message(player_id, 'User rated your TikTok *{}*\.\nYou rated their TikTok *{}*\.\n\n*🏆 You won the battle\!*'.format(other,user), parse_mode='MarkdownV2')

            elif user > other:
                set_tiktok_win(call.message.chat.id)
                user = scoreconversion[user]
                other = scoreconversion[other]
                bot.send_message(call.message.chat.id, 'User rated your TikTok *{}*\.\nYou rated their TikTok *{}*\.\n\n*🏆 You won the battle\!*'.format(user,other), parse_mode='MarkdownV2')
                bot.send_message(player_id, 'User rated your TikTok *{}*\.\nYou rated their TikTok *{}*\.\n\n*🙊 User won the battle\!*'.format(other,user), parse_mode='MarkdownV2')

            elif user == other:
                user = scoreconversion[user]
                other = scoreconversion[other]
                bot.send_message(call.message.chat.id, "User rated your TikTok *{}*\.\nYou rated their TikTok *{}*\.\n\n*👔 It\'s a tie\!*".format(user,other), parse_mode='MarkdownV2')
                bot.send_message(player_id, "User rated your TikTok *{}*\.\nYou rated their TikTok *{}*\.\n\n*👔 It\'s a tie\!*".format(other,user), parse_mode='MarkdownV2')

            set_tiktok_url(player_id, None)
            set_tiktok_url(call.message.chat.id, None)
            round = get_tiktok_round(call.message.chat.id)
            win1 = get_tiktok_win(call.message.chat.id)
            win2 = get_tiktok_win(player_id)
            tally = '__TikTokBattle™ Scoreboard__\nYou: *{}*\nUser: *{}*'
            bot.send_message(call.message.chat.id, tally.format(win1,win2), parse_mode='MarkdownV2', reply_markup= tiktok_encore_menu())
            bot.send_message(player_id, tally.format(win2,win1), parse_mode='MarkdownV2', reply_markup= tiktok_encore_menu())

        else:
            sent = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Waiting for user to rate your TikTok...')
            set_game_message(call.message.chat.id, sent.message_id)

    elif call.data == 'about':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = messages.about, reply_markup = about_menu())

    elif call.data == 'backtohelp':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = messages.help, reply_markup=help_menu() ,parse_mode = 'MarkdownV2')

    elif call.data == 'NewChat':

      if get_queue(call.message.chat.id) != None:
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❗ You are already in the queue!')
      
      elif setup_complete(call.message.chat.id) == False:
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❗ Your profile is incomplete!')

      elif call.message.chat.id in get_banned():
          bot.answer_callback_query(call.id)
          reason = get_banned_reason(call.message.chat.id)
          bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = '❗ You have been banned!\n\nReason: {}'.format(reason))

      elif get_active_chat(call.message.chat.id) == None:
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        gendermatch = get_gender_match(call.message.chat.id) # Get all user info
        gender = get_gender(call.message.chat.id)
        age = get_age(call.message.chat.id)
        agefilter = get_agefilter(call.message.chat.id)
        agefilter_ll = agefilter[0]
        agefilter_ul = agefilter[1]
        seeking = get_seeking(call.message.chat.id)
        mbti = get_mbti(call.message.chat.id)

        user_info = get_gender_chat(gender, gendermatch, age, agefilter_ll, agefilter_ul, seeking) # Look for match and obtain match's info
        chat_two = user_info[0]
        gender2 = user_info[1]
        age2 = user_info[2]
        seeking2 = user_info[3]
        mbti2 = user_info[4]
        msg = get_message_id(chat_two)

        if create_chat(call.message.chat.id, chat_two) == False:
                  bot.send_sticker(call.message.chat.id, messages.search_sticker)
                  sent = bot.send_message(call.message.chat.id, 'Searching for a suitable match...', reply_markup = stop_search())
                  add_queue(call.message.chat.id, gender, gendermatch, age, agefilter_ll, agefilter_ul, seeking, mbti, sent.message_id)
        else:
                  mess = 'Gender: {}\nAge: {}\nPurpose: {}\nMBTI: {}\n\nInput /stop to end the chat.'
                  bot.delete_message(chat_two, msg)
                  bot.delete_message(chat_two, int(msg)-1)
                  bot.send_sticker(call.message.chat.id, messages.match_sticker)
                  bot.send_message(call.message.chat.id, mess.format(gender2, age2, seeking2, mbti2), reply_markup=stop_dialog())
                  bot.send_sticker(chat_two, messages.match_sticker)
                  bot.send_message(chat_two, mess.format(gender, age, seeking, mbti), reply_markup=stop_dialog())
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
