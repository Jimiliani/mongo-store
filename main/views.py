from django.http import HttpResponse, JsonResponse

from models import items
from bson.objectid import ObjectId


def get_item(request, pk):
    if request.method == 'GET':
        item = items.find_one({"_id": ObjectId(pk)})
        return JsonResponse(item)
    else:
        return HttpResponse(status=405)


def get_multiple_items_or_create(request):
    if request.method == 'GET':
        items_ = items.find(request.GET)
        return JsonResponse(items_)
    elif request.method == 'POST':
        items.insert_one(request.POST.get('item'))
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)


def buy_item(request):
    if request.method == 'POST':
        item = items.find_one({"_id": request.POST.get('item')})
        if item:
            if item['count'] > 0:
                items.update_one({"_id": ObjectId(item['_id'])}, {"$set": {"count": item["count"] - 1}})
            else:
                return HttpResponse("Too few items", status=400)
        else:
            return HttpResponse(status=404)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
