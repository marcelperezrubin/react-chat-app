from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import os
import requests

app = Flask(__name__, static_folder='frontend/dist')
CORS(app, resources={r"/*": {"origins": "https://react-chat-capstone-project-5721959f643e.herokuapp.com"}})
socketio = SocketIO(app, cors_allowed_origins="*") 

# Mantén un seguimiento de los nombres de usuario asignados
user_count = 0

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
    global user_count
    session_id = request.args.get('sessionId')
    user_count += 1
    username = f'User{user_count}'
    print(f"Cliente conectado: {username}, session_id: {session_id}")
    emit('username_assigned', {'username': username})  # Envia el nombre de usuario al cliente

@socketio.on('message')
def handle_message(data):
    session_id = request.args.get('sessionId')
    username = request.args.get('username', 'Unknown')  # Si no hay nombre de usuario, usa 'Unknown'
    print(f"Mensaje recibido de {username} ({session_id}): {data}")
    emit('message', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, port=int(os.environ.get('PORT', 5000)))
