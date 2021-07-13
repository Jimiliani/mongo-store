from bson import json_util
from django.http import HttpResponse

from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt

from .models import items


def get_item(request, pk):
    if request.method == 'GET':
        item = items.find_one({"_id": ObjectId(pk)})
        return HttpResponse(json_util.dumps(item), headers={'Content-Type': 'application/json'})
    else:
        return HttpResponse(status=405)


@csrf_exempt
def get_multiple_items_or_create(request):
    if request.method == 'GET':
        items_ = []
        for item in items.find(request.GET):
            items_.append(item)
        print(items_)
        print(json_util.dumps(items_))
        return HttpResponse(json_util.dumps(items_), headers={'Content-Type': 'application/json'})
    elif request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        count = request.POST.get('count')
        additional = request.POST.get('additional')
        item = items.insert_one({'name': name, 'price': price, 'count': count, 'additional': additional})
        return HttpResponse(item.inserted_id, status=201)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def buy_item(request, pk):
    if request.method == 'POST':
        item = items.find_one({"_id": ObjectId(pk)})
        print(item)
        if item:
            if int(item['count']) > 0:
                items.update_one({"_id": ObjectId(item['_id'])}, {"$set": {"count": int(item["count"]) - 1}})
                return HttpResponse(status=200)
            else:
                return HttpResponse("Too few items", status=400)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)
