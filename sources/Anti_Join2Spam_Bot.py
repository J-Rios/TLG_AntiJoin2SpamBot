# -*- coding: utf-8 -*-
'''
Script:
    Anti_Join2Spam_Bot.py
Description:
    Telegram Bot that figth against the spammer users that join groups to spam their annoying and 
    unwanted info.
Author:
    Jose Rios Rubio
Creation date:
    04/04/2018
Last modified date:
    12/04/2018
Version:
    1.2.1
'''

####################################################################################################

### Imported modules ###
import re
import sys
import signal
import TSjson
from os import path, makedirs, listdir
from datetime import datetime, timedelta
from time import time, sleep, strptime, mktime
from threading import Thread, Lock
from Constants import CONST, TEXT
from operator import itemgetter
from collections import OrderedDict
from telegram import MessageEntity, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, \
                         ConversationHandler, CallbackQueryHandler

####################################################################################################

### Globals ###
lang = CONST['INIT_LANG']
enable = CONST['INIT_ENABLE']
time_for_allow_urls_h = CONST['INIT_TIME_ALLOW_URLS']
num_messages_for_allow_urls = CONST['INIT_MIN_MSG_ALLOW_URLS']
call_admins_when_spam_detected = CONST['INIT_CALL_ADMINS_WHEN_SPAM']
files_users_list = []
files_messages_list = []
files_config_list = []
to_delete_messages_list = []

####################################################################################################

### Termination signals handler for program process ###
def signal_handler(signal, frame):
    '''Termination signals (SIGINT, SIGTERM) handler for program process'''
    print('Closing the program, safe way...')
    # Acquire all messages and users files mutex to ensure not read/write operation on them
    for chat_users_file in files_users_list:
        chat_users_file['File'].lock.acquire()
    for chat_messages_file in files_messages_list:
        chat_messages_file['File'].lock.acquire()
    # Close the program
    sys.exit(0)


