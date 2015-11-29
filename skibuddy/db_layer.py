import pymongo
import skiserver.settings as conf
class db_layer:
    def __init__(self,coll_name):
        self.conn = pymongo.MongoClient(conf.mongo_uri)
        self.coll = (self.conn[conf.db_name])[coll_name]

    def get_data(self,cond):
        print cond
        cur = self.coll.find(cond)
        #print "hi9", cur
        l = []
        for i in cur:
            del i['_id']
            print i
            l.append(i)
        return l

    def get_count(self):
        cur = self.coll.find({},{"count":1})
        res= cur[0]['count']
        return res

    def set_count(self,record):
        print "Inside set_count "
        print record
        cur = self.coll.save({"_id":"event_id_check","count":record})

#expect records as list of records
    def set_data(self,records):
        self.coll.insert_many(records)



