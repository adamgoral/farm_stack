from dataclasses import dataclass, field
from fastapi import Body, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List, Optional

app = FastAPI()
client = AsyncIOMotorClient(os.environ['MONGODB_URL'])

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
    db = client.football
    matches = await db.matches.find({}).to_list(None)
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
    db = client.football
    result = await db.matches.insert_many(matches)
    added_matches = await db.matches.find({'_id': {'$in': result.inserted_ids}}).to_list(None)
    print(f'added_matches: {added_matches}')
    for match in added_matches:
        match['id'] = str(match['_id'])
        del match['_id']
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_matches)