from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
CHANNEL = int(os.getenv('CHANNEL'))
LOG_CHAT = int(os.getenv('LOG_CHAT'))
CHANNEL_LINK = os.getenv('CHANNEL_LINK')
DB_PATH = os.getenv('DB_PATH')
ADMIN_IDS = os.getenv('ADMIN_IDS').split(",")
CRYPTOBOT_INVOICE_URL = os.getenv('CRYPTOBOT_INVOICE_URL')
