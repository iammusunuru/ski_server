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
@csrf_exempt
def create_event(request):
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    data['data'][0]['event_id']=autoIncrement()
    data['data'][0]['start_time'] = datetime.datetime.strptime(data['data'][0]['start_time'],'%Y-%m-%dT%H:%M:%S.%fZ')
    data['data'][0]['end_time'] = datetime.datetime.strptime(data['data'][0]['end_time'],'%Y-%m-%dT%H:%M:%S.%fZ')
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    db = db_layer.db_layer('ski_event')
    db.set_data(data['data'])
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

@csrf_exempt
def get_events(request):
    data = request.body
    data = data.replace("'", "\"")
    data = json.loads(data)
    #put current scheduled joined tags
    #for current and scheduled check ski seesion db
    #for joined check event user db




