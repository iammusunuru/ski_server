from django.shortcuts import render
from django.http import HttpResponse
import db_layer
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

# Create your views here.

# always return JSON objects in the format
# {data:[], status: success/failed}

def home(request):
    return HttpResponse("it worked")

#When the user logs in, we check if it already exists or not. If not, we add it to our db
'''
{
"data":  [ {"user_id":"harsham"}   ]
}
'''

@csrf_exempt
def check_user(request):
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    print data
    db = db_layer.db_layer('user')
    l = db.get_data({'user_id':data['data'][0]['user_id']})
    print l
    if not l:
        db.set_data(data['data'])
        return HttpResponse(json.dumps({'data':" User created ",'status':"success"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'data':" Already exists ",'status':"success"}), content_type="application/json")




#function to autoincrement the event_id
def autoIncrement():
    cnt=0;
    db = db_layer.db_layer('count')
    l = db.get_count()
    cnt=l+1;
    db.set_count(cnt)
    return cnt


#******check time on android side******
# format 2012-05-29T19:30:03.283Z
#if many items are there plese send them as a list of {}
#Created a new event here

'''
input format "data":  [ {"event_creator":"harsham","title":"itsworking","start_time":"2015-11-29T10:51:47.911555Z",
"end_time":"2015-11-29T10:51:47.911555Z","description":"nothing","venue":"hell"}

output: {"status": "success", "data": "Event created Successfully"}
'''


@csrf_exempt
def create_event(request):
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    x =autoIncrement()
    data['data'][0]['event_id']= x
    data['data'][0]['start_time'] = datetime.datetime.strptime(data['data'][0]['start_time'],'%Y-%m-%dT%H:%M:%S.%fZ')
    data['data'][0]['end_time'] = datetime.datetime.strptime(data['data'][0]['end_time'],'%Y-%m-%dT%H:%M:%S.%fZ')
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    db = db_layer.db_layer('ski_event')
    db.set_data(data['data'])
    db = db_layer.db_layer('event_members')
    db.set_data([{'user_id':data['data'][0]['user_id'],'event_id':str(data['data'][0]['event_id'])}])
    return HttpResponse(json.dumps({'data':"Event created Successfully",'status':"success"}), content_type="application/json")


#User is added to the join event table which wll have the user is and event id of the event joined

@csrf_exempt
def join_event(request):
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    db = db_layer.db_layer('event_members')
    db.set_data(data['data'])
    return HttpResponse(json.dumps({'data':"person joined the event",'status':"success"}), content_type="application/json")

#User is deleted from the join event table

@csrf_exempt
def unjoin_event(request):
    print "A"
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    print "B"
    db = db_layer.db_layer('event_members')
    db.unjoin_event(data['data'][0]['user_id'],data['data'][0]['event_id'])
    return HttpResponse(json.dumps({'data':"user-event pair deleted",'status':"success"}), content_type="application/json")

@csrf_exempt
def get_skirecords(request):
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    print data
    print "A"
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    print "B"
    db = db_layer.db_layer('ski_session')
    print "C"
    l=db.getCommonEvents(data['data'][0]['user_id'],data['data'][0]['player_id'])
    if not l:
        return HttpResponse(json.dumps({'data':"Matched event not found",'status':"failed"}))
    else:
     return HttpResponse(json.dumps({'data':"fetched ski records for the events",'status':"success"}), content_type="application/json")





#to get all  pass {} to get selected pass query
#gives info of a particular record
@csrf_exempt
def event_details(request):
    data = ((request.body))
    print data
    data = data.replace("'", "\"")
    data = json.loads(data)
    print data
    db = db_layer.db_layer('ski_event')
    l = db.get_data(data['data'])
    if not l:
        return HttpResponse(json.dumps({'data':"Event Notfound",'status':"failed"}))
    else:
        return HttpResponse(json.dumps({'data':l,'status':"success"}), content_type="application/json")



# need session name user id
@csrf_exempt
def start_session(request):
    data = request.body
    data = data.replace("'", "\"")
    data = json.loads(data)
    db = db_layer.db_layer('ski_session')
    data['data'][0]['start_time'] = datetime.datetime.utcnow()
    data['data'][0]['end_time'] = ''
    data['data'][0]['distance'] = ''
    data['data'][0]['location_trace'] = ''
    db.set_data(data['data'])
    return HttpResponse(json.dumps({'data':"session started",'status':"success"}), content_type="application/json")



'''
output format name, start_date, end_date, start_time, end_time, venue, eventId, title, join
input format {"event_id":"first_event","event_creator":"musunuru","title":"itsworking","start_time":"2015-11-29T10:51:47.911555Z",
               "end_time":"2015-11-29T10:51:47.911555Z","description":"nothing","venue":"hell"}
'''
@csrf_exempt
def get_events(request):
    data = request.body
    data = data.replace("'", "\"")
    data = json.loads(data)
    #get event in which user joined
    db = db_layer.db_layer('event_members')
    join_data = db.get_data(data['data'][0])
    event_list = []
    for i in join_data:
        event_list.append(i['event_id'])
    print event_list
    db  = db_layer.db_layer('ski_event')
    out = {'start_date':[], 'end_date':[], 'start_time':[], 'end_time':[], 'venue':[], 'eventId':[], 'title':[], 'join':[], 'description':[]}
    event_data = db.get_data({})
#tailoring the request
    for i in event_data:
        if str(i['event_id']) in event_list:
            out['join'].append(True)
        else:
            out['join'].append(False)
        out['start_time'].append("%d:%d" %(i['start_time'].hour, i['start_time'].minute))
        out['end_time'].append("%d:%d" %(i['end_time'].hour, i['end_time'].minute))
        out['start_date'].append("%d-%d-%d" %(i['start_time'].month, i['start_time'].day, i['start_time'].year))
        out['end_date'].append("%d-%d-%d" %(i['end_time'].month, i['end_time'].day, i['end_time'].year))
        out['title'].append(i['title'])
        out['venue'].append(i['venue'])
        out['description'].append(i['description'])
        out['eventId'].append(i['event_id'])
    return HttpResponse(json.dumps({'data':out,'status':"success"}), content_type="application/json")



'''
request {"user_id":"", "CurrentLocation": {"latitude":37.5771021,"longitude":-122.0445751,"mVersionCode":1}}
'''

@csrf_exempt
def update_currentloc(request):
    data = request.body
    data = data.replace("'", "\"")
    data = json.loads(data)
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    db = db_layer.db_layer('user')
    db.update({'user_id':data['data'][0]['user_id']},{'user_location':data['data'][0]['CurrentLocation']})
    return HttpResponse(json.dumps({'data':"location updated",'status':"success"}), content_type="application/json")




