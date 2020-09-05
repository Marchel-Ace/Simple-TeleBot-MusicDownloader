import spotdl
import sqlite3
import os
import json
from spotdl import Spotdl
from spotdl.metadata_search import MetadataSearch
from pprint import pprint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.bot import Bot
from database_handle import SqliteHandle
from urllib.parse import urlparse

spotify = Spotdl()
db_file = "./data.db"    

logger_bot = Bot(token='YOUR TOKEN')
Admin_Chat_Id = ''
msg = {}
msg['App'] = "Music Downloader Bot"

def url_validation(url):
    if 'youtu.be' in url:
        parser = urlparse(url)
        url = "https://youtube.com/watch?v="+parser.path
        return url

    if 'youtube' in url or 'spotify' in url or 'youtu.be' in url: return url
    else: False
    

def download_music(url):
    new_url = url_validation(url)
    if new_url:
        metadata = spotify.download_track(new_url)
        return metadata
    return False

def start(bot, update):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    chat_id = update.message.chat.id
    uname = user['first_name']
    text = f'''
            Hi {uname}!
Welcome to Music Downloader bot, just enter link/url from spotify or youtube to download
for example send back this link:
    https://www.youtube.com/watch?v=uODuvT8m2-o&list=RDuODuvT8m2-o&start_radio=1
    or
    https://open.spotify.com/track/2DGa7iaidT5s0qnINlwMjJ
            '''
    update.message.reply_text(text)
    msg['user'] = uname
    msg['chat_id'] = chat_id
    msg['status'] = 'Send Help Message'
    logger_bot.send_message(Admin_Chat_Id, json.dumps(msg, indent=4))

def echo(bot, update):
    db = SqliteHandle(db_file)
    chat_id = update.message.chat.id
    message_user = update.message.text
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    user_id = update.message.from_user.id
    user_data = (user_id, username, chat_id, first_name)
    db.insert_users(user_data)
    filename = download_music(message_user)
    if filename:
        update.message.reply_text("Sending File")
        bot.sendAudio(chat_id, open(filename, 'rb'))
        os.remove(filename)
        log_data = (user_id, chat_id, message_user)
        db.insert_log(log_data)
        msg['user'] = username
        msg['chat_id'] = chat_id
        msg['status'] = 'Success Downloading ' + filename + ' with url ' + message_user
        logger_bot.send_message(Admin_Chat_Id, json.dumps(msg, indent=4))
    else:
        update.message.reply_text("Invalid URL")
        msg['user'] = username
        msg['chat_id'] = chat_id
        msg['status'] = 'Failed download from ' + message_user + ' Invalid URL'
        logger_bot.send_message(Admin_Chat_Id, json.dumps(msg, indent=4))

def main():
    updater = Updater("YOUR TOKEN", use_context=False)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))

    dp.add_handler(MessageHandler(Filters.regex('^(http|https)://'), echo))

    updater.start_polling()
    
    updater.idle()
    
if __name__ == "__main__":
    main()