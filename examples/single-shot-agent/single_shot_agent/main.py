import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def run_dev_server():
    uvicorn.run("single_shot_agent.main:app", host="0.0.0.0", port=8000, reload=True)
