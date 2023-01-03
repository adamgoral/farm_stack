from dataclasses import dataclass, field
from fastapi import Body, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List, Optional
import datetime as dt

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = AsyncIOMotorClient(os.environ['MONGODB_URL'])
    app.mongodb = app.mongodb_client.football
    collections = await app.mongodb.list_collection_names()
    if 'prices' not in collections:
        await create_ts('prices')
    if 'matches' not in collections:
        await app.mongodb.create_collection('matches')

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()

async def create_ts(collection_name: str):
    try:
        await app.mongodb.create_collection(collection_name,
         timeseries={
            'timeField': 'timestamp',
            'granularity': 'seconds'
         })
    except Exception as e:
        print(f'create_ts: {e}')

async def create_prices():
    await create_ts('prices')
    now = dt.datetime.now()
    prices = []
    for i in range(1, 11):
        prices.append({'timestamp': now + dt.timedelta(seconds=i), 'price': i})

    return await app.mongodb.prices.insert_many(prices)

@app.get("/")
async def get_root():
    """Return a simple status message."""
    return { "status": "OK" }

@app.get("/sports/prices")
async def get_prices():
    await create_ts('prices')
    prices = await app.mongodb.prices.find({}).to_list(None)
    for price in prices:
        price['id'] = str(price['_id'])
        del price['_id']
    return prices

@app.post('/sports/prices')
async def post_prices(prices: List[dict] = Body(...)):
    """Save a list of prices."""
    await create_ts('prices')
    result = await app.mongodb.prices.insert_many(prices)
    return JSONResponse(status_code=status.HTTP_201_CREATED)

@dataclass
class Match:
    """A football match"""
    id: int
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int

@app.get("/sports/football/matches")
async def get_football_matches():
    """Return a list of football matches."""
    matches = await app.mongodb.matches.find({}).to_list(None)
    for match in matches:
        match['id'] = str(match['_id'])
        del match['_id']
    return matches

@app.post("/sports/football/matches")
async def post_football_matches(matches: List[Match] = Body(...)):
    """Save a list of football matches."""
    matches = jsonable_encoder(matches)
    for match in matches:
        match['_id'] = match['id']
        del match['id']

    print(f'type: {type(matches)}) value: {matches}')
    result = await app.mongodb.matches.insert_many(matches)
    added_matches = await app.mongodb.matches.find({'_id': {'$in': result.inserted_ids}}).to_list(None)
    print(f'added_matches: {added_matches}')
    for match in added_matches:
        match['id'] = str(match['_id'])
        del match['_id']
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_matches)