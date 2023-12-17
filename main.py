from dotenv import load_dotenv
import os
import telebot
from openai import OpenAI
load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = telebot.TeleBot(TELEGRAM_API_KEY)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_cmd(text):
    words = text.split()
    if words:
        return words[0].lower()
    else:
        return None
    
def get_message_without_cmd(text):
    message = ' '.join(text.split()[1:]) 
    if message != '':
        return message
    else:
        return None

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")	
	
@bot.message_handler(func=lambda message: True)
def handling_command(message):
    cmd = get_cmd(message.text)
    user_message = get_message_without_cmd(message.text)

    if cmd == 'chat' or cmd == 'c':
        if not user_message :
            return bot.reply_to(message, "Please Provide A Message!")   
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="gpt-3.5-turbo",
        )
        bot.reply_to(message, chat_completion.choices[0].message.content)
		
bot.infinity_polling()