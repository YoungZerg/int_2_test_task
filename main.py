import scanner
from config import error_counter_global
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
def main_page(request: Request, ip_address = Form(), port=Form(), login=Form(), passwd=Form()): 
    
    scan = scanner.Scanner(login, passwd, port, ip_address)
    scan.ssh_conn_n_parse()

    if error_counter_global != 0:
        return templates.TemplateResponse("error.html", {"request": request, "error_code": error_counter_global})
    
    return templates.TemplateResponse("success.html", {"request": request})


@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


@app.get("/error", response_class=HTMLResponse)
def error_page(request: Request, error_code = error_counter_global):
    return templates.TemplateResponse("error.html", {"request": request, "error_code": error_code})
