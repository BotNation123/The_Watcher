from pymongo import MongoClient
from datetime import datetime, timedelta
from pymongo.server_api import ServerApi


url = (
    "mongodb+srv://test1:123@cluster0.gpskocw.mongodb.net/?retryWrites=true&w=majority"
)


client = MongoClient(
    url,
    server_api=ServerApi("1"),
    connectTimeoutMS=30000,
    socketTimeoutMS=None,
    connect=False,
    maxPoolsize=1,
)

db = client["the_watcher"]
collection = db["links"]


def test(arg, author):
    try:
        nuevo_arg = {
            "url": arg,
            "owner": author,
            "date": datetime.utcnow() + timedelta(hours=3),
        }
        collection.insert_one(nuevo_arg)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_links():
    try:
        links = []
        result = collection.find()
        for document in result:
            for key in document:
                if key == "url":
                    links.append(document[key])
        return links
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def get_all_links():
    try:
        links = []
        result = collection.find({})
        for document in result:
            for key in document:
                if key == "url":
                    links.append(document[key])
        return links
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def delete_link(arg):
    try:
        collection.delete_one({"url": arg})
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def delete_all_link():
    try:
        collection.delete_many({})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