### Signals attachment ###
signal.signal(signal.SIGTERM, signal_handler) # SIGTERM (kill pid) to signal_handler
signal.signal(signal.SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler

####################################################################################################

### General functions ###

def initialize_resources():
    '''Initialize resources by populating files list and configs with chats found files'''
    global lang
    global enable
    global time_for_allow_urls_h
    global num_messages_for_allow_urls
    global call_admins_when_spam_detected
    global files_users_list
    global files_messages_list
    global files_config_list
    # Create data directory if it does not exists
    if not path.exists(CONST['DATA_DIR']):
        makedirs(CONST['DATA_DIR'])
    else:
        # If directry data exists, check all subdirectories names (chats ID)
        files = listdir(CONST['DATA_DIR'])
        if files:
            for f in files:
                # Populate users files list
                users_file = OrderedDict([('ID', None), ('File', None)])
                users_file['ID'] = f
                users_file['File'] = get_chat_users_file(f)
                files_users_list.append(users_file)
                # Populate messages files list
                messages_file = OrderedDict([('ID', None), ('File', None)])
                messages_file['ID'] = f
                messages_file['File'] = get_chat_messages_file(f)
                files_messages_list.append(messages_file)
                # Restore last configurations properties of the chat
                config_file = OrderedDict([('ID', None), ('File', None)])
                config_file['ID'] = f
                config_file['File'] = get_chat_config_file(f)
                config_data = config_file['File'].read()
                if config_data:
                    lang = config_data['Language']
                    enable = config_data['Antispam']
                    time_for_allow_urls_h = config_data['Time_for_allow_urls_h']
                    num_messages_for_allow_urls = config_data['Num_messages_for_allow_urls']
                    call_admins_when_spam_detected = config_data['Call_admins_when_spam_detected']
                files_config_list.append(config_file)


def get_chat_users_file(chat_id):
    '''Determine chat users file from the list by ID. Get the file if exists or create it if not'''
    file = OrderedDict([('ID', chat_id), ('File', None)])
    found = False
    if files_users_list:
        for chat_file in files_users_list:
            if chat_file['ID'] == chat_id:
                file = chat_file
                found = True
                break
        if not found:
            chat_users_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_USERS'])
            file['ID'] = chat_id
            file['File'] = TSjson.TSjson(chat_users_file_name)
            files_users_list.append(file)
    else:
        chat_users_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_USERS'])
        file['ID'] = chat_id
        file['File'] = TSjson.TSjson(chat_users_file_name)
        files_users_list.append(file)
    return file['File']


def get_chat_messages_file(chat_id):
    '''Determine chat msgs file from the list by ID. Get the file if exists or create it if not'''
    file = OrderedDict([('ID', chat_id), ('File', None)])
    file = {'ID': chat_id, 1: 7.8}
    found = False
    if files_messages_list:
        for chat_file in files_messages_list:
            if chat_file['ID'] == chat_id:
                file = chat_file
                found = True
                break
        if not found:
            chat_messages_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_MSG'])
            file['File'] = TSjson.TSjson(chat_messages_file_name)
            files_messages_list.append(file)
    else:
        chat_messages_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_MSG'])
        file['File'] = TSjson.TSjson(chat_messages_file_name)
        files_messages_list.append(file)
    return file['File']


def get_chat_config_file(chat_id):
    '''Determine chat config file from the list by ID. Get the file if exists or create it if not'''
    file = OrderedDict([('ID', chat_id), ('File', None)])
    found = False
    if files_config_list:
        for chat_file in files_config_list:
            if chat_file['ID'] == chat_id:
                file = chat_file
                found = True
                break
        if not found:
            chat_config_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_CONF'])
            file['ID'] = chat_id
            file['File'] = TSjson.TSjson(chat_config_file_name)
            files_config_list.append(file)
    else:
        chat_config_file_name = '{}/{}/{}'.format(CONST['DATA_DIR'], chat_id, CONST['F_CONF'])
        file['ID'] = chat_id
        file['File'] = TSjson.TSjson(chat_config_file_name)
        files_config_list.append(file)
    return file['File']


def save_config_properties(chat_id):
    '''Store actual chat configuration in file'''
    fjson_config = get_chat_config_file(chat_id)
    config_data = fjson_config.read()
    if not config_data:
        config_data = OrderedDict( \
        [ \
            ('Language', lang), \
            ('Antispam', enable), \
            ('Time_for_allow_urls_h', time_for_allow_urls_h), \
            ('Num_messages_for_allow_urls', num_messages_for_allow_urls), \
            ('Call_admins_when_spam_detected', call_admins_when_spam_detected) \
        ])
    else:
        config_data['Language'] = lang
        config_data['Antispam'] = enable
        config_data['Time_for_allow_urls_h'] = time_for_allow_urls_h
        config_data['Num_messages_for_allow_urls'] = num_messages_for_allow_urls
        config_data['Call_admins_when_spam_detected'] = call_admins_when_spam_detected
    fjson_config.write(config_data)


def register_new_user(chat_id, user_id, user_name, join_date):
    '''Add new member to the users file'''
    # Default new user data
    user_data = OrderedDict( \
    [ \
        ('User_id', user_id), \
        ('User_name', user_name), \
        ('Join_date', join_date), \
        ('Num_messages', 0) \
    ])
    # Get the chat users file and write the user data to it
    fjson_usr = get_chat_users_file(chat_id)
    fjson_usr.write_content(user_data)


def add_new_message(chat_id, msg_id, user_id, user_name, text, msg_date):
    '''Add new message to the messages file'''
    # Default new message data
    msg_data = OrderedDict( \
    [ \
        ('Chat_id', chat_id), \
        ('Msg_id', msg_id), \
        ('User_id', user_id), \
        ('User_name', user_name), \
        ('Text', text), \
        ('Date', msg_date) \
    ])
    # Get the chat messages file and write the messages data to it
    fjson_msg = get_chat_messages_file(chat_id)
    fjson_msg.write_content(msg_data)


def get_user(chat_id, user_id):
    '''Get user data by member ID'''
    fjson_usr = get_chat_users_file(chat_id)
    users_data = fjson_usr.read_content()
    for usr in users_data:
        if user_id == usr['User_id']:
            return usr
    return None


def get_message(chat_id, msg_id):
    '''Get message data of a chat by ID'''
    fjson_msg = get_chat_messages_file(chat_id)
    messages_data = fjson_msg.read_content()
    for msg in messages_data:
        if chat_id == msg['Chat_id']:
            if msg_id == msg['Msg_id']:
                return msg    
    return None


def user_in_json(chat_id, user_id):
    '''Check if a user is in the file by his ID'''
    fjson_usr = get_chat_users_file(chat_id)
    users_data = fjson_usr.read_content()
    for usr in users_data:
        if user_id == usr['User_id']:
            return True
    return False


def update_user(chat_id, new_user_data):
    '''Update an existing user from the JSON file. If the user does not exists, add to it'''
    fjson_usr = get_chat_users_file(chat_id)
    user_id = new_user_data['User_id']
    if user_in_json(chat_id, user_id):
        fjson_usr.update(new_user_data, 'User_id')
    else:
        fjson_usr.write_content(new_user_data)


def user_is_admin(bot, user_id, chat_id):
    '''Check if the specified user is an Administrator of a group given by IDs'''
    try:
        group_admins = bot.get_chat_administrators(chat_id)
    except:
        return None
    for admin in group_admins:
        if user_id == admin.user.id:
            return True
    return False


def bot_is_admin(bot, chat_id):
    '''Check if the Bot is Admin of the actual group'''
    try:
        bot_id = bot.id
        group_admins = bot.get_chat_administrators(chat_id)
    except:
        return None
    for admin in group_admins:
        if bot_id == admin.user.id:
            return True
    return False


def get_admins_usernames_in_string(bot, chat_id):
    '''Get all the group Administrators usernames/alias in a single line string separed by \' \''''
    admins = ""
    group_admins = bot.get_chat_administrators(chat_id)
    for admin in group_admins:
        if admins == "":
            admins = "@{}".format(admin.user.username)
        else:
            admins = "{}\n@{}".format(admins, admin.user.username)
    return admins

####################################################################################################

### Received Telegram not-command messages handlers ###

def new_user(bot, update):
    '''New member join the group event handler'''
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    join_date = (update.message.date).now().strftime("%Y-%m-%d %H:%M:%S")
    register_new_user(chat_id, user_id, user_name, join_date)


def msg_nocmd(bot, update):
    '''All Not-command messages handler'''
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    msg_date = (update.message.date).now().strftime("%Y-%m-%d %H:%M:%S")
    text = update.message.text
    # If it is a text message
    if text != None:
        # If user not yet register, add to users file, else, get his number of published messages
        if not user_in_json(chat_id, user_id):
            # Register user and set "Num_messages" and "Join_date" to allow publish URLs
            register_new_user(chat_id, user_id, user_name, msg_date)
            user_data = get_user(chat_id, user_id)
            user_data['Num_messages'] = num_messages_for_allow_urls
            user_data['Join_date'] = datetime(1971, 1, 1).strftime("%Y-%m-%d %H:%M:%S")
            update_user(chat_id, user_data)
            num_published_messages = num_messages_for_allow_urls + 1
        else:
            user_data = get_user(chat_id, user_id)
            user_data['Num_messages'] = user_data['Num_messages'] + 1
            update_user(chat_id, user_data)
            num_published_messages = user_data['Num_messages']
        # If the user is not an Admin and the Bot Anti-Spam is enabled
        is_admin = user_is_admin(bot, user_id, chat_id)
        if (is_admin != True) and (enable == True):
            # If there is any URL in the message
            any_url = re.findall(CONST['REGEX_URLS'], text)
            if any_url:
                # Check user time in the group
                user_join_date = user_data['Join_date']
                user_join_date_dateTime = strptime(user_join_date, "%Y-%m-%d %H:%M:%S")
                msg_date_dateTime = strptime(msg_date, "%Y-%m-%d %H:%M:%S")
                t0 = mktime(user_join_date_dateTime) # Date to epoch
                t1 = mktime(msg_date_dateTime) # Date to epoch
                user_hours_in_group = (t1 - t0)/3600
                # If user is relatively new in the group or has not write enough messages
                if ((user_hours_in_group < time_for_allow_urls_h) or 
                    (num_published_messages < num_messages_for_allow_urls)):
                        # Delete user message and notify what happen
                        bot.delete_message(chat_id=chat_id, message_id=msg_id)
                        bot_msg_head = TEXT[lang]['MSG_SPAM_HEADER']
                        bot_msg_0 = TEXT[lang]['MSG_SPAM_DETECTED_0'].format(user_name)
                        bot_msg_1 = TEXT[lang]['MSG_SPAM_DETECTED_1'].format( \
                            time_for_allow_urls_h, num_messages_for_allow_urls)
                        bot_message = "{}{}{}".format(bot_msg_head, bot_msg_0, bot_msg_1)
                        if call_admins_when_spam_detected:
                            admins = get_admins_usernames_in_string(bot, chat_id)
                            if admins:
                                bot_msg_2 = TEXT[lang]['CALLING_ADMINS'].format(admins)
                                bot_message = "{}{}".format(bot_message, bot_msg_2)
                        bot.send_message(chat_id, bot_message)
        # Truncate the message text to 500 characters
        if len(text) > 50:
            text = text[0:50]
            text = "{}...".format(text)
        # Add the message to messages file
        add_new_message(chat_id, msg_id, user_id, user_name, text, msg_date)
    
####################################################################################################

### Received Telegram command messages handlers ###

def cmd_start(bot, update):
    '''Command /start message handler'''
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, update.message.chat_id, TEXT[lang]['START'])


