from fastapi import FastAPI
from models import MsgPayload

app = FastAPI()
messages_list: dict[int, MsgPayload] = {}


# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}


