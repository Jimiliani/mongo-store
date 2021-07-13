import json

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


def get_filtration_dict(filtration):
    if filtration == 'count':
        return 'count', -1
    elif filtration == 'sales':
        return 'additional.sales', -1
    return 'name', 1


@csrf_exempt
def get_multiple_items_or_create(request):
    if request.method == 'GET':
        data = request.GET.copy()
        filtration = data.pop('filtration', None)
        if isinstance(filtration, list):
            filtration = filtration[0]

        items_ = []
        for item in items.find(data).sort(*get_filtration_dict(filtration)):
            items_.append(item)

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
        if item:
            if int(item['count']) > 0:
                new_count = int(item.get("count", 0)) - 1
                try:
                    new_additional = item.get("additional", {})
                    new_additional['sales'] = int(new_additional.get('sales', 0)) + 1
                except (AttributeError, json.decoder.JSONDecodeError) as e:
                    new_additional = {}
                    new_additional['sales'] = int(new_additional.get('sales', 0)) + 1

                items.update_one(
                    {
                        "_id": ObjectId(item['_id'])
                    },
                    {
                        "$set":
                            {
                                "count": new_count,
                                "additional": new_additional
                            }
                    }
                )
                return HttpResponse(status=200)
            else:
                return HttpResponse("Too few items", status=400)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)
