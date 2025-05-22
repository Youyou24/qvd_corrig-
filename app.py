from flask import Flask, request, jsonify
import pandas as pd
from qvd import qvd_reader
import os

app = Flask(__name__)

@app.route('/qvd', methods=["GET"])
def getQVD():
    badRequest = {"ERROR": "Bad Request", "STATUS": 400, "MESSAGE": "path and name parameters are required"}
    notFound = {"ERROR": "Not Found", "STATUS": 404, "MESSAGE": "QVD file not found"}

    qvdPath = request.args.get('path')
    qvdName = request.args.get('name')

    if not qvdPath or not qvdName:
        return jsonify(badRequest), 400

    filename = os.path.join(qvdPath, qvdName + ".qvd")
    if not os.path.exists(filename):
        return jsonify(notFound), 404

    try:
        # Lecture QVD
        df = qvd_reader.read(filename)

        # Convertir en dict puis JSON
        data = df.to_dict(orient='records')
        return jsonify(data)

    except Exception as e:
        return jsonify({"ERROR": "Internal Server Error", "STATUS": 500, "MESSAGE": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
