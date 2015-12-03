import pymongo
import json as simplejson
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
        cur=self.coll.remove({"user_id": userId,"event_id":eventId})

    def addEventName(self,result):
        res=[]
        for i in range(len(result)):
             cur = self.coll.find({"event_id":result[i]}, {"event_id":1,"title":1,"_id":0})
             for j in cur:
                 res.append(j)
        return res


    def getCommonEvents(self,userId,playerId):
        userEvents = self.coll.find({"user_id":userId},{"event_id":1,"_id":0})
        userEventList = []
        for i in userEvents:
            i = int(i['event_id'])
            userEventList.append(i)

        playerEvents = self.coll.find({"user_id":playerId},{"event_id":1,"_id":0})
        playerEventList = []
        for i in playerEvents:
            i = int(i['event_id'])
            playerEventList.append(i)

        result = list(set(userEventList).intersection(playerEventList))
        db = db_layer('ski_event')
        res=db.addEventName(result)

        playerDetail=[]
        for i in range(len(res)):
            cur = self.coll.find({"user_id":playerId,"event_id":res[i]['event_id'] },{"event_id":1,"distance":1,"location_trace":1,"_id":0})
            for j in cur:
                j[u'title'] = res[i]['title']
                playerDetail.append(j)
        return playerDetail

    def update(self,query,cond, choice = True):
        self.coll.update(query,{'$set':cond},choice)

    def getUserRecords(self):
        userList=[]
        userRecords = self.coll.find({},{"user_name":1,"user_location.latitude":1,"user_location.longitude":1,"_id":0})
        for i in userRecords:
            userList.append(i)
        return userList

    def update(self,query,cond):
        self.coll.update(query,{'$set':cond},True)










