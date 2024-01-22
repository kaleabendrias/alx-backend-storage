#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""


from pymongo import MongoClient


def main():
    """prints some info"""
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.logs
    collection = db.nginx
    print(collection.count_documents({}), "logs")
    print("Methods:")
    print("\tmethod GET:", collection.count_documents({"method": "GET"}))
    print("\tmethod POST:", collection.count_documents({"method": "POST"}))
    print("\tmethod PUT:", collection.count_documents({"method": "PUT"}))
    print("\tmethod PATCH:", collection.count_documents({"method": "PATCH"}))
    print("\tmethod DELETE:", collection.count_documents({"method": "DELETE"}))
    print(collection.count_documents
          ({"method": "GET", "path": "/status"}), "status check")


if __name__ == "__main__":
    main()
