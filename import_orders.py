from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017")

db = client["sales_db"]
orders_collection = db["orders"]

file_path = "orders_10k.jsonl"

with open(file_path, "r") as file:
    data = []
    for line in file:
        data.append(json.loads(line))

orders_collection.insert_many(data)

print("Data inserted successfully")