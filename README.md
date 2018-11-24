# TLG_AntiJoin2SpamBot

Telegram Bot that figth against the spammer users that join groups to spam their annoying and unwanted info.

Important Notice: The Bot account @The_Anti_Join2Spam_Bot has been closed and has stopped working. The Bot was being hosted by the developer and was offered free for use in any telegram group, however, the Bot has reach more than 600 groups and that starts to affect the Bot functionality (response time) due to low resources of the host machine (and I can't afford to spend more money for a better host). Remember that it is an open-source Bot and anyone can get the source code, host it and create a new telegram account for it.

-------------------------------------------------------------------------------------------------------------------------

## How to install, setup and execute the Bot:

1 - Install Python3 and their tools:
```
sudo -i
apt-get install python3
apt-get install python3-pip
pip3 install --upgrade pip
pip3 install --upgrade setuptools
```

2 - Install python-telegram-bot library using python3-pip tool:
```
pip3 install python-telegram-bot --upgrade
exit
```

3 - Download Bot repository and go inside sources directory:
```git clone https://github.com/J-Rios/TLG_AntiJoin2SpamBot
cd TLG_AntiJoin2SpamBot/sources
```

4 - Change the TOKEN line of Constants file to set the TOKEN of your Bot account (from @BotFather):
```
nano Constants.py
[Change this line -> 'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
```

5 - Run the Bot:
```
A - Run it at normal:
	python3 Anti_Join2Spam_Bot.py

B - Run it in background and unassociated to actual tty (preserve execution when terminal/console is closed):
	nohup python3 Anti_Join2Spam_Bot.py &
```

6 - Enjoy of a Telegram free of "join2spam" users ;)

-------------------------------------------------------------------------------------------------------------------------

## Bot help:

- To get working the Anti-spam, you must add me to a group ang give me Administration privileges to let me delete spam messages.

- Once I got Admin privileges, I'll watch for all new users that join the group and don't let them to publish messages that contains URLs until they have been in the group long as an specific time, and they have written an enough number of messages.

- The time that new users need to wait and the number of messages that they need to write before they can publish messages with URLs are, by default, 24 hours and 10 messages, but this values can be modified and configured by using the commands /set_messages and /set_hours.

- To preserve a clean group, I auto-remove messages related to me, after 5 minutes (except Spam detection messages and Admins calls).

- Configuration and enable/disable commands just can be used by the group Administrators.

- You can change the language that I speak, using the command /language.

- Check /commands for get a list of all avaliable commands, and a short description of all of them.

-------------------------------------------------------------------------------------------------------------------------

## List of implemented commands:

/start - Show the initial information about the bot.

/help - Show the help information.

/commands - Show the actual message. Information about all the available commands and their description.

/language - Allow to change the language of the bot messages. Actual available languages: en (english) - es (spanish).

/status - Check actual configured values of all properties.

/set_messages - Set how many published messages are need for new users to be allowed to publish URLs in messages.

/set_hours - Set how many hours for new users are need to wait to get allowed to publish URLs in messages.

/call_admins - Call to all Admins of the group.

/call_when_spam - Enable/disable Admins notify when a spam message is detected.

/users_add_bots - Enable/disable allow users to invite and add Bots to the group.

/allow_user - Allow an user to publish URLs in messages.

/enable - Enable the Anti-Spam.

/disable - Disable the Anti-Spam.

/version - Show the version of the Bot.

/about - Show about info.

-------------------------------------------------------------------------------------------------------------------------

## Notes

- This Bot uses [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.

- This Bot was developed using Python 3.6.
