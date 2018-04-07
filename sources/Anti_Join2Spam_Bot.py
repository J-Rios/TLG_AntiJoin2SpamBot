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
    07/04/2018
Version:
    1.0.0
'''

####################################################################################################

### Imported modules ###
import re
import sys
import signal
import TSjson
from datetime import datetime, timedelta
from time import strptime, mktime
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
fjson_usr = TSjson.TSjson(CONST['F_USR'])
fjson_msg = TSjson.TSjson(CONST['F_MSG'])

####################################################################################################

### Termination signals handler for program process ###
def signal_handler(signal, frame):
    '''Termination signals (SIGINT, SIGTERM) handler for program process'''
    print('Closing the program, safe way...')
    # Acquire messages and users files mutex to ensure not read/write operation on it
    fjson_msg.lock.acquire()
    fjson_usr.lock.acquire()
    # Close the program
    sys.exit(0)


### Signals attachment ###
signal.signal(signal.SIGTERM, signal_handler) # SIGTERM (kill pid) to signal_handler
signal.signal(signal.SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler

####################################################################################################

### Specific json files read/write reputation functions ###

def register_new_user(user_id, user_name, join_date):
    '''Add new member to the users file'''
    user_data = OrderedDict( \
    [ \
        ('User_id', user_id), \
        ('User_name', user_name), \
        ('Join_date', join_date), \
        ('Num_messages', 0) \
    ])
    fjson_usr.write_content(user_data)


def add_new_message(chat_id, msg_id, user_id, user_name, text, msg_date):
    '''Add new message to the messages file'''
    msg_data = OrderedDict( \
    [ \
        ('Chat_id', chat_id), \
        ('Msg_id', msg_id), \
        ('User_id', user_id), \
        ('User_name', user_name), \
        ('Text', text), \
        ('Date', msg_date) \
    ])
    fjson_msg.write_content(msg_data)


def get_user(user_id):
    '''Get user data by member ID'''
    users_data = fjson_usr.read_content()
    for usr in users_data:
        if user_id == usr['User_id']:
            return usr
    return None


def get_message(chat_id, msg_id):
    '''Get message data of a chat by ID'''
    messages_data = fjson_msg.read_content()
    for msg in messages_data:
        if chat_id == msg['Chat_id']:
            if msg_id == msg['Msg_id']:
                return msg    
    return None


def user_in_json(user_id):
    '''Check if a user is in the file by his ID'''
    users_data = fjson_usr.read_content()
    for usr in users_data:
        if user_id == usr['User_id']:
            return True
    return False


def update_user(new_user_data):
    '''Update an existing user from the JSON file. If the user does not exists, add to it'''
    user_id = new_user_data['User_id']
    if user_in_json(user_id):
        fjson_usr.update(new_user_data, 'User_id')
    else:
        fjson_usr.write_content(new_user_data)


def user_is_admin(bot, user_id, chat_id):
    '''Check if the specified user is an Administrator of a group given by IDs'''
    group_admins = bot.get_chat_administrators(chat_id)
    for admin in group_admins:
        if user_id == admin.user.id:
            return True
    return False


def get_admins_usernames_in_string(bot, chat_id):
    '''Get all the group Administrators usernames/alias in a single line string separed by \' \''''
    admins = ""
    group_admins = bot.get_chat_administrators(chat_id)
    for admin in group_admins:
        if admins == "":
            admins = admin.user.username
        else:
            admins = "{} {}".format(admins, admin.user.username)
    return admins

####################################################################################################

### Received Telegram not-command messages handlers ###

