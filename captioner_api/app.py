from flask import Flask, request
from flask_cors import CORS, cross_origin
from database.manipulation import init_database, kill

from services import AuthService, CaptionerService, UserService

import json
import os

from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

print("Loading model...")
model = VisionEncoderDecoderModel.from_pretrained("assets/model")
print("Loading featire extractor...")
feature_extractor = ViTImageProcessor.from_pretrained("assets/feature_extractor")
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("assets/tokenizer")

print("Configuring device...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device configured: {device}")
model.to(device)
 
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

init_database(bool(os.environ["RESTART_DATABASE"]))

@app.route("/login", methods=["POST"])
@cross_origin(origin='*')
def login():
    data = request.data
    return AuthService.login(json.loads(data), request.remote_addr)

@app.route("/user", methods=["POST"])
@cross_origin(origin='*')
def register_user():
    data = request.data
    return UserService.save(json.loads(data))

@app.route("/user/<email>", methods=["GET"])
@cross_origin(origin='*')
def get_user(email):
    return UserService.get(email)

@app.route("/account", methods=["GET"])
@cross_origin(origin='*')
def get_logged():
    token = request.headers["Authorization"]
    return AuthService.get_account(token, request.remote_addr)

@app.route("/captioner", methods=["POST"])
@cross_origin(origin="*")
def captioner():
    data = request.data
    token = request.headers["Authorization"]
    return CaptionerService.captioner(token, json.loads(data), request.remote_addr)

if __name__ == "__main__":
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
        
    app.run(debug=False, host="0.0.0.0")
    kill()
