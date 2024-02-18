import cryptocode
import os
from flask import Blueprint, jsonify, request
from flask_login import current_user, AnonymousUserMixin
from flask_cors import cross_origin
from app.auth import token_required

from app.models import Role, User, Config
from . import db, captioner_model
import jwt

captioner = Blueprint('captioner', __name__)

@captioner.route('/api/captioner', methods=['POST'])
@cross_origin()
@token_required
def image_captioner(user):
    captions = captioner_model.generate_captions(request.json.get('images_srcs'))
    return jsonify(captions)