def new_user(bot, update):
    '''New member join the group event handler'''
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    join_date = (update.message.date).now().strftime("%Y-%m-%d %H:%M:%S")
    register_new_user(user_id, user_name, join_date)


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
        if not user_in_json(user_id):
            # Register user and set "Num_messages" and "Join_date" to allow publish URLs
            register_new_user(user_id, user_name, msg_date)
            user_data = get_user(user_id)
            user_data['Num_messages'] = num_messages_for_allow_urls
            user_data['Join_date'] = datetime(1971, 1, 1).strftime("%Y-%m-%d %H:%M:%S")
            update_user(user_data)
            num_published_messages = num_messages_for_allow_urls + 1
        else:
            user_data = get_user(user_id)
            user_data['Num_messages'] = user_data['Num_messages'] + 1
            update_user(user_data)
            num_published_messages = user_data['Num_messages']
        # If the Bot Anti-Spam is enabled
        if enable:
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
                        bot_message_0 = TEXT[lang]['MSG_SPAM_DETECTED_0'].format(user_name)
                        bot_message_1 = TEXT[lang]['MSG_SPAM_DETECTED_1'].format( \
                            time_for_allow_urls_h, num_messages_for_allow_urls)
                        bot_message = "{}{}".format(bot_message_0, bot_message_1)
                        if call_admins_when_spam_detected:
                            admins = get_admins_usernames_in_string(bot, chat_id)
                            if admins:
                                bot_message = "{}{}".format(bot_message, \
                                    TEXT[lang]['CALLING_ADMINS'], admins)
                        bot.send_message(chat_id, bot_message)
        # Truncate the message text to 500 characters
        if len(text) > 500:
            text = text[0:500]
            text = "{}...".format(text)
        # Add the message to messages file
        add_new_message(chat_id, msg_id, user_id, user_name, text, msg_date)
    
####################################################################################################

### Received Telegram command messages handlers ###

def cmd_start(bot, update):
    '''Command /start message handler'''
    bot.send_message(update.message.chat_id, TEXT[lang]['START'])


def cmd_help(bot, update):
    '''Command /help message handler'''
    bot_msg = TEXT[lang]['HELP'].format(CONST['INIT_MIN_MSG_ALLOW_URLS'], \
        CONST['INIT_TIME_ALLOW_URLS'])
    bot.send_message(update.message.chat_id, bot_msg)


def cmd_commands(bot, update):
    '''Command /commands message handler'''
    bot.send_message(update.message.chat_id, TEXT[lang]['COMMANDS'])


def cmd_language(bot, update, args):
    '''Command /language message handler'''
    global lang
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_is_admin(bot, user_id, chat_id):
        if len(args) == 1:
            lang_provided = args[0]
            if lang_provided == 'en' or lang_provided == 'es':
                lang_provided = lang_provided.upper()
                if lang_provided != lang:
                    lang = lang_provided
                    bot_msg = TEXT[lang]['LANG_CHANGE']
                else:
                    bot_msg = TEXT[lang]['LANG_SAME']
            else:
                bot_msg = TEXT[lang]['LANG_BAD_LANG']
        else:
            bot_msg = TEXT[lang]['LANG_NOT_ARG']
    else:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    bot.send_message(chat_id, bot_msg)


def cmd_set_messages(bot, update, args):
    '''Command /set_messages message handler'''
    global num_messages_for_allow_urls
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_is_admin(bot, user_id, chat_id):
        if len(args) == 1:
            num_msgs_provided = args[0]
            if num_msgs_provided.isdigit():
                num_msgs_provided = int(num_msgs_provided)
                if num_msgs_provided >= 0:
                    num_messages_for_allow_urls = num_msgs_provided
                    bot_msg = TEXT[lang]['SET_MSG_CHANGED'].format(num_messages_for_allow_urls)
                else:
                    bot_msg = TEXT[lang]['SET_MSG_NEGATIVE']
            else:
                bot_msg = TEXT[lang]['SET_MSG_BAD_ARG']
        else:
            bot_msg = TEXT[lang]['SET_MSG_NOT_ARG']
    else:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    bot.send_message(chat_id, bot_msg)


