from fastapi import FastAPI
from models import MsgPayload
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


app = FastAPI()
messages_list: dict[int, MsgPayload] = {}

templates = Jinja2Templates(directory="templates")


# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "message": "Esta é a página inicial."})