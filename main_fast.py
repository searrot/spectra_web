from fastapi import FastAPI, Request, UploadFile, File, Form
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
from typing import List

'''--------------------------------------------------------------------------------------------'''

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
IMAGES = './static/user_images/'
templates = Jinja2Templates(directory="templates")
extentions = ['jpg', 'jpeg', 'png', 'webp', 'bmp']

'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

class Item(BaseModel):
    language = 'english'

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

@app.post('/log', response_model=BaseModel)
async def get_login( nn: str = Form(...), nn1: str = Form(...), nn2: str = Form(...)):
    print(nn,nn1,nn2)
    
'''--------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------'''

@app.get('/sign', response_class=HTMLResponse)
async def get_sign_webpage(request: Request):
    return templates.TemplateResponse("sign.html", {"request": request})

@app.post('/sign', response_model=BaseModel)
async def get_sign(nn: str = Form(...)):
    pass

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