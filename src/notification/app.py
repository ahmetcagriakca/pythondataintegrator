from flask import Flask, jsonify, request, Response, render_template
from flask_socketio import SocketIO, send
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = False


@app.route('/')
def index():
    return render_template('index.html')


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


@socketIo.on("connection")
def handleNotification(ntf):
    send('test')


@socketIo.event
def connect():
    print("I'm connected!")


@socketIo.event
def connect_error(data):
    print("The connection failed!")


@socketIo.event
def disconnect():
    print("I'm disconnected!")


if __name__ == '__main__':
    socketIo.run(app, host='0.0.0.0', port=7500)
