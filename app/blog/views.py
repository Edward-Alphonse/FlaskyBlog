from ..blog import blog
from flask import Response
from ..network import ResponseModel

@blog.route('/list', methods=['POST'])
def list():
    result = ResponseModel(0, "success")
    return Response(result.jsonSerialize(), mimetype='application/json')

@blog.route('/tags', methods=['GET'])
def tags():
    result = ResponseModel(0, "success",{"tags": ["123", "456"]})
    return Response(result.jsonSerialize(), mimetype='application/json')

@blog.route('/detail', methods=['GET'])
def detail():
    result = ResponseModel(0, "success",{"tags": ["123", "456"]})
    return Response(result.jsonSerialize(), mimetype='application/json')

@blog.route('/collection', methods=['GET'])
def collection():
    result = ResponseModel(0, "success",{"tags": ["123", "456"]})
    return Response(result.jsonSerialize(), mimetype='application/json')

@blog.route('/archive', methods=['GET'])
def archive():
    result = ResponseModel(0, "success",{"tags": ["123", "456"]})
    return Response(result.jsonSerialize(), mimetype='application/json')