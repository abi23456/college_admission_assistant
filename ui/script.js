const N8N_WEBHOOK_URL = "https://abi1011.app.n8n.cloud/webhook/admission-chat";

// Elements
const chatContainer = document.getElementById('chatContainer');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

// Configure marked.js to use line breaks and sanitize if necessary
marked.setOptions({
    breaks: true,
    gfm: true
});

// Generate unique session ID
function generateSessionId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Generate session ID for this page load
let sessionId = generateSessionId();

// Add message to UI
function addMessage(content, sender, isMarkdown = false) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('message-bubble');

    if (isMarkdown && sender === 'bot') {
        bubbleDiv.innerHTML = marked.parse(content);
    } else {
        bubbleDiv.textContent = content;
    }

    msgDiv.appendChild(bubbleDiv);
    chatContainer.appendChild(msgDiv);

    // Scroll to bottom
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 10);
}

// Add typing indicator
function addTypingIndicator() {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot');
    msgDiv.id = 'typingIndicator';

    const indicatorDiv = document.createElement('div');
    indicatorDiv.classList.add('typing-indicator');

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        indicatorDiv.appendChild(dot);
    }

    msgDiv.appendChild(indicatorDiv);
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Initialize chat
function init() {
    // Initial greeting
    const greeting = "Hello! I am your AI College Admission Assistant. How can I help you today?";
    addMessage(greeting, 'bot', true);
}

// Handle form submit
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const prompt = chatInput.value.trim();
    if (!prompt) return;

    // Add user message
    addMessage(prompt, 'user');

    // Clear input & disable button
    chatInput.value = '';
    sendBtn.disabled = true;
    chatInput.disabled = true;

    // Show typing indicator
    addTypingIndicator();

    try {
        const response = await fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sessionId: sessionId,
                chatInput: prompt
            })
        });

        removeTypingIndicator();

        let assistantReply = "";

        if (response.ok) {
            const data = await response.json();

            // Handle different n8n response structures
            let parsedData = data;
            if (Array.isArray(data) && data.length > 0) {
                parsedData = data[0];
            }

            if (typeof parsedData === 'object' && parsedData !== null) {
                assistantReply = parsedData.output || parsedData.text || parsedData.message || JSON.stringify(parsedData);
            } else {
                assistantReply = String(parsedData);
            }
        } else {
            assistantReply = `**Error**: Received status code ${response.status} from backend. Make sure your n8n workflow is active and allows CORS.`;
        }

        addMessage(assistantReply, 'bot', true);

    } catch (error) {
        removeTypingIndicator();
        const errorMsg = `**Connection Error**: Could not connect to n8n backend (${error.message}). Make sure the webhook URL is correct, n8n is running, and CORS is enabled for the webhook node.`;
        addMessage(errorMsg, 'bot', true);
    } finally {
        // Re-enable input
        sendBtn.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
    }
});

// Initialize on load
window.addEventListener('DOMContentLoaded', init);
