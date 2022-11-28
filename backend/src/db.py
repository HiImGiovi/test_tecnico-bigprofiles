from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


conn = MongoClient(os.getenv("MONGODB_URL"))

local_db = conn.local

enrich_inputs_collection = local_db.enrich_inputs