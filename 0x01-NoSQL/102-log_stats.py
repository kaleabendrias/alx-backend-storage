#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient
main = __import__("12-log_stats").main


if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client.logs
    collection = db.nginx
    main()
    print("IPs:")
    pipe = [
                {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
        ]
    popular = list(collection.aggregate(pipe))
    for ip in popular:
        print('\t{}: {}'.format(ip['_id'], ip['count']))
