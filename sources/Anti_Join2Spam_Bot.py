#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    Anti_Join2Spam_Bot.py
Description:
    Telegram Bot that figths against the spammer users that join groups to publish their annoying 
    and unwanted info.
Author:
    Jose Rios Rubio
Creation date:
    04/04/2018
Last modified date:
    10/06/2022
Version:
    1.11.0
'''

####################################################################################################

### Imported modules ###

import re
import TSjson

from platform import system as os_system

from signal import signal, SIGTERM, SIGINT
if os_system() != "Windows":
    from signal import SIGUSR1

from sys import exit

from os import kill, getpid, path, makedirs, listdir

from datetime import datetime, timedelta

from time import time, sleep, strptime, mktime, strftime

from threading import Thread, Lock

from operator import itemgetter

from collections import OrderedDict

from telegram import (
    Update, ParseMode
)

from telegram.ext import (
    CallbackContext, Updater, CommandHandler,
    ChatMemberHandler, MessageHandler, Filters,
    Defaults
)

from telegram.error import (
    TelegramError, Unauthorized, BadRequest,
    TimedOut, NetworkError
)

from Constants import CONST, TEXT

####################################################################################################

### Debug Flag ###
DEBUG = True

### Globals ###
updater = None
allowed_groups = []
files_users_list = []
files_messages_list = []
files_config_list = []
to_delete_messages_list = []
sent_antispam_messages_list = []
owner_notify = False
th_0 = None
force_exit = False

####################################################################################################

### Termination Signals Handler For Program Process

def signal_handler(signal,  frame):
    '''Termination signals (SIGINT, SIGTERM) handler for program process'''
    global force_exit
    global updater
    global th_0
    debug_print("Termination signal received. Releasing resources...")
    # Close the Bot instance (it wait for updater, dispatcher and other internals threads to end)
    if updater is not None:
        debug_print("Closing Bot...")
        updater.stop()
    # Acquire all messages and users files mutex to ensure not read/write operation on them
    for chat_users_file in files_users_list:
        chat_users_file['File'].lock.acquire()
    for chat_messages_file in files_messages_list:
        chat_messages_file['File'].lock.acquire()
    for chat_config_file in files_config_list:
        chat_config_file['File'].lock.acquire()
    # Wait to end threads
    force_exit = True
    debug_print("Waiting th_0 end...")
    if th_0 is not None:
        if th_0.is_alive():
            th_0.join()
    # Close the program
    debug_print("All resources released.")
    debug_print("Exit 0")
    exit(0)


### Signals attachment

signal(SIGTERM, signal_handler) # SIGTERM (kill pid) to signal_handler
signal(SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler
if os_system() != "Windows":
    signal(SIGUSR1, signal_handler) # SIGUSR1 (self-send) to signal_handler

####################################################################################################

### Debug print ###

def debug_print(text):
    '''Function to print text just when DEBUG flag is active'''
    if DEBUG:
        actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[{}] - {}".format(actual_time, text))


def debug_print_tlg(bot, text):
    '''Function to send text message to TLG chat just when DEBUG flag is active'''
    if DEBUG:
        try:
            bot.send_message(CONST['DEBUG_TO_CHAT'], text)
        except:
            pass

####################################################################################################

### General functions ###

def initialize_resources():
    '''Initialize resources by populating files list with chats found files'''
    # Create data directories and files if does not exists
    if not path.exists(CONST['DATA_DIR']):
        makedirs(CONST['DATA_DIR'])
    # Get allowed groups from persistent groups file
    f_json_groups = TSjson.TSjson(CONST['F_GROUPS'])
    groups_json = f_json_groups.read()
    if groups_json:
        if 'ID' in groups_json:
            for group_id in groups_json['ID']:
                allowed_groups.append(group_id)
    else:
        list_id = []
        list_id.append(CONST['OWNER_ID'])
        groups_json = OrderedDict([('ID', list_id)])
        f_json_groups.write(groups_json)
        allowed_groups.append(CONST['OWNER_ID'])
    # Check all subdirectories names (chats ID)
    files = listdir(CONST['DATA_DIR'])
    if files:
        if 'groups.json' in files:
            files.remove('groups.json')
        for f_chat_id in files:
            # Populate users files list
            file_path = '{}/{}/{}'.format(CONST['DATA_DIR'], f_chat_id, CONST['F_USERS'])
            files_users_list.append(OrderedDict([('ID', f_chat_id), \
                ('File', TSjson.TSjson(file_path))]))
            # Populate messages files list
            file_path = '{}/{}/{}'.format(CONST['DATA_DIR'], f_chat_id, CONST['F_MSG'])
            files_messages_list.append(OrderedDict([('ID', f_chat_id), \
                ('File', TSjson.TSjson(file_path))]))
            # Populate config files list
            file_path = '{}/{}/{}'.format(CONST['DATA_DIR'], f_chat_id, CONST['F_CONF'])
            files_config_list.append(OrderedDict([('ID', f_chat_id), \
                ('File', TSjson.TSjson(file_path))]))
            # Create default configuration file if it does not exists
            if not path.exists(file_path):
                default_conf = get_default_config_data()
                for key, value in default_conf.items():
                    save_config_property(f_chat_id, key, value)


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


def get_default_config_data():
    '''Get default config data structure'''
    config_data = OrderedDict( \
    [ \
        ('Title', CONST['INIT_TITLE']), \
        ('Link', CONST['INIT_LINK']), \
        ('Language', CONST['INIT_LANG']), \
        ('Antispam', CONST['INIT_ENABLE']), \
        ('Time_for_allow_urls_h', CONST['INIT_TIME_ALLOW_URLS']), \
        ('Num_messages_for_allow_urls', CONST['INIT_MIN_MSG_ALLOW_URLS']), \
        ('Call_admins_when_spam_detected', CONST['INIT_CALL_ADMINS_WHEN_SPAM']), \
        ('Allow_users_to_add_bots', CONST['INIT_ALLOW_USERS_ADD_BOTS'])
    ])
    return config_data


def save_allowed_group(group_id):
    '''Store a new allowed group'''
    f_json_groups = TSjson.TSjson(CONST['F_GROUPS'])
    groups_json = f_json_groups.read()
    if groups_json:
        if 'ID' in groups_json:
            groups_json['ID'].append(group_id)
        else:
            list_id = []
            list_id.append(group_id)
            groups_json = OrderedDict([('ID', list_id)])
    else:
        list_id = []
        list_id.append(group_id)
        groups_json = OrderedDict([('ID', list_id)])
    f_json_groups.write(groups_json)


def save_config_property(chat_id, property, value):
    '''Store actual chat configuration in file'''
    fjson_config = get_chat_config_file(chat_id)
    config_data = fjson_config.read()
    if not config_data:
        config_data = get_default_config_data()
    config_data[property] = value
    fjson_config.write(config_data)


def get_chat_config(chat_id, param):
    '''Get specific stored chat configuration property'''
    file = get_chat_config_file(chat_id)
    if file:
        config_data = file.read()
        if not config_data:
            config_data = get_default_config_data()
    else:
        config_data = get_default_config_data()
    return config_data[param]


def register_new_user(chat_id, user_id, user_name, join_date, allow_user):
    '''Add new member to the users file'''
    # Default new user data
    user_data = OrderedDict( \
    [ \
        ('User_id', user_id), \
        ('User_name', user_name), \
        ('Join_date', join_date), \
        ('Num_messages', 0), \
        ('Allow_user', allow_user) \
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


def get_message(chat_id, msg_id):
    '''Get message data of a chat by ID'''
    fjson_msg = get_chat_messages_file(chat_id)
    messages_data = fjson_msg.read_content()
    for msg in messages_data:
        if chat_id == msg['Chat_id']:
            if msg_id == msg['Msg_id']:
                return msg
    return None


def get_user_from_id(chat_id, user_id):
    '''Get user data by member ID'''
    fjson_usr = get_chat_users_file(chat_id)
    users_data = fjson_usr.read_content()
    for usr in users_data:
        if user_id == usr['User_id']:
            return usr
    return None


def get_user_from_alias(chat_id, user_alias):
    '''Get user from an alias'''
    fjson_usr = get_chat_users_file(chat_id)
    users_data = fjson_usr.read_content()
    for usr in users_data:
        if user_alias == usr['User_name']:
            return usr
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
    list_admins_names = list()
    try:
        group_admins = bot.get_chat_administrators(chat_id)
    except Exception as e:
        debug_print("Exception when checking Admins of {} - {}".format(chat_id, str(e)))
        return None
    for admin in group_admins:
        if admin.user.is_bot == False: # Ignore Bots
            list_admins_names.append(admin.user.username)
    for admin_name in sorted(list_admins_names):
        if admins == "":
            admins = "@{}".format(admin_name)
        else:
            admins = "{}\n@{}".format(admins, admin_name)
    return admins


def is_int(s):
    '''Check if the string is an integer number'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def notify_all_chats(bot, message):
    '''Publish a notify message in all the Chats where the Bot is'''
    # If directory data exists, check all subdirectories names (chats ID)
    chats_files = listdir(CONST['DATA_DIR'])
    if chats_files:
        for chat_id in chats_files:
            # Don't publish in private chats
            if chat_id[0] == '-':
                try:
                    bot.send_message(chat_id, message)
                except Exception as e:
                    debug_print("Exception when publishing in {} - {}".format(chat_id, str(e)))


