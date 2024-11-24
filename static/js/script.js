// Function to send user input to the backend
function sendMessage() {
    const userInput = document.getElementById('user_input').value;
    if (userInput) {
        const chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += `<div class="message">You: ${userInput}</div>`;
        document.getElementById('user_input').value = '';  // Clear the input field
        
        // Send the input to the Flask backend
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            const responseMessage = data.response;
            chatbox.innerHTML += `<div class="message">Bot: ${responseMessage}</div>`;
            chatbox.scrollTop = chatbox.scrollHeight;  // Auto scroll to the bottom
        });
    }
}

// Function to start voice input (uses Web Speech API)
function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.start();

    recognition.onresult = function(event) {
        const userInput = event.results[0][0].transcript;
        document.getElementById('user_input').value = userInput;
        sendMessage();  // Send the voice input to the backend
    };

    recognition.onerror = function(event) {
        alert("Sorry, I couldn't hear you properly.");
    };
}
