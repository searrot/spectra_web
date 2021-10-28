from fastapi import FastAPI, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random, os, uuid
import requests
import uvicorn
import cv2
import numpy as np
import io
from PIL import Image
from db import DataBase
from sqlite3 import IntegrityError

'''--------------------------------------------------------------------------------------------'''

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
IMAGES = './user_images/'
templates = Jinja2Templates(directory="templates")
extentions = ['jpg', 'jpeg', 'png', 'webp', 'bmp']
user_id = None

base = DataBase()
base.connect()
base.create_table()
ids = base.get_ids()

def create_id():
    id = random.randint(1, 1000000)
    if id not in ids:
        return id
    else:
        create_id()

'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

class Item(BaseModel):
    language = 'english'

class Registrator(BaseModel):
    log: str
    pass1: str
    pass2: str

    @classmethod
    def as_form(cls, log: str = Form(...), pass1: str = Form(...), pass2: str = Form(...)):
        return cls(log=log, pass1=pass1, pass2=pass2)

class Signer(BaseModel):
    log: str
    pass1: str

    @classmethod
    def as_form(cls, log: str = Form(...), pass1: str = Form(...)):
        return cls(log=log, pass1=pass1)
'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

@app.get('/', response_class=HTMLResponse)
async def get_webpage(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

@app.get('/log', response_class=HTMLResponse)
async def get_log_webpage(request: Request):
    return templates.TemplateResponse("log.html", {"request": request})

@app.post('/log', response_class=HTMLResponse)
async def get_login(request: Request, reg: Registrator = Depends(Registrator.as_form)):
    log, pass1, pass2 = reg.log, reg.pass1, reg.pass2
    if pass1 == pass2:
        email = 'non'
        id = create_id()
        score = 0
        password = pass1
        try:
            base.create_user(id, log, password, score, email)
            os.mkdir(f'{IMAGES}{id}')
        except IntegrityError:
            return templates.TemplateResponse("log.html", {"request": request})
        global ids
        ids = base.get_ids()
        return templates.TemplateResponse("main.html", {"request": request})
    else:
        pass
'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

@app.get('/sign', response_class=HTMLResponse)
async def get_sign_webpage(request: Request):
    return templates.TemplateResponse("sign.html", {"request": request})

@app.post('/sign', response_class=HTMLResponse)
async def get_sign(request: Request, sign: Signer = Depends(Signer.as_form)):
    images = sorted(os.listdir(IMAGES))
    log, pass1 = sign.log, sign.pass1
    if base.get_name(log) and base.get_pass(log, pass1):
        user_id = log
        return templates.TemplateResponse("profile.html", {"request": request, 'images': images})
    else:
        return templates.TemplateResponse("sign.html", {"request": request})
'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

@app.get('/profile', response_class=HTMLResponse)
async def get_profile_webpage(request: Request):
    images = os.listdir(IMAGES)
    return templates.TemplateResponse("profile.html", {"request": request, 'images': images})

@app.post('/profile', response_class=HTMLResponse)
async def upload_photo(request: Request, file: UploadFile = File(...)):
    try:
        image = await file.read()
        images = sorted(os.listdir(IMAGES))
        file.filename = f'{images[-1].split(".")[0] + "1"}.jpg'
        
        img = np.array(Image.open(io.BytesIO(image)))
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        cv2.imwrite(f'{IMAGES}{file.filename}', img)
        images = sorted(os.listdir(IMAGES))
        last = np.array(Image.open((f'{IMAGES}{images[-1]}')))
        lastt = np.array(Image.open((f'{IMAGES}{images[-2]}')))

        if not np.array_equal(lastt, last):
            pass
        else:
            os.remove(f'{IMAGES}{images[-1]}')
        print('1')
        return templates.TemplateResponse("main.html", {"request": request})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("main.html", {"request": request})
        #нужно сделать перенаправление на страницу с ошибкой либо с упешной загрузкой

'''--------------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    uvicorn.run('main_fast:app', reload=True)