def cmd_help(bot, update):
    '''Command /help message handler'''
    bot_msg = TEXT[lang]['HELP'].format(CONST['INIT_TIME_ALLOW_URLS'], \
        CONST['INIT_MIN_MSG_ALLOW_URLS'], CONST['T_DEL_MSG'])
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, update.message.chat_id, bot_msg)


def cmd_commands(bot, update):
    '''Command /commands message handler'''
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, update.message.chat_id, TEXT[lang]['COMMANDS'])


def cmd_language(bot, update, args):
    '''Command /language message handler'''
    global lang
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if len(args) == 1:
            lang_provided = args[0]
            if lang_provided == 'en' or lang_provided == 'es':
                lang_provided = lang_provided.upper()
                if lang_provided != lang:
                    lang = lang_provided
                    save_config_properties(chat_id)
                    bot_msg = TEXT[lang]['LANG_CHANGE']
                else:
                    bot_msg = TEXT[lang]['LANG_SAME']
            else:
                bot_msg = TEXT[lang]['LANG_BAD_LANG']
        else:
            bot_msg = TEXT[lang]['LANG_NOT_ARG']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_set_messages(bot, update, args):
    '''Command /set_messages message handler'''
    global num_messages_for_allow_urls
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if len(args) == 1:
            num_msgs_provided = args[0]
            if num_msgs_provided.isdigit():
                num_msgs_provided = int(num_msgs_provided)
                if num_msgs_provided >= 0:
                    num_messages_for_allow_urls = num_msgs_provided
                    save_config_properties(chat_id)
                    bot_msg = TEXT[lang]['SET_MSG_CHANGED'].format(num_messages_for_allow_urls)
                else:
                    bot_msg = TEXT[lang]['SET_MSG_NEGATIVE']
            else:
                bot_msg = TEXT[lang]['SET_MSG_BAD_ARG']
        else:
            bot_msg = TEXT[lang]['SET_MSG_NOT_ARG']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_set_hours(bot, update, args):
    '''Command /set_hours message handler'''
    global time_for_allow_urls_h
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if len(args) == 1:
            hours_provided = args[0]
            if hours_provided.isdigit():
                hours_provided = int(hours_provided)
                if hours_provided >= 0:
                    time_for_allow_urls_h = hours_provided
                    save_config_properties(chat_id)
                    bot_msg = TEXT[lang]['SET_HOURS_CHANGED'].format(time_for_allow_urls_h)
                else:
                    bot_msg = TEXT[lang]['SET_HOURS_NEGATIVE_HOUR']
            else:
                bot_msg = TEXT[lang]['SET_HOURS_BAD_ARG']
        else:
            bot_msg = TEXT[lang]['SET_HOURS_NOT_ARG']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_status(bot, update):
    '''Command /status message handler'''
    bot_msg = TEXT[lang]['STATUS'].format(num_messages_for_allow_urls, time_for_allow_urls_h, \
        call_admins_when_spam_detected, enable)
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, update.message.chat_id, bot_msg)


