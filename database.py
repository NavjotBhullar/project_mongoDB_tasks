from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["sales_db"]

orders_collection = db["orders"]