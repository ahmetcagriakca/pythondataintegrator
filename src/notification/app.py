from flask import Flask, jsonify, request, Response
from flask_socketio import SocketIO, send
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'


@app.route('/notify', methods=['POST'])
def add_user():
    request_data = request.get_json()
    if (type(request_data) is not dict):
        request_data = json.loads(request_data)
    socketIo.emit('notification', request_data)

    result = {
        "IsSuccess": True
    }
    return Response(json.dumps(result), status=200, mimetype='applciation/json')


@socketIo.on("notification")
def handleNotification(ntf):
    send(ntf, broadcast=True)
    return None


if __name__ == '__main__':
    socketIo.run(app, port=7500)
