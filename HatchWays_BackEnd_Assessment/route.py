
from settings import *
from flask import request
from utility import *
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
        (sortBy.strip() not in SORT_GROUP and (sortBy != None ) ) or
        (direction.strip() not in DIRECTION_GROUP and (direction != None ))
    ):
        return {
            "error": "sortBy parameter is invalid"}, 400
    else:
        direction = False if direction.strip().lower()  == 'desc' else True
        downloadData = get_Hatchways_API(tags)
        json_array = sort_json_array(downloadData, sortBy, direction)

        return json_array, 200