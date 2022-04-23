from collections import OrderedDict
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
        
    def keySet(self):
        return list(self.cache.keys())