def bot_leave_chat(bot, chat_id):
    '''Thread Function to try Bot leave a group.'''
    left = False
    while not left:
        try:
            bot.leave_chat(chat_id)
            left = True
        except Exception as e:
            debug_print('Bot fail to leave the chat "{}": {}'.format(chat_id, str(e)))
            sleep(5)

####################################################################################################

### Received Telegram not-command messages handlers ###

def left_user(update: Update, context: CallbackContext):
    '''Member left the group event handler'''
    bot = context.bot
    chat_id = update.message.chat.id
    if chat_id in allowed_groups:
        message_id = update.message.message_id
        user = update.message.left_chat_member
        left_user_name = "{} {}".format(user.first_name, user.last_name)
        # Delete left message if the user name has an URL or is too long
        has_url = re.findall(CONST['REGEX_URLS'], left_user_name)
        try:
            if has_url:
                bot.delete_message(chat_id, message_id)
            else:
                if len(left_user_name) > 30:
                    bot.delete_message(chat_id, message_id)
        except:
            pass


def new_user(update: Update, context: CallbackContext):
    '''New member join the group event handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    msg_from_user_id = update.message.from_user.id
    msg_from_user_name = update.message.from_user.name
    join_date = (update.message.date).now().strftime("%Y-%m-%d %H:%M:%S")
    lang = get_chat_config(chat_id, 'Language')
    # For each new user that join or has been added
    for join_user in update.message.new_chat_members:
        join_user_id = join_user.id
        join_user_alias = join_user.name
        join_user_name = "{} {}".format(update.message.from_user.first_name, \
            update.message.from_user.last_name)
        # If the added user is not myself (this Bot)
        if bot.id != join_user_id:
            # If it is an allowed group
            if chat_id in allowed_groups:
                to_register_user = True
                # If the message user source is not the join user, it has been invited/added by another
                if msg_from_user_id != join_user_id:
                    # If the member that has been join the group is a Bot
                    if update.message.new_chat_members[0].is_bot:
                        # If the user that has been added the Bot is not an Admin
                        if not user_is_admin(bot, msg_from_user_id, chat_id):
                            # If not allow users to add Bots
                            if get_chat_config(chat_id, 'Allow_users_to_add_bots') == False:
                                # Kick the Added Bot and notify
                                debug_print("An user has added a Bot.\n  (Chat) - ({}).".format( \
                                    chat_id))
                                try:
                                    bot.kickChatMember(chat_id, join_user_id)
                                    bot_message = TEXT[lang]['USER_CANT_ADD_BOT'].format \
                                        (msg_from_user_name, join_user_alias)
                                    debug_print("Added Bot successfully kicked.\n  (Chat) - ({}).". \
                                        format(chat_id))
                                except Exception as e:
                                    debug_print("Exception when kicking a Bot - {}".format(str(e)))
                                    if str(e) == "Not enough rights to restrict/unrestrict chat member":
                                        bot_message = TEXT[lang]['USER_CANT_ADD_BOT_CANT_KICK'].format \
                                            (msg_from_user_name, join_user_alias)
                                call_admins_when_spam_detected = get_chat_config(chat_id, \
                                    'Call_admins_when_spam_detected')
                                if call_admins_when_spam_detected:
                                    admins = get_admins_usernames_in_string(bot, chat_id)
                                    if admins:
                                        bot_msg_2_append = TEXT[lang]['CALLING_ADMINS'].format(admins)
                                        bot_message = "{}{}".format(bot_message, bot_msg_2_append)
                                tlg_send_selfdestruct_msg(bot, chat_id, bot_message)
                                to_register_user = False
                if to_register_user:
                    # Check if there is an URL in the user name
                    has_url = re.findall(CONST['REGEX_URLS'], join_user_name)
                    if has_url:
                        debug_print("Spammer (URL name) join detected.\n  (Chat) - ({}).".format( \
                            chat_id))
                        if len(join_user_name) > 10:
                            join_user_name = join_user_name[0:10]
                            join_user_name = "{}...".format(join_user_name)
                        try:
                            bot.delete_message(chat_id, message_id)
                            bot_message = TEXT[lang]['USER_URL_NAME_JOIN'].format(join_user_name)
                            debug_print("Spammer (URL name) join message successfully removed.\n" \
                                "  (Chat) - ({}).".format(chat_id))
                            tlg_send_selfdestruct_msg(bot, chat_id, bot_message)
                        except Exception as e:
                            debug_print("Exception when deleting a Spammer (URL name) join " \
                                "message - {}".format(str(e)))
                            if str(e) == "Message can't be deleted":
                                bot_message = TEXT[lang]['USER_URL_NAME_JOIN_CANT_REMOVE'].format( \
                                    join_user_name)
                                bot.send_message(chat_id, bot_message)
                    else:
                        # Check if user name and last name are too long
                        if len(join_user_name) > 30:
                            join_user_name = join_user_name[0:10]
                            join_user_name = "{}...".format(join_user_name)
                            try:
                                bot.delete_message(chat_id, message_id)
                                bot_message = TEXT[lang]['USER_LONG_NAME_JOIN'].format(join_user_name)
                                debug_print("Spammer (long name) join message successfully removed.\n" \
                                    "  (Chat) - ({}).".format(chat_id))
                                tlg_send_selfdestruct_msg(bot, chat_id, bot_message)
                            except Exception as e:
                                debug_print("Exception when deleting a Spammer (long name) join " \
                                    "message - {}".format(str(e)))
                                if str(e) == "Message can't be deleted":
                                    bot_message = TEXT[lang]['USER_LONG_NAME_JOIN_CANT_REMOVE']. \
                                        format(join_user_name)
                                    bot.send_message(chat_id, bot_message)
                    if len(join_user_alias) > 50:
                        join_user_alias = join_user_alias[0:50]
                        join_user_alias = "{}...".format(join_user_alias)
                    if not user_in_json(chat_id, join_user_id):
                        register_new_user(chat_id, join_user_id, join_user_alias, join_date, False)
        # The Anti-Spam Bot has been added to a group
        else:
            # Get the language of the Telegram client software that the Admin that has added the Bot to
            # assume this is the chat language and configure Bot language
            admin_language = update.message.from_user.language_code[0:2]
            if admin_language == 'es':
                lang = 'ES'
            else:
                lang = 'EN'
            chat_title = update.message.chat.title
            chat_link = update.message.chat.username
            admin_name = update.message.from_user.name
            admin_id = update.message.from_user.id
            if chat_id in allowed_groups:
                save_config_property(chat_id, 'Language', lang)
                # Notify to Bot Owner that the Bot has been added to a group
                notify_msg = "The Bot has been added to a new group:\n\n"
                notify_msg = "{}- ID: {}\n".format(notify_msg, chat_id)
                if chat_title:
                    save_config_property(chat_id, 'Title', chat_title)
                    notify_msg = "{}- Title: {}\n".format(notify_msg, chat_title)
                else:
                    notify_msg = "{}- Title: Unknown\n".format(notify_msg)
                if chat_link:
                    chat_link = '@{}'.format(chat_link)
                    save_config_property(chat_id, 'Link', chat_link)
                    notify_msg = "{}- Link: {}\n".format(notify_msg, chat_link)
                else:
                    notify_msg = "{}- Link: Unknown\n".format(notify_msg)
                notify_msg = "{}- Admin: {} [{}]".format(notify_msg, admin_name, admin_id)
                debug_print_tlg(bot, notify_msg)
                # Send bot join message
                bot_message = TEXT[lang]['ANTI-SPAM_BOT_ADDED_TO_GROUP_ALLOW']
                bot.send_message(chat_id, bot_message)
            else:
                # Notify to Bot Owner that the Bot has been added to a group
                notify_msg = "The Bot has been added to a not allowed group:\n\n"
                notify_msg = "{}- ID: {}\n".format(notify_msg, chat_id)
                if chat_title:
                    save_config_property(chat_id, 'Title', chat_title)
                    notify_msg = "{}- Title: {}\n".format(notify_msg, chat_title)
                else:
                    notify_msg = "{}- Title: Unknown\n".format(notify_msg)
                if chat_link:
                    chat_link = '@{}'.format(chat_link)
                    save_config_property(chat_id, 'Link', chat_link)
                    notify_msg = "{}- Link: {}\n".format(notify_msg, chat_link)
                else:
                    notify_msg = "{}- Link: Unknown\n".format(notify_msg)
                notify_msg = "{}- Admin: {} [{}]".format(notify_msg, admin_name, admin_id)
                debug_print(notify_msg)
                debug_print_tlg(bot, notify_msg)
                # Bot message
                bot_message = TEXT[lang]['ANTI-SPAM_BOT_ADDED_TO_GROUP_NOT_ALLOW'].format(chat_id)
                bot.send_message(chat_id, bot_message)
                # Launch Bot leave group thread
                thread = Thread(target=bot_leave_chat, args=(bot, chat_id))
                thread.setDaemon(True)
                thread.start()


def msg_nocmd(update: Update, context: CallbackContext):
    '''All Not-command messages handler'''
    global owner_notify
    bot = context.bot
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    user_id = update.message.from_user.id
    lang = get_chat_config(chat_id, 'Language')
    ## Handle on Private Chat Conversation ##
    if chat_type == "private":
        if user_id == CONST['OWNER_ID']:
            if owner_notify == True:
                owner_notify = False
                message = update.message.text
                notify_all_chats(bot, message)
                bot.send_message(chat_id, TEXT[lang]['CMD_NOTIFY_ALL_OK'])
        return
    ## Handle on Groups/Channels ##
    # Leave not allowed groups
    if chat_id not in allowed_groups:
        # Bot message
        bot_message = TEXT[lang]['ANTI-SPAM_BOT_ADDED_TO_GROUP_NOT_ALLOW'].format(chat_id)
        bot.send_message(chat_id, bot_message)
        # Launch Bot leave group thread
        thread = Thread(target=bot_leave_chat, args=(bot, chat_id))
        thread.setDaemon(True)
        thread.start()
        return
    chat_title = update.message.chat.title
    if chat_title:
        save_config_property(chat_id, 'Title', chat_title)
    chat_link = update.message.chat.username
    if chat_link:
        chat_link = '@{}'.format(chat_link)
        save_config_property(chat_id, 'Link', chat_link)
    msg_id = update.message.message_id
    user_name = update.message.from_user.name
    msg_date = (update.message.date).now().strftime("%Y-%m-%d %H:%M:%S")
    text = update.message.text
    if text == None:
        text = getattr(update.message, "caption_html", None)
        if text == None:
            text = getattr(update.message, "caption", None)
    enable = get_chat_config(chat_id, 'Antispam')
    time_for_allow_urls_h = get_chat_config(chat_id, 'Time_for_allow_urls_h')
    num_messages_for_allow_urls = get_chat_config(chat_id, 'Num_messages_for_allow_urls')
    call_admins_when_spam_detected = get_chat_config(chat_id, 'Call_admins_when_spam_detected')
    # If user not yet register, add to users file, else, get his number of published msgs
    if not user_in_json(chat_id, user_id):
        # Register user and set "Num_messages" and "Join_date" to allow publish URLs
        register_new_user(chat_id, user_id, user_name, msg_date, True)
        user_data = get_user_from_id(chat_id, user_id)
        user_data['Num_messages'] = num_messages_for_allow_urls + 1
        user_data['Join_date'] = datetime(1971, 1, 1).strftime("%Y-%m-%d %H:%M:%S")
        update_user(chat_id, user_data)
    else:
        # Increase num messages count
        user_data = get_user_from_id(chat_id, user_id)
        user_data['Num_messages'] = user_data['Num_messages'] + 1
        update_user(chat_id, user_data)
        # If it is a text message
        if text != None:
            # If the user is not an Admin and the Bot Anti-Spam is enabled
            is_admin = user_is_admin(bot, user_id, chat_id)
            if (is_admin != True) and (enable == True):
                # If there is any URL in the message
                any_url = re.findall(CONST['REGEX_URLS'], text)
                if any_url:
                    # If user does not have allowed to publish
                    if user_data['Allow_user'] == False:
                        num_published_messages = user_data['Num_messages']
                        # Check user time in the group
                        user_join_date = user_data['Join_date']
                        user_join_date_dateTime = strptime(user_join_date, "%Y-%m-%d %H:%M:%S")
                        msg_date_dateTime = strptime(msg_date, "%Y-%m-%d %H:%M:%S")
                        t0 = mktime(user_join_date_dateTime) # Date to epoch
                        t1 = mktime(msg_date_dateTime) # Date to epoch
                        user_hours_in_group = (t1 - t0)/3600
                        # If user is relatively new in the group or has not write enough msgs
                        if ((user_hours_in_group < time_for_allow_urls_h) or 
                            (num_published_messages < num_messages_for_allow_urls + 1)):
                            debug_print("Spam message detected.\n  (Chat, User, Message) - " \
                                "({}, {}, {}).".format(chat_id, user_name, user_id))
                            # Decrease this message from the user messages count
                            user_data['Num_messages'] = user_data['Num_messages'] - 1
                            update_user(chat_id, user_data)
                            # Check if there was another spam messages in the chat from same
                            # user, and remove it
                            for antispam_msg in sent_antispam_messages_list:
                                if (antispam_msg['User_id'] == user_id) and \
                                    (antispam_msg['Chat_id'] == chat_id):
                                    # Try to delete that sent message if possible (still exists)
                                    try:
                                        if bot.delete_message(chat_id, antispam_msg['Msg_id']):
                                            sent_antispam_messages_list.remove(antispam_msg)
                                            debug_print("Previous Spam message successfully " \
                                                "removed.\n  (Chat, User, Message) - " \
                                                "({}, {}, {}).".format(chat_id, user_name, \
                                                user_id))
                                    except Exception as e:
                                        debug_print("Exception when deleting a previous Spam " \
                                            "message from an user - {}".format(str(e)))
                                        sent_antispam_messages_list.remove(antispam_msg)
                            # Delete user message and notify what happen
                            bot_msg_head = TEXT[lang]['MSG_SPAM_HEADER']
                            try:
                                if bot.delete_message(chat_id, msg_id):
                                    bot_msg_0 = TEXT[lang]['MSG_SPAM_DETECTED_0'].format( \
                                        user_name)
                                    bot_msg_1 = TEXT[lang]['MSG_SPAM_DETECTED_1'].format( \
                                        num_messages_for_allow_urls, time_for_allow_urls_h)
                                    bot_message = "{}{}{}".format(bot_msg_head, bot_msg_0, \
                                        bot_msg_1)
                                    debug_print("Spam message successfully removed.\n  " \
                                        "(Chat, User, Message) - ({}, {}, {}).".format( \
                                        chat_id, user_name, user_id))
                            except Exception as e:
                                debug_print("Exception when deleting an Spam message - {}". \
                                    format(str(e)))
                                if str(e) == "Message can't be deleted":
                                    bot_message = "{}{}".format(bot_msg_head, \
                                        TEXT[lang]['MSG_SPAM_DETECTED_CANT_REMOVE'])
                            if call_admins_when_spam_detected:
                                admins = get_admins_usernames_in_string(bot, chat_id)
                                if admins:
                                    bot_msg_2 = TEXT[lang]['CALLING_ADMINS'].format(admins)
                                    bot_message = "{}{}".format(bot_message, bot_msg_2)
                            sent_msg = bot.send_message(chat_id, bot_message, \
                                parse_mode=ParseMode.HTML)
                            # Store sent anti-spam message in to delete list
                            antispam_msg = OrderedDict( \
                            [ \
                                ('User_id', user_id), \
                                ('Chat_id', chat_id), \
                                ('Msg_id', sent_msg.message_id), \
                                ('Msg_date', t1) \
                            ])
                            sent_antispam_messages_list.append(antispam_msg)
                        # If the user is allowed to publish URLs
                        else:
                            # Give user permission
                            user_data['Allow_user'] = True
                            update_user(chat_id, user_data)
            # Truncate the message text to 500 characters
            if len(text) > 50:
                text = text[0:50]
                text = "{}...".format(text)
            # Add the message to messages file
            add_new_message(chat_id, msg_id, user_id, user_name, text, msg_date)
    # Remove from list all messages from 5h ago or more
    msg_date_epoch = mktime(strptime(msg_date, "%Y-%m-%d %H:%M:%S")) # Date string to epoch
    for antispam_msg in sent_antispam_messages_list:
        if msg_date_epoch - antispam_msg['Msg_date'] >= 40:
            sent_antispam_messages_list.remove(antispam_msg)

####################################################################################################

### Received Telegram command messages handlers ###

def cmd_start(update: Update, context: CallbackContext):
    '''Command /start message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        if chat_type == "private":
            bot.send_message(chat_id, TEXT[lang]['START'])
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['START'])


