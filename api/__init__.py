from flask import Blueprint, jsonify, request
from detect_api.api import calculation

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify({'column': 'value'}, 201)


@api.route('/detect', methods=['POST'])
def detection():
    return calculation.detection(request)