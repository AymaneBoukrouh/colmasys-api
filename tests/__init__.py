from dotenv import load_dotenv
import os

### environment variables
load_dotenv()
DB_USER = os.environ['TEST_DB_USER']
DB_PASS = os.environ['TEST_DB_PASS']
DB_HOST = os.environ['TEST_DB_HOST']
DB_NAME = os.environ['TEST_DB_NAME']
URI = f'mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
