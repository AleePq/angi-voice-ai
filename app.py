from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import jarvis
import threading
import queue

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Cola para manejar las solicitudes de voz secuencialmente
voice_queue = queue.Queue()

def voice_worker():
    """Procesa las solicitudes de voz en un hilo separado."""
    while True:
        text = voice_queue.get()
        if text:
            try:
                jarvis.hablar(text)
            except Exception as e:
                print(f"Error al hablar: {e}")
        voice_queue.task_done()

# Iniciar hilo de voz
threading.Thread(target=voice_worker, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Consultar a Gemini
    response_text = jarvis.consultar_ia(question)
    
    # Encolar respuesta de voz
    voice_queue.put(response_text)
    
    return jsonify({'answer': response_text})

@app.route('/listen', methods=['POST'])
def trigger_listen():
    """Activa el micrófono del servidor para escuchar."""
    try:
        text = jarvis.escuchar()
        if text:
            # Si se escuchó algo, procesarlo
            if jarvis.PALABRA_CLAVE in text or True: # Ignoramos palabra clave si es botón manual
                 response_text = jarvis.consultar_ia(text)
                 voice_queue.put(response_text)
                 return jsonify({'question': text, 'answer': response_text})
        return jsonify({'error': 'No se escuchó nada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import webbrowser

if __name__ == '__main__':
    print("Iniciando servidor web Jarvis...")
    # Abrir el navegador automáticamente
    webbrowser.open('http://127.0.0.1:5000')
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
