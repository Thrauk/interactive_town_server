import uvicorn
from fastapi import FastAPI

from routers import agent_router


app = FastAPI()

app.include_router(agent_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    # uvicorn main:app --reload
