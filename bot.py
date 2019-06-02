import random
from telegram.ext import Updater, MessageHandler, Filters, run_async
from env import bot_token
import json

def get_name(telegramUser):
    first_name = telegramUser.first_name or "PersonWithNoName"  # edge case of empty name - occurs for some bugs.
    if telegramUser.last_name:
        fullname = "{} {}".format(first_name, telegramUser.last_name)
    else:
        fullname = first_name
    return fullname

@run_async
def new_member(bot, update):
    with open('messages.json') as json_file:
        welcome_messages = json.load(json_file)['welcome']

    chat = update.effective_chat
    group_name = chat['title']
    new_members = update.effective_message.new_chat_members

    for new_mem in new_members:
        fullname = get_name(new_mem)

        if new_mem.id != bot.id:
            update.effective_message.reply_text(random.choice(welcome_messages).
                                                format(name=fullname, group_name=group_name))


@run_async
def leaving_member(bot,update):
    with open('messages.json') as json_file:
        goodbye_messages = json.load(json_file)['goodbye']
    
    chat = update.effective_chat
    group_name = chat['title']
    leaving_member = update.effective_message.left_chat_member

    fullname = get_name(leaving_member)

    if leaving_member != bot.id:
        update.effective_message.reply_text(random.choice(goodbye_messages).
                                                format(name=fullname, group_name=group_name))


if __name__ == '__main__':
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, leaving_member))
    updater.start_polling()
    updater.idle()

