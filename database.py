# import pymongo
# myArts = pymongo.MongoClient("mongodb+srv://user:user@cluster0.u3fdtma.mongodb.net/Master")
# mydb = myArts["ArtDB"]
# mycol= mydb["Art"]

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://user:user@cluster0.u3fdtma.mongodb.net/Master")
db = client["your_database_name"]