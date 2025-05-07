function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = chatContainer.style.display === "block" ? "none" : "block";
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const userText = input.value.trim();
    if (!userText) return;

    addMessage("You", userText, "user-message");
    input.value = "";
    
    document.getElementById("typing-indicator").style.display = "block";

    fetch(`/get?msg=${userText}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("typing-indicator").style.display = "none";
            addMessage("Bot", data, "bot-message");
        });
}

function addMessage(sender, text, className) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(className);
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
