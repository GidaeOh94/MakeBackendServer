
from flask import Flask, request
from requests import get
import json
from collections import OrderedDict

config = {
    "DEBUG": True,          
    "PORT":5000,
    "THREADED":True
}

SORT_GROUP = [
    "id",
    "reads",
    "likes",
    "popularity"
]

DIRECTION_GROUP = [
    "desc",
    "asc"
]

SOLUTION_URL = "https://api.hatchways.io/assessment/blog/posts?tag="

class LRUCache:
    
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.N = capacity
        
    def put(self, key,value)->None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if(len(self.cache)>self.N):
            self.cache.popitem(last=False)
            
    def get(self,key):
        if key not in self.cache:
            return 0;
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
        
    def containsKey(self, key):
        if key in self.cache.keys():
            return True
        else:
            return False
        
app = Flask(__name__)

app.config.from_mapping(config)

def get_Hatchways_API(tags:str =""):
    if "," not in tags:
        return get(SOLUTION_URL+f"{tags}").json()
    else:
        tags = tags.split(',')
        
        # TODO
        for i, tag in enumerate(tags):
            if i == 0:
                head = json.loads(json.dumps(get_Hatchways_API(tag)))
                _temp_items = head['posts']
                #print(_temp_items)
            else:
                _temp_items.extend(json.loads(json.dumps(get_Hatchways_API(tag)))['posts'])
                
        head['posts'] = list(removeduplicate(_temp_items))
        return head

def removeduplicate(item):
    seen_id = []
    for i in item:
        if i['id'] not in seen_id:          
            yield i
            seen_id.append(i['id'])
    seen_id = None

def test_request(tags:str=""):
    if "," not in tags:
        if len(get(SOLUTION_URL+f"{tags}").json()['posts']) >0:
            return True
        else :
            return False
    else:
        tags = tags.split(',')
        _bool_tag_list = []
        for tag in tags:
            _bool_tag_list.append(test_request(tag))
            
        if(len(_bool_tag_list) == sum(_bool_tag_list)):
            return True
        else:
            return False
    

def sort_json_array(json_object, key_name, ascending = False):
    #print(json_object['posts'])
    json_object['posts'] = sorted(json_object['posts'], key=lambda x : x[key_name], reverse=not(ascending))
    return json_object

# fetch data from the below API:
# Route: https://api.hatchways.io/assessment/blog/posts?tag=tech
# Method: Get
# Field: tag

tempStored = LRUCache(100)
# Request Function
# Route 1: ping
@app.route('/api/ping')
def CheckPing():
    return {"success":True}

# Route 2: Result
@app.route('/api/posts')
def GetPostResult():
    tags = str(request.args.get('tags', type=str))
    sortBy = str(request.args.get('sortBy', type=str, default='id'))
    direction = str(request.args.get('direction', type=str, default='asc'))
    
    if tags.strip() == '' or tags == None or test_request(tags) == False:
        return {"error": "Tags parameter is required"}, 400
    
    elif(
        (sortBy not in SORT_GROUP and (sortBy != None ) ) or
        (direction not in DIRECTION_GROUP and (direction != None ))
    ):
        return {
            "error": "sortBy parameter is invalid"}, 400
    else:
        direction = False if direction.lower()  == 'desc' else True
        if(tempStored.containsKey(tags)):
            json_array = tempStored.get(tags)
            sort_json_array(json_array, sortBy, direction)
            return tempStored.get(tags), 200
        else:
            downloadData = get_Hatchways_API(tags)
            json_array = sort_json_array(downloadData, sortBy, direction)
            tempStored.put(tags, json_array)
            return json_array, 200
if __name__ == ('__main__'):
    
    app.run()
    
