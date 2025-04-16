from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
DB_URI = os.getenv("DB_URI")
client = MongoClient(DB_URI)
db = client['LLM']