def cmd_set_hours(bot, update, args):
    '''Command /set_hours message handler'''
    global time_for_allow_urls_h
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_is_admin(bot, user_id, chat_id):
        if len(args) == 1:
            hours_provided = args[0]
            if hours_provided.isdigit():
                hours_provided = int(hours_provided)
                if hours_provided >= 0:
                    time_for_allow_urls_h = hours_provided
                    bot_msg = TEXT[lang]['SET_HOURS_CHANGED'].format(time_for_allow_urls_h)
                else:
                    bot_msg = TEXT[lang]['SET_HOURS_NEGATIVE_HOUR']
            else:
                bot_msg = TEXT[lang]['SET_HOURS_BAD_ARG']
        else:
            bot_msg = TEXT[lang]['SET_HOURS_NOT_ARG']
    else:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    bot.send_message(chat_id, bot_msg)


def cmd_status(bot, update):
    '''Command /status message handler'''
    chat_id = update.message.chat_id
    bot_msg = TEXT[lang]['STATUS'].format(num_messages_for_allow_urls, time_for_allow_urls_h, \
        call_admins_when_spam_detected, enable)
    bot.send_message(update.message.chat_id, bot_msg)


def cmd_call_admins(bot, update):
    '''Command /call_admins message handler'''
    chat_id = update.message.chat_id
    admins = get_admins_usernames_in_string(bot, chat_id)
    bot_message = TEXT[lang]['CALLING_ADMINS']
    bot_message = "{}{}".format(bot_message, admins)


def cmd_call_when_spam(bot, update, args):
    '''Command /cmd_call_when_spam message handler'''
    global call_admins_when_spam_detected
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_is_admin(bot, user_id, chat_id):
        if len(args) == 1:
            value_provided = args[0]
            if value_provided == 'enable' or value_provided == 'disable':
                if value_provided != call_admins_when_spam_detected:
                    if value_provided == 'enable':
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_ENABLE']
                    else:
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_DISABLE']
                else:
                    if value_provided == 'enable':
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_ALREADY_ENABLE']
                    else:
                        bot_msg = TEXT[lang]['CALL_WHEN_SPAM_ALREADY_DISABLE']
            else:
                bot_msg = TEXT[lang]['CALL_WHEN_SPAM_NOT_ARG']
        else:
            bot_msg = TEXT[lang]['CALL_WHEN_SPAM_NOT_ARG']
    else:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    bot.send_message(chat_id, bot_msg)


def cmd_enable(bot, update):
    '''Command /disable message handler'''
    global enable
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_is_admin(bot, user_id, chat_id):
        if enable:
            bot_msg = TEXT[lang]['ALREADY_ENABLE']
        else:
            enable = True
            bot_msg = TEXT[lang]['ENABLE']
    else:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    bot.send_message(chat_id, bot_msg)


def cmd_disable(bot, update):
    '''Command /disable message handler'''
    global enable
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if user_is_admin(bot, user_id, chat_id):
        if enable:
            enable = False
            bot_msg = TEXT[lang]['DISABLE']
        else:
            bot_msg = TEXT[lang]['ALREADY_DISABLE']
    else:
        bot_msg = TEXT[lang]['CMD_NOT_ALLOW']
    bot.send_message(chat_id, bot_msg)


def cmd_version(bot, update):
    '''Command /version message handler'''
    bot_msg = TEXT[lang]['VERSION'].format(CONST['VERSION'])
    bot.send_message(update.message.chat_id, bot_msg)


def cmd_about(bot, update):
    '''Command /cmd_about handler'''
    bot_msg = TEXT[lang]['ABOUT_MSG'].format(CONST['DEVELOPER'], CONST['REPOSITORY'])
    bot.send_message(update.message.chat_id, bot_msg)

####################################################################################################

### Main Function ###

def main():
    '''Main Function'''
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
    # Stop the execution of actual main thread and wait for async Bot messages reception handlers
    updater.idle()


if __name__ == '__main__':
    main()

### End Of Code ###
