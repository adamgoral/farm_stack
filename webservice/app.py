from fastapi import FastAPI

app = FastAPI()

print('starting up')

@app.get("/")
async def get_root():
    """Return a simple status message."""
    return {"status": "OK"}