from fastflows import fastflows_app
from fastapi import FastAPI
import uvicorn


app = FastAPI()

app.mount(path="", app=fastflows_app)


if __name__ == "__main__":
    uvicorn.run("fastapi_app:app")