def cmd_call_admins(bot, update):
    '''Command /call_admins message handler'''
    chat_id = update.message.chat_id
    admins = get_admins_usernames_in_string(bot, chat_id)
    bot_msg = TEXT[lang]['CALLING_ADMINS'].format(admins)
    bot.send_message(chat_id, bot_msg)


def cmd_call_when_spam(bot, update, args):
    '''Command /cmd_call_when_spam message handler'''
    global call_admins_when_spam_detected
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if len(args) == 1:
            value_provided = args[0]
            if value_provided == 'enable' or value_provided == 'disable':
                if value_provided == 'enable':
                    if call_admins_when_spam_detected == True:
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_ALREADY_ENABLE']
                    else:
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_ENABLE']
                        call_admins_when_spam_detected = True
                        save_config_properties(chat_id)
                else:
                    if call_admins_when_spam_detected == True:
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_DISABLE']
                        call_admins_when_spam_detected = False
                        save_config_properties(chat_id)
                    else:
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_ALREADY_DISABLE']
            else:
                bot_msg = TEXT[lang]['CALL_WHEN_SPAM_NOT_ARG']
        else:
            bot_msg = TEXT[lang]['CALL_WHEN_SPAM_NOT_ARG']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_enable(bot, update):
    '''Command /disable message handler'''
    global enable
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if enable:
            bot_msg = TEXT[lang]['ALREADY_ENABLE']
        else:
            enable = True
            save_config_properties(chat_id)
            bot_msg = TEXT[lang]['ENABLE']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_disable(bot, update):
    '''Command /disable message handler'''
    global enable
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    is_admin = user_is_admin(bot, user_id, chat_id)
    if is_admin == True:
        if enable:
            enable = False
            save_config_properties(chat_id)
            bot_msg = TEXT[lang]['DISABLE']
        else:
            bot_msg = TEXT[lang]['ALREADY_DISABLE']
    elif is_admin == False:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    else:
        bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_version(bot, update):
    '''Command /version message handler'''
    bot_msg = TEXT[lang]['VERSION'].format(CONST['VERSION'])
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, update.message.chat_id, bot_msg)


