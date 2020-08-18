import requests
import json
import time

def search_dict(partial, key):
    """
    A handy function that searches for a specific `key` in a partial dictionary/list

    """
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:    # if key found then return the value of the key
                yield v
            else:      # value of the key may be another dictionary, search again
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list): # if the partial is a list
        for i in partial:  # every list may contain dictionary, that's whay search dict again
            for o in search_dict(i, key):
                yield o


data = [{
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "JSON:API paints my bikeshed!",
      "body": "The shortest article. Ever.",
      "created": "2015-05-22T14:56:29.000Z",
      "updated": "2015-05-22T14:56:28.000Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "42", "type": "people"}
      }
    }
  }],
  "included": [
    {
      "type": "people",
      "id": "42",
      "attributes": {
        "name": "John",
        "age": 80,
        "gender": "male",
        "saqib": "aquaticmango654"
      }
    }
  ]
},
{
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "JSON:API paints my bikeshed!",
      "body": "The shortest article. Ever.",
      "created": "2015-05-22T14:56:29.000Z",
      "updated": "2015-05-22T14:56:28.000Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "42", "type": "people"}
      }
    }
  }],
  "included": [
    {
      "type": "people",
      "id": "42",
      "attributes": {
        "name": "John",
        "age": 80,
        "gender": "male",
        "saqib": "aquaticmango654"
      }
    }
  ]
},
{
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "JSON:API paints my bikeshed!",
      "body": "The shortest article. Ever.",
      "created": "2015-05-22T14:56:29.000Z",
      "updated": "2015-05-22T14:56:28.000Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "42", "type": "people"}
      }
    }
  }],
  "included": [
    {
      "type": "people",
      "id": "42",
      "attributes": {
        "name": "John",
        "age": 80,
        "gender": "male",
        "saqib": "aquaticmango654"
      }
    }
  ]
}]
import time
def info(datas):
    con = list(datas)
    while True:
        con.pop()
        for data in datas:
            yield data

        time.sleep(1)
        con.append(datas)
from pprint import pprint
#print(info(data['data'][0]['attributes']))
c=1
for v in info(data):

    pprint(v)
    print("="*50)
    if c==5:
        break
    c+=1
