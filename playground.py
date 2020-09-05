from telegram.bot import Bot
import json

logger_bot = Bot(token='1386047134:AAFuvSO0I_wm6yuIIWqRp7dR_5Y4tTEQ8DY')
msg = {}
msg['user'] = 'hi'
msg['chat'] = 'ho'

logger_bot.sendMessage('675876469', json.dumps(msg, indent=4))