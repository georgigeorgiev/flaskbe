from . import api_v1_0
from flask import jsonify


@api_v1_0.route('/start', methods=['GET'])
def start():
    return jsonify({'message': 'hello'})
