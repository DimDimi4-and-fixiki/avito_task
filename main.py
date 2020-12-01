from fastapi import FastAPI
from fastapi import BackgroundTasks
from models import AvitoPair
from db_handler import DataBaseHandler
from web_parser import WebParser
import datetime
import asyncio

app = FastAPI()

ids = []
data_base_handler = DataBaseHandler(path="Avito")
web_parser = WebParser()
loop = asyncio.get_event_loop()


async def update_timestamps(pair: AvitoPair):
    while True:
        add_timestamp(pair=pair)
        await asyncio.sleep(3600)  # sleeps for an hour




@app.get("/")
async def root():
    return {"message": "API is working :)"}


@app.post("/add")
async def add_pair(pair: AvitoPair):
    pair_id = str(data_base_handler.add_pair(pair))  # adds pair to the db
    asyncio.ensure_future(update_timestamps(pair=pair))
    return {"id": pair_id}


@app.post("/add_stamp")
def add_timestamp(pair: AvitoPair):
    pair_id = str(data_base_handler.get_pair_id(pair=pair))
    counter = str(web_parser.get_num_of_posts(pair=pair.dict()))
    timestamp = str(datetime.datetime.now().timestamp())
    params = {
        "pair_id": pair_id,
        "counter": counter,
        "timestamp": timestamp,
    }
    data_base_handler.add_timestamp(params=params)
    print("Timestamp is added :)")
    #return {"res": "Timestamp is added"}


@app.post("/get_timestamps")
def get_timestamps(pair_id: int):
    res = data_base_handler.get_timestamps(pair_id=pair_id)
    return {"res": res}


@app.post("/get_html")
def get_html(pair: AvitoPair):
    res = web_parser.get_num_of_posts(pair.dict())
    return {"res": res}


