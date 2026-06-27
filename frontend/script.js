// -------------------------
// Element references
// -------------------------
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatOutput = document.getElementById('chat-output');

// -------------------------
// FastAPI endpoint
// -------------------------
const PROXY_URL = "http://localhost:8000/ask";

// -------------------------
// Add message to chat
// -------------------------
function addMessage(message, senderClass) {
    const messageDiv = document.createElement('div');
    messageDiv.className = senderClass;
    messageDiv.textContent = message;
    chatOutput.appendChild(messageDiv);
    
    // Auto-scroll
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

// -------------------------
// Reset chat button
// -------------------------
document.addEventListener("DOMContentLoaded", () => {
    const resetBtn = document.getElementById("reset-chat-btn");
    if (!resetBtn || !chatOutput) return;

    resetBtn.addEventListener("click", () => {
        chatOutput.innerHTML = `
            <div class="chat-placeholder text-muted text-center">
                <p class="mb-1">Welcome to your custom GPT workspace ✨</p>
                <small>Ask anything to begin.</small>
            </div>
        `;
    });
});

// -------------------------
// Handle form submit
// -------------------------
if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userMessage = chatInput.value.trim();
        if (!userMessage) return;

        // Display user message
        addMessage(userMessage, 'user-message');
        chatInput.value = '';

        // Show loading
        const loadingMessage = 'AI is thinking...';
        addMessage(loadingMessage, 'ai-loading');
        const loadingDiv = chatOutput.querySelector('.ai-loading');

        try {
            const response = await fetch(PROXY_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: userMessage })
            });

            if (!response.ok) throw new Error(`Server error! Status: ${response.status}`);

            const data = await response.json();
            const aiResponse = data.answer || "Sorry, no response from AI.";

            // Remove loading
            if (loadingDiv) chatOutput.removeChild(loadingDiv);

            // Display AI response
            addMessage(aiResponse, 'ai-message');

        } catch (error) {
            if (loadingDiv) chatOutput.removeChild(loadingDiv);
            addMessage(`Error: ${error.message}`, 'error-message');
            console.error(error);
        }
    });
}
