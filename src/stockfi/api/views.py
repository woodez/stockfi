import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import pandas as pd
import pyarrow as pa

# Connect to our Redis instance
#redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
 #                                 port=settings.REDIS_PORT, db=0)
pool = redis.ConnectionPool(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=0)
cur = redis.Redis(connection_pool=pool)
context = pa.default_serialization_context()
all_keys = [key.decode("utf-8") for key in cur.keys()]



@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    print("testing")
    if request.method == 'GET':
        items = []
        count = 0
        for key in redis_instance.keys("*"):
               print("testing") 
               test = key.decode("utf-8")
 #           print(key.decode("utf-8"))
 #           print(test)
 #              items[test] = redis_instance.get(test)
 #              context = pa.default_serialization_context()
 #              result = redis_instance.get(test)
 #              dataframe = pd.DataFrame.from_dict(context.deserialize(result))
 #              items.append(dataframe)
               count += 1      
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)
    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)

@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
           result = cur.get(kwargs['key'])
           dataframe = pd.DataFrame.from_dict(context.deserialize(result))
           df_dict = dataframe.to_json()
           if df_dict:
#                response = {
#                    'key': kwargs['key'],
#                    'value': value,
#                    'msg': 'success'
#                }
              return Response(df_dict, status=200)
           else:
              response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
              }
              return Response(response, status=404)
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_instance.get(kwargs['key'])
            if value:
                redis_instance.set(kwargs['key'], new_value)
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['key']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_instance.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['key']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)