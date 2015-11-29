import pymongo
import skiserver.settings as conf
class db_layer:
    def __init__(self,coll_name):
        self.conn = pymongo.MongoClient(conf.mongo_uri)
        self.coll = (self.conn[conf.db_name])[coll_name]

    def get_data(self,cond):
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

    def get_count(self):
        cur = self.coll.find()
        res= cur[0]['count']
        return res

    def set_count(self,record):
        self.coll.update({"id":"event_id_check"},{'$set':{"count":record}},True)


    def unjoin_event(self,userId,eventId):
        print "C"
        cur=self.coll.remove({"user_id": userId,"event_id":eventId})






