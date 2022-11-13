from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId

from datetime import datetime

import sys

sys.path.insert(1, "/Users/jiaronghe/Desktop/DigitalXi/askAVet/flask-seed")
from config import DevelopmentConfig


class MongoDBTest(object):
    def __init__(self):
        self.cluster = MongoClient("mongodb://root:root@localhost:27017")

    def add_one(self):
        doc = {
            "username": "roytest",
            "password": "123456",
            "reg_date": datetime.now(),
            "company": {
                "name": "company A",
                "tel": "1231231234",
            },
        }
        db = self.cluster["flask_seed"]
        collection = db["users"]
        result = collection.insert_one(doc)
        print(result.inserted_id)

    def add_many(self):
        doc1 = {
            "username": "roytest2",
            "password": "123456",
            "reg_date": datetime.now(),
            "company": {
                "name": "company A",
                "tel": "1231231234",
            },
        }
        doc2 = {
            "username": "roytest3",
            "password": "123456",
            "reg_date": datetime.now(),
            "company": {
                "name": "company A",
                "tel": "1231231234",
            },
        }
        doc_list = [doc1, doc2]
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.insert_many(doc_list)
        print(result.inserted_ids)

    def search_one(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        user_obj = collection.find_one()
        print(user_obj)
        print(user_obj["company"]["name"])

    def search_user_by_pk(self, pk):
        obj_id = ObjectId(pk)
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        user_obj = collection.find_one({"_id": obj_id})
        print(user_obj)

    def search_many(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        stu_list = collection.find({"username": "roytest2"}, {"_id": 1})
        for item in stu_list:
            print(item)

    def paginate(self, page=1, page_size=2):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("grades")
        grade_list = (
            collection.find()
            .skip((page - 1) * page_size)
            .limit(page_size)
            .sort("grade.score", DESCENDING)
        )
        for item in grade_list:
            print(item)

    def count(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("grades")
        result = collection.count_documents({})
        print(result)

    def aggregate(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("grades")
        grade_list = collection.aggregate(
            [
                # where
                {"$match": {"grade.score": {"$gte": 60}}},
                # group by
                {"$group": {"_id": "$stu_no", "total": {"$sum": 1}}},
                # having
                {"$match": {"total": {"$eq": 3}}},
            ]
        )
        for item in grade_list:
            print(item)

    def update_one(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.update_one({}, {"$set": {"password": "123321"}})
        print(result)

    def replace_one(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.replace_one(
            {},
            {
                "username": "replaced",
                "password": "123321",
            },
        )
        print(result)

    def update_many(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.update_many({}, {"$set": {"password": "111111"}})
        print(result)

    def find_one_and_update(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.find_one_and_update({}, {"$set": {"sex": "female"}})
        print(result)

    def delete_one(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.delete_one({})
        print(result.deleted_count)

    def find_one_and_delete(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.find_one_and_delete({})
        print(result)

    def delete_many(self):
        db = self.cluster.get_database("flask_seed")
        collection = db.get_collection("users")
        result = collection.delete_many({})
        print(result.deleted_count)


def main():
    obj = MongoDBTest()
    # obj.add_one()
    # obj.add_many()
    # obj.search_one()
    # obj.search_user_by_pk("636c5eda1825fb20cca428c6")
    # obj.search_many()
    # obj.paginate(page=2, page_size=2)
    # obj.count()
    # obj.aggregate()
    # obj.update_one()
    # obj.replace_one()
    # obj.update_many()
    # obj.find_one_and_update()
    # obj.delete_one()
    obj.find_one_and_delete()


if __name__ == "__main__":
    main()
