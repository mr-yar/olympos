import logging
import os
from functools import partial

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler

from src.downloaders.youtube import download_youtube_video_best_quality
from src.utils import remake_folder

DOWNLOAD_VIDEO = 'Download video'
DOWNLOAD_ENTIRE_LIST = 'Download entire list'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TeleBot:
    def __init__(self):
        self.token = os.environ["API_TOKEN"]
        self.current_state = None
        self.user_id = None

    async def start_co(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.user_id = update.message.from_user.id
        text = update.message.text

        remake_folder(str(self.user_id))

        if text == DOWNLOAD_VIDEO:
            await update.message.reply_text('Enter link of that video : ')
            self.current_state = DOWNLOAD_VIDEO

    async def download_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.current_state != DOWNLOAD_VIDEO:
            return

        url = update.message.text
        video = download_youtube_video_best_quality(url, self.user_id)
        await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video, 'rb'))

        os.remove(video)
        self.current_state = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_keyboard_start = [[DOWNLOAD_ENTIRE_LIST], [DOWNLOAD_VIDEO]]

        markup_start = ReplyKeyboardMarkup(reply_keyboard_start, resize_keyboard=True, one_time_keyboard=True)

        await update.message.reply_text('Choose between options : ', reply_markup=markup_start)
        # return (START_CO)

    def init_bot(self):
        application = ApplicationBuilder().token(self.token).build()

        start_handler = CommandHandler('start', self.start)
        download_list_handler = MessageHandler(filters.Regex(f'^{DOWNLOAD_ENTIRE_LIST}$'), self.start_co)
        download_handler = MessageHandler(filters.Regex(f'^{DOWNLOAD_VIDEO}$'), self.start_co)
        download_video_handler = MessageHandler(None, partial(self.download_video))

        application.add_handler(start_handler)
        application.add_handler(download_list_handler)
        application.add_handler(download_handler)
        application.add_handler(download_video_handler)

        application.run_polling()