def cmd_help(update: Update, context: CallbackContext):
    '''Command /help message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        bot_msg = TEXT[lang]['HELP'].format(CONST['INIT_TIME_ALLOW_URLS'], \
            CONST['INIT_MIN_MSG_ALLOW_URLS'], CONST['T_DEL_MSG'])
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_commands(update: Update, context: CallbackContext):
    '''Command /commands message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        if chat_type == "private":
            bot.send_message(chat_id, TEXT[lang]['COMMANDS'])
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['COMMANDS'])


def cmd_language(update: Update, context: CallbackContext):
    '''Command /language message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        allow_command = True
        if chat_type != "private":
            is_admin = user_is_admin(bot, user_id, chat_id)
            if is_admin == False:
                allow_command = False
        if allow_command:
            if len(args) == 1:
                lang_provided = args[0]
                if lang_provided == 'en' or lang_provided == 'es':
                    lang_provided = lang_provided.upper()
                    if lang_provided != lang:
                        lang = lang_provided
                        save_config_property(chat_id, 'Language', lang)
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
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_set_messages(update: Update, context: CallbackContext):
    '''Command /set_messages message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == True:
            if len(args) == 1:
                num_msgs_provided = args[0]
                if num_msgs_provided.isdigit():
                    num_msgs_provided = int(num_msgs_provided)
                    if num_msgs_provided >= 0:
                        save_config_property(chat_id, 'Num_messages_for_allow_urls', num_msgs_provided)
                        bot_msg = TEXT[lang]['SET_MSG_CHANGED'].format(num_msgs_provided)
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
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_set_hours(update: Update, context: CallbackContext):
    '''Command /set_hours message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == True:
            if len(args) == 1:
                hours_provided = args[0]
                if hours_provided.isdigit():
                    hours_provided = int(hours_provided)
                    if hours_provided >= 0:
                        save_config_property(chat_id, 'Time_for_allow_urls_h', hours_provided)
                        bot_msg = TEXT[lang]['SET_HOURS_CHANGED'].format(hours_provided)
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
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_status(update: Update, context: CallbackContext):
    '''Command /status message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        enable = get_chat_config(chat_id, 'Antispam')
        num_messages_for_allow_urls = get_chat_config(chat_id, 'Num_messages_for_allow_urls')
        time_for_allow_urls_h = get_chat_config(chat_id, 'Time_for_allow_urls_h')
        call_admins_when_spam_detected = get_chat_config(chat_id, 'Call_admins_when_spam_detected')
        allow_users_to_add_bots = get_chat_config(chat_id, 'Allow_users_to_add_bots')
        bot_msg = TEXT[lang]['STATUS'].format(num_messages_for_allow_urls, time_for_allow_urls_h, \
            call_admins_when_spam_detected, allow_users_to_add_bots, enable)
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_call_admins(update: Update, context: CallbackContext):
    '''Command /call_admins message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        lang = get_chat_config(chat_id, 'Language')
        admins = get_admins_usernames_in_string(bot, chat_id)
        if admins:
            bot_msg = TEXT[lang]['CALLING_ADMINS'].format(admins)
        else:
            bot_msg = TEXT[lang]['CALLING_ADMINS_NO_ADMINS']
        bot.send_message(chat_id, bot_msg)


def cmd_call_when_spam(update: Update, context: CallbackContext):
    '''Command /call_when_spam message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        call_admins_when_spam_detected = get_chat_config(chat_id, 'Call_admins_when_spam_detected')
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
                            save_config_property(chat_id, 'Call_admins_when_spam_detected', \
                                call_admins_when_spam_detected)
                    else:
                        if call_admins_when_spam_detected == True:
                            bot_msg = TEXT[lang]['CALL_WHEN_SPAM_DISABLE']
                            call_admins_when_spam_detected = False
                            save_config_property(chat_id, 'Call_admins_when_spam_detected', \
                                call_admins_when_spam_detected)
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
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_users_add_bots(update: Update, context: CallbackContext):
    '''Command /users_add_bots message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        allow_users_to_add_bots = get_chat_config(chat_id, 'Allow_users_to_add_bots')
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == True:
            if len(args) == 1:
                value_provided = args[0]
                if value_provided == 'enable' or value_provided == 'disable':
                    if value_provided == 'enable':
                        if allow_users_to_add_bots == True:
                            bot_msg = TEXT[lang]['USERS_ADD_BOTS_ALREADY_ENABLE']
                        else:
                            bot_msg = TEXT[lang]['USERS_ADD_BOTS_ENABLE']
                            allow_users_to_add_bots = True
                            save_config_property(chat_id, 'Allow_users_to_add_bots', \
                                allow_users_to_add_bots)
                    else:
                        if allow_users_to_add_bots == True:
                            bot_msg = TEXT[lang]['USERS_ADD_BOTS_DISABLE']
                            allow_users_to_add_bots = False
                            save_config_property(chat_id, 'Allow_users_to_add_bots', \
                                allow_users_to_add_bots)
                        else:
                            bot_msg = TEXT[lang]['USERS_ADD_BOTS_ALREADY_DISABLE']
                else:
                    bot_msg = TEXT[lang]['USERS_ADD_BOTS_NOT_ARG']
            else:
                bot_msg = TEXT[lang]['USERS_ADD_BOTS_NOT_ARG']
        elif is_admin == False:
            bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
        else:
            bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_allow_user(update: Update, context: CallbackContext):
    '''Command /allow_user message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        lang = get_chat_config(chat_id, 'Language')
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == True:
            if len(args) >= 1:
                user_alias = ""
                for arg in args:
                    if user_alias == "":
                        user_alias = arg
                    else:
                        user_alias = "{} {}".format(user_alias, arg)
                user_data = get_user_from_alias(chat_id, user_alias)
                if user_data != None:
                    if user_data['Allow_user'] == False:
                        user_data['Allow_user'] = True
                        update_user(chat_id, user_data)
                        bot_msg = TEXT[lang]['CMD_ALLOW_USR_OK'].format(user_alias)
                    else:
                        bot_msg = TEXT[lang]['CMD_ALLOW_USR_ALREADY_ALLOWED'].format(user_alias)
                else:
                    bot_msg = TEXT[lang]['CMD_ALLOW_USR_NOT_FOUND']
            else:
                bot_msg = TEXT[lang]['CMD_ALLOW_USR_NOT_ARG']
        elif is_admin == False:
            bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
        else:
            bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
        bot.send_message(chat_id, bot_msg)


