from datetime import datetime
from services.AuthService import check_token
import base64
from PIL import Image
import numpy as np
import io
import requests
import os
from utils.messages import CAPTIONS_SUCCESSFULLY_GENERATED

from utils.response import build_response

from app import model, tokenizer, feature_extractor, device

TEMP_DIR = "tmp"
extensions = ["jpg", "png", "jpeg"]

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def __predict_step(images):

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds


def captioner(token, data, ip):
    valid, message, _ = check_token(token, ip)
    response = None
    
    if valid:
        srcs = data["imgs_src"]
        predictions = dict()

        if len(srcs) > 0:
            
            imgs = dict()
            successful_imgs = dict()

            counter = 0
            for src in srcs:
                if src.startswith("data:image"):
                    img = __decodeBase64(src)
                    imgs[counter] = img
                    
                    if img is not None:
                        successful_imgs[counter] = img
                else:
                     img = __downloadImage(src)
                     imgs[counter] = img

                     if img is not None:
                        successful_imgs[counter] = img

                counter += 1

            sorted_keys = sorted(successful_imgs.keys())
            successful_imgs = {key:successful_imgs[key] for key in sorted_keys}
            
            predictions_values = __predict_step(list(successful_imgs.values())) if len(list(successful_imgs.values())) > 0 else []
            
            for key in imgs.keys():
                if key in sorted_keys:
                    idx = sorted_keys.index(key)
                    predictions[key] = predictions_values[idx]
                else:
                    predictions[key] = None

        sorted_keys = sorted(predictions.keys())
        predictions = {key:predictions[key] for key in sorted_keys}
        
        response = build_response(CAPTIONS_SUCCESSFULLY_GENERATED, status_code=200, data={
            "captions": list(map(lambda x: predictions[x] if x is not None else "Não foi possível realizar a descrição dessa imagem com ZoIA", predictions.keys()))
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
        #os.remove(file_path)
        return img
    except:
        return None


def __downloadImage(src:str):
    try:
        response = requests.get(src)
        imgdata = response.content

        img = Image.open(io.BytesIO(imgdata))
    
        file_path = f"{TEMP_DIR}/{''.join(str(datetime.now().timestamp()).split('.'))}.png"
        img.save(file_path)

        return img
    except: 
        return None
    