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
            l.append(i)
        return l

    #expect records as list of records
    def set_data(self,records):
        self.coll.insert_many(records)

    def get_count(self):
        cur = self.coll.find()
        if not cur.count():
            return 1
        res= cur[0]['count']
        return res

    def set_count(self,record):
        self.coll.update({"id":"event_id_check"},{'$set':{"count":record}},True)


    def unjoin_event(self,userId,eventId):
        print "C"
        cur=self.coll.remove({"user_id": userId,"event_id":eventId})


    def getCommonEvents(self,userId,playerId):
        userEvents = self.coll.find({"user_id":userId},{"event_id":1,"_id":0})
        userEventList = []
        for i in userEvents:
            i = int(i['event_id'])
            userEventList.append(i)
        print userEventList
        playerEvents = self.coll.find({"user_id":playerId},{"event_id":1,"_id":0})
        playerEventList = []
        for i in playerEvents:
            i = int(i['event_id'])
            playerEventList.append(i)
        print playerEventList
        res = list(set(userEventList).intersection(playerEventList))
        print res
        playerDetail=[]
        for i in range(len(res)):
            cur = self.coll.find({"user_id":playerId,"event_id":res[i]},{"event_id":1,"distance":1,"location_trace":1,"_id":0})
            for j in cur:
                 playerDetail.append(j)

        print playerDetail
        return playerDetail

    def update(self,query,cond):
        self.coll.update(query,{'$set':cond},True)










