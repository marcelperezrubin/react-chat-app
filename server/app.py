from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
socketio = SocketIO(app, cors_allowed_origins="*")




# Resto del código...


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")



# Manejar solicitudes de pronóstico del tiempo
@app.route('/weather/<city>')
def obtener_pronostico_ciudad(city):
    try:
        api_key = os.environ.get('OPENWEATHER_API_KEY')  # Usar variables de entorno para proteger claves
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

        respuesta = requests.get(url).json()
        return jsonify(respuesta)
    except Exception as error:
        print('Error al obtener el pronóstico del tiempo:', str(error))
        return jsonify({'error': 'Error al obtener el pronóstico del tiempo'}), 500

@socketio.on('connect')
def handle_connect():
    print(f"Cliente conectado: {request.sid}")

@socketio.on('message')
def handle_message(data):
    print(f"Mensaje recibido: {data}")
    emit('message', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, port=int(os.environ.get('PORT', 5000)))
