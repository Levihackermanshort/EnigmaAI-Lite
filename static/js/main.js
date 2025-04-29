document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');

    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const query = userInput.value.trim();
        if (!query) return;

        // Add user message to chat
        addMessage(query, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `query=${encodeURIComponent(query)}`
            });

            const data = await response.json();
            addMessage(data.answer, 'bot', data.source);
        } catch (error) {
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    });

    function addMessage(text, sender, source = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = text;

        if (source) {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'source';
            sourceDiv.textContent = `Source: ${source}`;
            messageDiv.appendChild(sourceDiv);
        }

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}); 