def cmd_about(bot, update):
    '''Command /cmd_about handler'''
    bot_msg = TEXT[lang]['ABOUT_MSG'].format(CONST['DEVELOPER'], CONST['REPOSITORY'])
    tlg_msg_to_selfdestruct(bot, update.message)
    tlg_send_selfdestruct_msg(bot, update.message.chat_id, bot_msg)

####################################################################################################

def tlg_send_selfdestruct_msg(bot, chat_id, message):
    '''tlg_send_selfdestruct_msg_in() with default delete time'''
    tlg_send_selfdestruct_msg_in(bot, chat_id, message, CONST['T_DEL_MSG'])


def tlg_msg_to_selfdestruct(bot, message):
    '''tlg_msg_to_selfdestruct_in() with default delete time'''
    tlg_msg_to_selfdestruct_in(bot, message, CONST['T_DEL_MSG'])


def tlg_send_selfdestruct_msg_in(bot, chat_id, message, time_delete_min):
    '''Send a telegram message that will be auto-delete in specified time'''
    # Send the message
    sent_msg = bot.send_message(chat_id, message)
    # If has been succesfully sent
    if sent_msg:
        # Get sent message ID and delete time
        msg_id = sent_msg.message_id
        destroy_time = int(time()) + int(time_delete_min*60)
        # Add sent message data to to-delete messages list
        sent_msg_data = OrderedDict([('Chat_id', None), ('Msg_id', None), ('delete_time', None)])
        sent_msg_data['Chat_id'] = chat_id
        sent_msg_data['Msg_id'] = msg_id
        sent_msg_data['delete_time'] = destroy_time
        to_delete_messages_list.append(sent_msg_data)


