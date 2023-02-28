from datetime import datetime
from services.AuthService import check_token
import base64
import cv2 as cv
from PIL import Image
import numpy as np
import io
import requests
import os
from utils.messages import CAPTIONS_SUCCESSFULLY_GENERATED

from utils.response import build_response

TEMP_DIR = "tmp"
extensions = ["jpg", "png", "jpeg"]

def captioner(token, data, ip):
    valid, message, _ = check_token(token, ip)
    response = None
    
    if valid:
        srcs = data["imgs_src"]
        
        if len(srcs) > 0:
            
            imgs = list()

            for src in srcs:
                if src.startswith("data:image"):
                    imgs.append(__decodeBase64(src))
                else:
                    imgs.append(__downloadImage(src))
        
        response = build_response(CAPTIONS_SUCCESSFULLY_GENERATED, status_code=200, data={
            "captions": list(map(lambda x: "Descrição gerada automaticamente com ZoIA" if x is not None else "Não foi possível realizar a descrição dessa imagem com ZoIA", srcs))
        })
    else:
        response = build_response(message, status_code=403)

    return response

def __decodeBase64(image:str):
    try:
        metadata, data = image.split("base64")
        extension = metadata.split("/")[-1][:-1]
        data = data[1:]

        data_bytes = bytes(data, "utf-8")
        file_path = f"{TEMP_DIR}/{''.join(str(datetime.now().timestamp()).split('.'))}.{extension}"

        with open(file_path, "wb") as fh:
            fh.write(base64.decodebytes(data_bytes))

        img = Image.open(file_path)
        os.remove(file_path)
        return np.array(img)
    except:
        return None


def __downloadImage(src:str):
    try:
        response = requests.get(src)
        imgdata = response.content

        img = Image.open(io.BytesIO(imgdata))
        img.seek(0)

        #file_path = f"{TEMP_DIR}/{''.join(str(datetime.now().timestamp()).split('.'))}.png"
        #img.save(file_path)

        return np.array(img)
    except: 
        return None
    