def cmd_add_group(update: Update, context: CallbackContext):
    '''Command /add_group message handler'''
    bot = context.bot
    args = context.args
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_id == CONST['OWNER_ID']:
        #lang = get_chat_config(chat_id, 'Language')
        if len(args) == 1:
            group_id = args[0]
            if(is_int(group_id)):
                group_id_int = int(group_id)
                if group_id_int not in allowed_groups:
                    save_allowed_group(group_id_int)
                    allowed_groups.append(group_id_int)
                    bot_msg = "Grupo autorizado para utilizarme."
                else:
                    bot_msg = "Ese grupo ya tenia permiso."
        else:
            bot_msg = "Tienes que especificar el ID del grupo:\n/add_group -123456"
    else:
        bot_msg = "Just the owner of the Bot can use this command."
    bot.send_message(chat_id, bot_msg)


def cmd_enable(update: Update, context: CallbackContext):
    '''Command /enable message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        enable = get_chat_config(chat_id, 'Antispam')
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == True:
            if enable:
                bot_msg = TEXT[lang]['ALREADY_ENABLE']
            else:
                enable = True
                save_config_property(chat_id, 'Antispam', enable)
                bot_msg = TEXT[lang]['ENABLE']
        elif is_admin == False:
            bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
        else:
            bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_disable(update: Update, context: CallbackContext):
    '''Command /disable message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        user_id = update.message.from_user.id
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        enable = get_chat_config(chat_id, 'Antispam')
        is_admin = user_is_admin(bot, user_id, chat_id)
        if is_admin == True:
            if enable:
                enable = False
                save_config_property(chat_id, 'Antispam', enable)
                bot_msg = TEXT[lang]['DISABLE']
            else:
                bot_msg = TEXT[lang]['ALREADY_DISABLE']
        elif is_admin == False:
            bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
        else:
            bot_msg = TEXT[lang]['CAN_NOT_GET_ADMINS']
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_notify_all_chats(update: Update, context: CallbackContext):
    '''Command /notify_all_chats message handler'''
    global owner_notify
    bot = context.bot
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    user_id = update.message.from_user.id
    lang = get_chat_config(chat_id, 'Language')
    if chat_type == "private":
        if user_id == CONST['OWNER_ID']:
            if owner_notify == False:
                owner_notify = True
                bot.send_message(chat_id, TEXT[lang]['CMD_NOTIFY_ALL'])
            else:
                bot.send_message(chat_id, TEXT[lang]['CMD_NOTIFYING'])
        else:
            bot.send_message(chat_id, TEXT[lang]['CMD_JUST_ALLOW_OWNER'])
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['CMD_JUST_ALLOW_IN_PRIVATE'])