def tlg_msg_to_selfdestruct_in(bot, message, time_delete_min):
    '''Add a telegram message to be auto-delete in specified time''' 
    # Get sent message ID and delete time
    chat_id = message.chat_id
    msg_id = message.message_id
    destroy_time = int(time()) + int(time_delete_min*60)
    # Check if the Bot is Admin
    if bot_is_admin(bot, chat_id) == True:
        # Add sent message data to to-delete messages list
        sent_msg_data = OrderedDict([('Chat_id', None), ('Msg_id', None), ('delete_time', None)])
        sent_msg_data['Chat_id'] = chat_id
        sent_msg_data['Msg_id'] = msg_id
        sent_msg_data['delete_time'] = destroy_time
        to_delete_messages_list.append(sent_msg_data)


def selfdestruct_messages(bot):
    '''Handle remove messages sent by the Bot with the timed self-delete function'''
    global to_delete_messages_list
    while True:
        # Check each Bot sent message
        for sent_msg in to_delete_messages_list:
            # If actual time is equal or more than the expected sent msg delete time
            if int(time()) >= sent_msg['delete_time']:
                # Delete that sent message
                bot.delete_message(chat_id=sent_msg['Chat_id'], message_id=sent_msg['Msg_id'])
                to_delete_messages_list.remove(sent_msg)
        # Wait 10s (release CPU usage)
        sleep(10)


####################################################################################################

### Main Function ###

def main():
    '''Main Function'''
    # Initialize resources by populating files list and configs with chats found files
    initialize_resources()
    # Create an event handler (updater) for a Bot with the given Token and get the dispatcher
    updater = Updater(CONST['TOKEN'])
    dp = updater.dispatcher
    # Set to dispatcher a not-command messages handler
    dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.audio | Filters.voice | \
        Filters.video | Filters.sticker | Filters.document | Filters.location | Filters.contact, \
        msg_nocmd))
    # Set to dispatcher a new member join the group event handler
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))
    # Set to dispatcher all expected commands messages handler
    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CommandHandler("help", cmd_help))
    dp.add_handler(CommandHandler("commands", cmd_commands))
    dp.add_handler(CommandHandler("language", cmd_language, pass_args=True))
    dp.add_handler(CommandHandler("set_messages", cmd_set_messages, pass_args=True))
    dp.add_handler(CommandHandler("set_hours", cmd_set_hours, pass_args=True))
    dp.add_handler(CommandHandler("status", cmd_status))
    dp.add_handler(CommandHandler("call_admins", cmd_call_admins))
    dp.add_handler(CommandHandler("call_when_spam", cmd_call_when_spam, pass_args=True))
    dp.add_handler(CommandHandler("enable", cmd_enable))
    dp.add_handler(CommandHandler("disable", cmd_disable))
    dp.add_handler(CommandHandler("version", cmd_version))
    dp.add_handler(CommandHandler("about", cmd_about))
    # Launch the Bot ignoring pending messages (clean=True)
    updater.start_polling(clean=True)
    # Handle self-messages delete
    selfdestruct_messages(updater.bot)


if __name__ == '__main__':
    main()

### End Of Code ###
