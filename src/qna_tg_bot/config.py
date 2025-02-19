import os
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
BASE_DIR = os.path.join('src/', 'qna_tg_bot/')

ENV_PATH = os.path.join(ROOT_DIR, '.env')
load_dotenv(ENV_PATH)

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
