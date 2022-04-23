
from flask import Flask
from utility import *

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



app = Flask(__name__)

app.config.from_mapping(config)

