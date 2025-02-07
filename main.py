from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from service.email_service import read_emails_from_gmail

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}

@app.get("/mail")
def about() -> dict[str, str]:
    return read_emails_from_gmail()

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "message": "Esta é a página inicial."})