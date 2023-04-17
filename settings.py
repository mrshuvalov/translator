import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_URL = os.getenv('GOOGLE_URL')
MONGO_DETAILS = os.getenv('MONGO_DETAILS')