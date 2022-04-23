from settings import *
import json
from requests import get
from LRU import LRUCache

LRU_CACHE_STORAGE = LRUCache(100)
SOLUTION_URL = "https://api.hatchways.io/assessment/blog/posts?tag="

def get_Hatchways_API(tags:str =""):
    if "," not in tags:
        tags = tags.strip()
        download = get(SOLUTION_URL+f"{tags}").json()
        LRU_CACHE_STORAGE.put(tags, download)
        return download
    else:
        tags = tags.split(',')
        
        # TODO
        for i, tag in enumerate(tags):
            tag = tag.strip()
            if i == 0:
                
                if(LRU_CACHE_STORAGE.containsKey(tag)):
                    head = json.loads(json.dumps(LRU_CACHE_STORAGE.get(tag)))
                else:
                    head = json.loads(json.dumps(get_Hatchways_API(tag)))
                _temp_items = head['posts']
                #print(_temp_items)
            else:
                if(LRU_CACHE_STORAGE.containsKey(tag)):
                    tag_value = json.loads(json.dumps(LRU_CACHE_STORAGE.get(tag)))
                else:
                    tag_value = json.loads(json.dumps(get_Hatchways_API(tag)))
                _temp_items.extend(tag_value['posts'])
                
        head['posts'] = list(removeduplicate(_temp_items))
        tag_value = None
        print("Current Key in Cache")
        print(LRU_CACHE_STORAGE.keySet())
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
        tags = tags.strip()
        if len(get(SOLUTION_URL+f"{tags}").json()['posts']) >0:
            return True
        else :
            return False
    else:
        tags = tags.split(',')
        _bool_tag_list = []
        for tag in tags:
            tag = tag.strip()
            _bool_tag_list.append(test_request(tag))
            
        if(len(_bool_tag_list) == sum(_bool_tag_list)):
            return True
        else:
            return False
    

def sort_json_array(json_object, key_name, ascending = False):
    #print(json_object['posts'])
    key_name = key_name.strip()
    json_object['posts'] = sorted(json_object['posts'], key=lambda x : x[key_name], reverse=not(ascending))
    return json_object