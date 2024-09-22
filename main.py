from src.telegram_bot import TeleBot
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    bot = TeleBot()
    bot.init_bot()
