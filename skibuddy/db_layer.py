import pymongo
import skiserver.settings as conf
class db_layer:
    def __init__(self,coll_name):
        self.conn = pymongo.MongoClient(conf.mongo_uri)
        self.coll = (self.conn[conf.db_name])[coll_name]

    def get_data(self,cond):
        print cond
        cur = self.coll.find(cond)
        l = []
        for i in cur:
            del i['_id']
            print i
            l.append(i)
        return l

#expect records as list of records
    def set_data(self,records):
        self.coll.insert_many(records)


