# 🤖 J.A.R.V.I.S. Voice AI

Este es un asistente virtual inteligente activado por voz, inspirado en J.A.R.V.I.S. de Iron Man. Utiliza Google Gemini para generar respuestas y una interfaz web futurista para la interacción.

## 🚀 Características

*   **Activación por Voz**: Escucha y responde solo cuando se le llama (Palabra clave: "Viernes" o "Jarvis").
*   **Inteligencia Artificial**: Conectado a Google Gemini Pro para responder cualquier pregunta.
*   **Interfaz Futurista**: Diseño visual estilo "Iron Man" con efectos de neón y humo.
*   **Modo Híbrido**: Puedes hablarle o escribirle.

## ⚠️ IMPORTANTE: Cómo ejecutar

Este proyecto **NO** es una página web estática. Requiere un "cerebro" (Python) para funcionar, por lo que no puedes ejecutarlo directamente desde GitHub Pages (eso dará error 404). Debes descargarlo en tu computadora.

### Paso 1: Instalación (Solo la primera vez)

1.  Asegúrate de tener **Python** instalado.
2.  Abre una terminal en la carpeta del proyecto.
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configura tu **API KEY** de Google Gemini en el archivo `jarvis.py`.

### Paso 2: Iniciar J.A.R.V.I.S.

Simplemente haz doble clic en el archivo:
👉 **`iniciar_jarvis.bat`**

Esto abrirá automáticamente:
1.  El servidor de inteligencia artificial.
2.  Tu navegador con la interfaz lista para usar.

---

## 🛠️ Tecnologías

*   Python 3.x
*   Flask (Backend Web)
*   SpeechRecognition & PyAudio (Oído)
*   pyttsx3 (Voz)
*   Google Generative AI (Cerebro)
*   HTML5/CSS3/JS (Interfaz)

Creado por **AleePq**
