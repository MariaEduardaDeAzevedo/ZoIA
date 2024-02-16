import base64
import requests
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer, pipeline
import torch
import os
from datetime import datetime
from PIL import Image
import io
import tempfile 

class Captioner():
    def __init__(self) -> None:
        root_path = os.path.dirname(__file__).split('services')[0]
        self.model = VisionEncoderDecoderModel.from_pretrained(os.path.join(root_path, "assets","model"))
        self.feature_extractor = ViTImageProcessor.from_pretrained(os.path.join(root_path, "assets", "feature_extractor"))
        self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(root_path, "assets","tokenizer"))

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        self.translator_model = M2M100ForConditionalGeneration.from_pretrained(os.path.join(root_path, "assets","translation_model"))
        self.translator_tokenizer = M2M100Tokenizer.from_pretrained(os.path.join(root_path, "assets","translation_tokenizer"))
        self.translator_tokenizer.src_lang = 'en'

        self.extensions = ["jpg", "png", "jpeg"]
        self.max_length = 16
        self.num_beams = 4
        self.gen_kwargs = {"max_length": self.max_length, "num_beams": self.num_beams}

    def generate_captions(self, srcs: list):

        if len(srcs) > 0:
            imgs = dict()
            successful_imgs = []

            for i, src in enumerate(srcs):
                if src.startswith("data:image"):
                    img = self.__decodeBase64(src)
                    imgs[i] = img

                    if img is not None:
                        successful_imgs.append(img)
                else:
                     img = self.__downloadImage(src)
                     imgs[i] = img

                     if img is not None:
                        successful_imgs.append(img)

            predictions_values = self.__predict_step(successful_imgs)
            predictions = dict()

            pred_counter = 0
            for key in sorted(list(imgs.keys())):
                img = imgs[key]

                if img is None:
                    predictions[key] = 'Could not generate a caption.'
                else:
                    predictions[key] = self.__translate(predictions_values[pred_counter])
                    pred_counter += 1


        return predictions

    def __predict_step(self, images:list):
        pixel_values = self.feature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        output_ids = self.model.generate(pixel_values, **self.gen_kwargs)

        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        return preds

    def __downloadImage(self, src:str):
        try:
            response = requests.get(src)
            imgdata = response.content

            img = Image.open(io.BytesIO(imgdata))

            return img
        except Exception as e:
            return None

    def __decodeBase64(self, image:str):
        try:
            metadata, data = image.split("base64")
            extension = metadata.split("/")[-1][:-1]
            data = data[1:]

            data_bytes = bytes(data, "utf-8")
            file_path = f"tmp/{''.join(str(datetime.now().timestamp()).split('.'))}.{extension}"

            tmp = tempfile.NamedTemporaryFile()

            try:
                tmp.write(data_bytes)
                tmp.seek(0)
            finally:
                tmp.close()

            # with open(file_path, "wb") as fh:
            #     fh.write(base64.decodebytes(data_bytes))

            img = Image.open(tmp.name)
            return img
        except:
            return None
        
    def __translate(self, text:str):
        encoded_text = self.translator_tokenizer(text, return_tensors="pt")
        generated_tokens = self.translator_model.generate(**encoded_text, forced_bos_token_id=self.translator_tokenizer.get_lang_id("pt"))
        
        return self.translator_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)