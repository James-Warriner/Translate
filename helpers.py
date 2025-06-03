from flask import jsonify

def returnError(message, status=400):
  return jsonify({"message":message}),status