import telebot

def send_message(apikey,chatid,data,search_term):
    # Load bot class
    bot = telebot.TeleBot(apikey)

    # For each company in data send a message
    for company in data:

        co_name = company['coname']
        co_joburl = company['jobspage']
        message = (f'<b>{co_name}</b> has a ' +
        f'<u><a href="{co_joburl}">New {search_term}</a></u> vacancy!')
        print('Sending Telegram message ' +
        f'for {co_name} with jobs page URL: {co_joburl}')
        bot.send_message(chatid,message,parse_mode='HTML')

# # When the start command is used the chatID will
# # print to the console
# @bot.message_handler(commands=['start'])
# def start(message):
#     cid = message.chat.id
#     print(cid)

# bot.polling()

