# TLG_AntiJoin2SpamBot

Telegram Bot that figths against Spammers who joins groups to spam their annoying and unwanted info.

The Bot will watch for all new users that join a group and don't let them to publish messages containing links (URLs) until they have been in the group long as an specific time, and they have written an enough number of messages (configurable parameters).

## Donate

Do you like this Bot? Buy me a coffee :)

Paypal:
[https://www.paypal.me/josrios](https://www.paypal.me/josrios)

## How to install, setup and execute the Bot

Note: Use Python 3.6 or above to install and run the Bot, previous version are unsupported.

1. Install Python3 and their tools:

    ```bash
    sudo apt-get install python3
    sudo apt-get install python3-pip
    sudo python3 -m pip install --upgrade pip
    sudo python3 -m pip install --upgrade setuptools
    ```

2. Get and setup the project:

    ```bash
    git clone https://github.com/J-Rios/TLG_AntiJoin2SpamBot
    cd TLG_AntiJoin2SpamBot
    make setup
    ```

3. Specify Telegram Bot account Token (get it from @BotFather) in `src/constants.py` file:

    ```python
    'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    ```

## Usage

Launch the Bot:

```bash
make run
```

Check if the Bot is running:

```bash
make status
```

- Stop the Bot:

```bash
make stop
```

## Bot help

- To get working the Anti-spam, you must add me to a group and give me Administration privileges to let me delete spam messages.

- Once I got Admin privileges, I'll watch for all new users that join the group and don't let them to publish messages containing URLs until they have been in the group long as an specific time, and they have written an enough number of messages.

- The time that new users need to wait and the number of messages that they need to write before they can publish messages with URLs are, by default, 24 hours and 10 messages, but this values can be modified and configured by using the commands /set_messages and /set_hours.

- To preserve a clean group, I auto-remove messages related to me, after 5 minutes (except Spam detection messages and Admins calls).

- Configuration and enable/disable commands just can be used by the group Administrators.

- You can change the language that I speak, using the command /language.

- Check /commands for get a list of all avaliable commands, and a short description of all of them.

## List of implemented commands

/start - Show the initial information about the bot.

/help - Show the help information.

/commands - Show the actual message. Information about all the available commands and their description.

/language - Allow to change the language of the bot messages. Actual available languages: en (english) - es (spanish).

/status - Check actual configured values of all properties.

/set_messages - Set how many published messages are need for new users to be allowed to publish URLs in messages.

/set_hours - Set how many hours for new users are need to wait to get allowed to publish URLs in messages.

/admin - Call to all Admins of the group.

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

- Minimal Python version 3.6.
