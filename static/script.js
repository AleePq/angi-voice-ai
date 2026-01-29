document.addEventListener('DOMContentLoaded', () => {
    const displayArea = document.getElementById('displayArea');
    const questionInput = document.getElementById('questionInput');
    const sendBtn = document.getElementById('sendBtn');
    const micBtn = document.getElementById('micBtn');

    let isListening = false;

    // Función para agregar mensajes al chat
    function addMessage(text, type) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', type);
        msgDiv.textContent = text;
        displayArea.appendChild(msgDiv);
        displayArea.scrollTop = displayArea.scrollHeight;
    }

    // Enviar pregunta de texto
    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) return;

        addMessage(question, 'user');
        questionInput.value = '';

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
            const data = await response.json();
            
            if (data.answer) {
                addMessage(data.answer, 'ai');
            } else if (data.error) {
                addMessage(`Error: ${data.error}`, 'system');
            }
        } catch (error) {
            addMessage(`Error de conexión: ${error}`, 'system');
        }
    }

    sendBtn.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendQuestion();
    });

    // Activar micrófono
    micBtn.addEventListener('click', async () => {
        if (isListening) return; // Evitar múltiples clics
        
        isListening = true;
        micBtn.classList.add('active');
        micBtn.innerHTML = '<span class="icon">🔴</span> ESCUCHANDO...';

        try {
            const response = await fetch('/listen', {
                method: 'POST'
            });
            const data = await response.json();

            if (data.question) {
                addMessage(data.question, 'user');
                if (data.answer) {
                    addMessage(data.answer, 'ai');
                }
            } else if (data.error) {
                // No es necesariamente un error grave, puede ser silencio
                if (data.error !== 'No se escuchó nada') {
                    addMessage(data.error, 'system');
                }
            }
        } catch (error) {
            addMessage(`Error de audio: ${error}`, 'system');
        } finally {
            isListening = false;
            micBtn.classList.remove('active');
            micBtn.innerHTML = '<span class="icon">🎙️</span> ACTIVAR AUDIO';
        }
    });
});
