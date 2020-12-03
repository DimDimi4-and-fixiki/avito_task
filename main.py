from fastapi import FastAPI
from fastapi import BackgroundTasks
from models import AvitoPair
from db_handler import DataBaseHandler
from web_parser import WebParser
import datetime
import asyncio

app = FastAPI()  # API app

data_base_handler = DataBaseHandler(path="Avito")  # handles all database operations
web_parser = WebParser()  # handles all operations with the web site scrapping
loop = asyncio.get_event_loop()  # event loop of asyncio


async def update_timestamps(pair: AvitoPair):
    """
    Updates all information about timestamps and counters for the pair
    Updates information about top posts for the pair
    :param pair: pair of phrase and region
    """
    while True:
        # adds data about timestamps in the database:
        add_timestamp(pair=pair)

        # Adds top 5 links for the pair in the database
        add_top_posts(pair=pair)
        await asyncio.sleep(3600)  # sleeps for an hour


@app.get("/")
async def root():
    """
    Base method to check that API is working fine
    :return: message that it works
    """
    return {"message": "API is working :)"}


@app.post("/add")
async def add_pair(pair: AvitoPair):
    """
    Adds pair to the database and returns an id of the pair
    Starts to refresh pair's top posts and timestamps every hour
    :param pair:
    :return:
    """
    check_pair = data_base_handler.check_pair(pair=pair)  # checks if pair is new
    pair_id = str(data_base_handler.add_pair(pair))  # adds pair to the db

    if check_pair:  # pair is new
        # Runs periodical updates for timestamps and top posts for a new pair
        asyncio.ensure_future(update_timestamps(pair=pair))

    return {"id": pair_id}  # id of the pair


def add_top_posts(pair: AvitoPair):
    """
    Gets top posts for the pair and adds them to the database
    :param pair: pair of phrase and region
    :return:
    """
    pair_id = str(data_base_handler.get_pair_id(pair=pair))  # id of the pair
    links = web_parser.get_top_posts()  # string with top links
    data_base_handler.add_top_posts(pair_id=pair_id, links=links)  # adds links to the database


def add_timestamp(pair: AvitoPair):
    """
    Updates (counter; timestamp) for the pair
    :param pair: pair of phrase and region
    """
    pair_id = str(data_base_handler.get_pair_id(pair=pair))  # id of the pair
    counter = str(web_parser.get_num_of_posts(pair=pair.dict()))  # gets counter for the pair
    timestamp = str(datetime.datetime.now().timestamp())  # gets current timestamp

    #  packs all parameters in the dictionary
    params = {
        "pair_id": pair_id,
        "counter": counter,
        "timestamp": timestamp,
    }
    data_base_handler.add_timestamp(params=params)  # adds a record to the database


@app.post("/stat")
def get_timestamps(pair_id: str):
    """
    Gets all timestamps and counters for the pair
    :param pair_id: id of the pair
    :return: dictionary with (timestamp: counter)
    """

    # dictionary with all data:
    res = data_base_handler.get_timestamps(pair_id=pair_id)
    return {"result": res}


@app.post("/get_top")
def get_top(pair_id: str):
    """
    Gets top 5 posts for the pair
    :param pair_id: id of the pair
    :return: list of links to the posts
    """

    # list of the links:
    res = data_base_handler.get_top_posts(pair_id=pair_id)
    return {"result": res}



