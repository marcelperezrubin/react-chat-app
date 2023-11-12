from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import requests

app = Flask(__name__, static_folder='frontend/dist')
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Manejar solicitudes de pronóstico del tiempo
@app.route('/weather/<city>')
def obtener_pronostico_ciudad(city):
    try:
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        respuesta = requests.get(url).json()
        return jsonify(respuesta)
    except Exception as error:
        print('Error al obtener el pronóstico del tiempo:', str(error))
        return jsonify({'error': 'Error al obtener el pronóstico del tiempo'}), 500

# Ruta para servir archivos estáticos del frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path != '' and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@socketio.on('connect')
def handle_connect():
    session_id = request.args.get('sessionId')
    print(f"Cliente conectado: {session_id}")

@socketio.on('message')
def handle_message(data):
    session_id = request.args.get('sessionId')
    print(f"Mensaje recibido de {session_id}: {data}")
    emit('message', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, port=int(os.environ.get('PORT', 5000)))
