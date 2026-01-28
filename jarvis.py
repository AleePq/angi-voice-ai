import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
import sys

# --- CONFIGURACIÓN ---

# CLAVE DE API DE GOOGLE GEMINI
# Debes obtener una clave gratuita aquí: https://aistudio.google.com/app/apikey
API_KEY = "AIzaSyAcW6fg_iYz1Tp57F9B9yeYYQh3S_e20C4"

# PALABRA SECRETA DE ACTIVACIÓN
# Solo se activará si dices esta frase exacta.
PALABRA_CLAVE = "viernes" 

# Configuración de la IA (Gemini)
# Se asume que la clave ha sido configurada si no es el placeholder original
if API_KEY != "AIzaSyAcW6fg_iYz1Tp57F9B9yeYYQh3S_e20C4":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    print("ADVERTENCIA: No has configurado tu API KEY de Gemini.")

# Inicializar síntesis de voz (Text-to-Speech)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Intentar seleccionar una voz en español
for voice in voices:
    if "spanish" in voice.name.lower() or "es-" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150) # Velocidad de habla un poco más rápida

def hablar(texto):
    """Convierte texto a voz."""
    print(f"JARVIS: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    """Escucha el micrófono y devuelve el texto reconocido."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando ruido ambiente para calibrar...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Esperando comando...")
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            texto = r.recognize_google(audio, language="es-ES")
            return texto.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            hablar("Error de conexión con el servicio de voz.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

def consultar_ia(pregunta):
    """Envía la pregunta a Gemini y obtiene una respuesta concisa."""
    if not model:
        return "Por favor, configura tu clave de API en el código."
    
    try:
        # Prompt del sistema para forzar respuestas concisas
        prompt = f"""
        Eres una IA asistente tipo JARVIS. 
        Responde a la siguiente pregunta de manera EXTREMADAMENTE concisa, directa y breve.
        Máximo 2 o 3 oraciones. Sin saludos ni despedidas innecesarias.
        
        Pregunta: {pregunta}
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Ocurrió un error al consultar la IA: {str(e)}"

def main():
    print(f"--- INICIANDO SISTEMA ---")
    print(f"Palabra clave: '{PALABRA_CLAVE}'")
    
    if API_KEY == "AIzaSyAcW6fg_iYz1Tp57F9B9yeYYQh3S_e20C4":
        print("\n[IMPORTANTE] Necesitas poner tu API KEY en el archivo jarvis.py")
        hablar("Sistemas iniciados. Por favor configura tu clave de acceso.")
    else:
        hablar("Sistemas en línea. Esperando activación.")

    activo = False

    while True:
        try:
            texto = escuchar()
            
            if texto:
                print(f"Oído: {texto}")

            # Lógica de activación
            if PALABRA_CLAVE in texto and not activo:
                activo = True
                hablar("Sí, señor. ¿Qué necesita?")
                continue # Saltar al siguiente ciclo para escuchar el comando inmediatamente
            
            # Si ya está activo, procesar comandos
            if activo:
                if "desactivar" in texto or "descansar" in texto:
                    activo = False
                    hablar("Entendido. Entrando en modo de espera.")
                elif texto:
                    # Enviar a la IA
                    respuesta = consultar_ia(texto)
                    hablar(respuesta)
                    # Opcional: Desactivarse después de responder para volver a requerir la clave
                    # activo = False 
            
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

if __name__ == "__main__":
    main()
