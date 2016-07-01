import config
import telebot
from game import Game
from statistics import Statistics

game6v6_ = False

bot = telebot.TeleBot(config.token)

stats = Statistics()
g = Game(stats, bot, "tname")

def handle_6v6(msg):
    g.chat_id = msg.chat.id
    g.uinput = msg.text

@bot.message_handler(content_types=["text"])
def handle_msg(message):
    handle_6v6(message)
    #if message.text == 'start':
    g.start()
    if message.text == 'new':
        g.new()

if __name__ == '__main__':
    bot.polling(none_stop=True)
