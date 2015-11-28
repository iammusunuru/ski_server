from django.shortcuts import render
from django.http import HttpResponse
import db_layer
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

# always return JSON objects in the format
# {data:[], status: success/failed}

def home(request):
    return HttpResponse("it worked")

#
@csrf_exempt
def check_user(request):
    data = ((request.body))
    data = data.replace("'", "\"")
    data = json.loads(data)
    print data
    db = db_layer.db_layer('user')
    l = db.get_data({'user_id':data['data'][0]['user_id']})
    print "hi"
    print l
    if not l:
        db.set_data(data['data'])
        return HttpResponse(json.dumps({'data':" User created ",'status':"success"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'data':" Already exists ",'status':"success"}), content_type="application/json")


#******check time on android side******
#if many items are there plese send them as a list of {}

@csrf_exempt
def create_event(request):
    data = ((request.body))
    print data
    data = data.replace("'", "\"")
    data = json.loads(data)
    print data
    if data == '':
        return HttpResponse(json.dumps({'data':"no data received",'status':"failed"}), content_type="application/json")
    db = db_layer.db_layer('ski_event')
    db.set_data(data['data'])
    return HttpResponse(json.dumps({'data':"Event created Successfully",'status':"success"}), content_type="application/json")


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

