from dataclasses import dataclass
from fastapi import Body, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pymongo import MongoClient
import os
from typing import List

app = FastAPI()

print('starting up')

@app.get("/")
async def get_root():
    """Return a simple status message."""
    return { "status": "OK" }

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
    client = MongoClient(os.environ['MONGODB_URL'])
    db = client.football
    matches = list(db.matches.find({}))
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
    client = MongoClient(os.environ['MONGODB_URL'])
    db = client.football
    result = db.matches.insert_many(matches)
    added_matches = list(db.matches.find({'_id': {'$in': result.inserted_ids}}))
    print(f'added_matches: {added_matches}')
    for match in added_matches:
        match['id'] = str(match['_id'])
        del match['_id']
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_matches)