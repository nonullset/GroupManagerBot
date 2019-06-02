import random
from telegram.ext import Updater, MessageHandler, Filters, run_async
from env import bot_token


@run_async
def new_member(bot, update):
    welcome_messages = [
        'All rise for {name}, for they have joined {group_name}.',
        'Oh shit {name} just waltzed in here. Shit\'s about to go down.',
        'Welcome to our group {name}. Leaving is not an option.',
        'My mum said I need to be nicer to people. So I made a bot to greet you {name}.',
        'Welcome to AmErIcA, {name}'
    ]
    chat = update.effective_chat
    group_name = chat['title']
    new_members = update.effective_message.new_chat_members

    for new_mem in new_members:
        first_name = new_mem.first_name or "PersonWithNoName"  # edge case of empty name - occurs for some bugs.

        if new_mem.last_name:
            fullname = "{} {}".format(first_name, new_mem.last_name)
        else:
            fullname = first_name

        if new_mem.id != bot.id:
            update.effective_message.reply_text(random.choice(welcome_messages).
                                                format(name=fullname, group_name=group_name))


if __name__ == '__main__':
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    updater.start_polling()
    updater.idle()