def cmd_notify_discard(update: Update, context: CallbackContext):
    '''Command /notify_discard message handler'''
    global owner_notify
    bot = context.bot
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    user_id = update.message.from_user.id
    lang = get_chat_config(chat_id, 'Language')
    if chat_type == "private":
        if user_id == CONST['OWNER_ID']:
            if owner_notify == True:
                owner_notify = False
                bot.send_message(chat_id, TEXT[lang]['CMD_NOTIFY_DISCARD'])
            else:
                bot.send_message(chat_id, TEXT[lang]['CMD_NOTIFY_CANT_DISCARD'])
        else:
            bot.send_message(chat_id, TEXT[lang]['CMD_JUST_ALLOW_OWNER'])
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, TEXT[lang]['CMD_JUST_ALLOW_IN_PRIVATE'])


def cmd_version(update: Update, context: CallbackContext):
    '''Command /version message handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    if chat_id in allowed_groups:
        chat_type = update.message.chat.type
        lang = get_chat_config(chat_id, 'Language')
        bot_msg = TEXT[lang]['VERSION'].format(CONST['VERSION'])
        if chat_type == "private":
            bot.send_message(chat_id, bot_msg)
        else:
            tlg_msg_to_selfdestruct(bot, update.message)
            tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)


def cmd_about(update: Update, context: CallbackContext):
    '''Command /about handler'''
    bot = context.bot
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    lang = get_chat_config(chat_id, 'Language')
    bot_msg = TEXT[lang]['ABOUT_MSG'].format(CONST['DEVELOPER'], CONST['REPOSITORY'], \
        CONST['DEV_PAYPAL'], CONST['DEV_BTC'])
    if chat_type == "private":
        bot.send_message(chat_id, bot_msg)
    else:
        tlg_msg_to_selfdestruct(bot, update.message)
        tlg_send_selfdestruct_msg(bot, chat_id, bot_msg)

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
        # Get sent message ID and calculate delete time
        msg_id = sent_msg.message_id
        destroy_time = int(time()) + int(time_delete_min*60)
        # Add sent message data to to-delete messages list
        sent_msg_data = OrderedDict([('Chat_id', None), ('Msg_id', None), ('delete_time', None)])
        sent_msg_data['Chat_id'] = chat_id
        sent_msg_data['Msg_id'] = msg_id
        sent_msg_data['delete_time'] = destroy_time
        to_delete_messages_list.append(sent_msg_data)
        debug_print("Sent message has been set to selfdestruct.\n  (Chat, Msg, When) - " \
            "({}, {}, {}).".format(chat_id, msg_id, (destroy_time-int(time()))/60))


def tlg_msg_to_selfdestruct_in(bot, message, time_delete_min):
    '''Add a telegram message to be auto-delete in specified time'''
    # Get sent message ID and calculate delete time
    chat_id = message.chat_id
    msg_id = message.message_id
    destroy_time = int(time()) + int(time_delete_min*60)
    # Add sent message data to to-delete messages list
    sent_msg_data = OrderedDict([('Chat_id', None), ('Msg_id', None), ('delete_time', None)])
    sent_msg_data['Chat_id'] = chat_id
    sent_msg_data['Msg_id'] = msg_id
    sent_msg_data['delete_time'] = destroy_time
    to_delete_messages_list.append(sent_msg_data)
    debug_print("Chat message has been set to selfdestruct.\n  (Chat, Msg, When) - " \
        "({}, {}, {}).".format(chat_id, msg_id, destroy_time))


def th_selfdestruct_messages(bot):
    '''Handle remove messages sent by the Bot with the timed self-delete function'''
    global to_delete_messages_list
    while not force_exit:
        # Thread sleep for each iteration
        sleep(0.01)
        # Check each Bot sent message
        i = 0
        while i < len(to_delete_messages_list):
            sent_msg = to_delete_messages_list[i]
            # Check for break iterating if script must exit
            if force_exit:
                return
            # Sleep each 100 iterations
            i = i + 1
            if (i != 0) and ((i % 1000) == 0):
                i = 0
                sleep(0.01)
            # If actual time is equal or more than the expected sent msg delete time
            if int(time()) >= sent_msg['delete_time']:
                # Try to delete that sent message if possible (still exists)
                debug_print("Time accomplished for delete message.\n  (Chat, Msg) - ({}, {}).". \
                    format(sent_msg['Chat_id'], sent_msg['Msg_id']))
                debug_print("Trying to remove it...")
                try:
                    if bot.delete_message(sent_msg['Chat_id'], sent_msg['Msg_id']):
                        to_delete_messages_list.remove(sent_msg)
                        debug_print("Message successfully removed.")
                except:
                    debug_print("Fail - Can't delete message.")
                    to_delete_messages_list.remove(sent_msg)

####################################################################################################

### Telegram Errors Callback ###

def tlg_error_callback(update, context):
    '''Telegram errors handler.'''
    try:
        raise context.error
    except Unauthorized:
        debug_print("TLG Error: Unauthorized")
    except BadRequest:
        debug_print("TLG Error: Bad Request")
    except TimedOut:
        debug_print("TLG Error: Timeout (slow connection issue)")
    except NetworkError:
        debug_print("TLG Error: network problem")
    except TelegramError as e:
        debug_print("TLG Error: {}".format(str(e)))

####################################################################################################

### Main Function ###

def main():
    '''Main Function'''
    global updater
    # Check if Bot Token has been set or has default value
    if CONST["TOKEN"] == "XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX":
        debug_print("Error: Bot Token has not been set.")
        debug_print("Please add your Bot Token to constants.py file.")
        debug_print("Exit.\n")
        exit(0)
    # Initialize resources by populating files list and configs with chats found files
    debug_print("Launching Bot...")
    initialize_resources()
    # Set messages to be sent silently by default
    msgs_defaults = Defaults(disable_notification=True)
    # Create an event handler (updater) for a Bot with the given Token and get the dispatcher
    updater = Updater(CONST["TOKEN"], workers=12, defaults=msgs_defaults)
    dp = updater.dispatcher
    # Set Telegram errors handler
    dp.add_error_handler(tlg_error_callback)
    # Set to dispatcher all expected commands messages handler
    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CommandHandler("help", cmd_help))
    dp.add_handler(CommandHandler("commands", cmd_commands))
    dp.add_handler(CommandHandler("language", cmd_language, pass_args=True))
    dp.add_handler(CommandHandler("set_messages", cmd_set_messages, pass_args=True))
    dp.add_handler(CommandHandler("set_hours", cmd_set_hours, pass_args=True))
    dp.add_handler(CommandHandler("status", cmd_status))
    dp.add_handler(CommandHandler("admin", cmd_call_admins))
    dp.add_handler(CommandHandler("call_when_spam", cmd_call_when_spam, pass_args=True))
    dp.add_handler(CommandHandler("users_add_bots", cmd_users_add_bots, pass_args=True))
    dp.add_handler(CommandHandler("allow_user", cmd_allow_user, pass_args=True))
    dp.add_handler(CommandHandler("add_group", cmd_add_group, pass_args=True))
    dp.add_handler(CommandHandler("enable", cmd_enable))
    dp.add_handler(CommandHandler("disable", cmd_disable))
    dp.add_handler(CommandHandler("notify_all_chats", cmd_notify_all_chats))
    dp.add_handler(CommandHandler("notify_discard", cmd_notify_discard))
    dp.add_handler(CommandHandler("version", cmd_version))
    dp.add_handler(CommandHandler("about", cmd_about))
    # Set to dispatcher a not-command text messages handler
    dp.add_handler(MessageHandler(Filters.text, msg_nocmd, run_async=True))
    # Set to dispatcher a new member join the group and member left the group events handlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_user))
    # Launch the Bot ignoring pending messages and get all updates
    if CONST["WEBHOOK_HOST"] == "None":
        debug_print("Setup Bot for Polling.")
        updater.start_polling(
            drop_pending_updates=True,
            #allowed_updates=Update.ALL_TYPES
            allowed_updates=[
                Update.MESSAGE,
                Update.EDITED_MESSAGE,
                Update.MY_CHAT_MEMBER,
                Update.CHAT_MEMBER
            ]
        )
    else:
        debug_print("Setup Bot for Webhook.")
        updater.start_webhook(
            drop_pending_updates=True, listen="0.0.0.0", port=CONST["WEBHOOK_PORT"],
            url_path=CONST["TOKEN"], key=CONST["WEBHOOK_CERT_PRIV_KEY"], cert=CONST["WEBHOOK_CERT"],
            webhook_url="https://{}:{}/{}".format(CONST["WEBHOOK_HOST"], CONST["WEBHOOK_PORT"],
            CONST["TOKEN"]),
            #allowed_updates=Update.ALL_TYPES
            allowed_updates=[
                Update.MESSAGE,
                Update.EDITED_MESSAGE,
                Update.MY_CHAT_MEMBER,
                Update.CHAT_MEMBER
            ]
        )
    debug_print("Bot setup completed. Bot is now running.")
    # Launch delete mesages thread
    th_0 = Thread(target=th_selfdestruct_messages, args=(updater.bot,))
    th_0.name = "th_selfdestruct_messages"
    th_0.start()
    # Set main thread to idle
    updater.idle()
    print("Bot Threads end")
    if os_system() == "Windows":
        kill(getpid(), SIGTERM)
    else:
        kill(getpid(), SIGUSR1)
    sleep(1)
    debug_print("Exit 1")
    exit(1)


if __name__ == '__main__':
    main()

### End Of Code ###
