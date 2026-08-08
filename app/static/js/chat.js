const chatWindow = document.getElementById('chatWindow');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const appArea = document.getElementById('appArea');

let typingIndicator = null;
let isFirstMessage = true;

function renderMarkdown(text) {
    if (typeof marked !== 'undefined') {
        marked.setOptions({ breaks: true, gfm: true, sanitize: false });
        return marked.parse(text);
    }
    return text;
}

function addMessageToChat(username, text, time, isMarkdown = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    if (username === 'LandarevAI') messageDiv.classList.add('ai-message');

    const headerDiv = document.createElement('div');
    headerDiv.className = 'message-header';
    headerDiv.innerHTML = `
        <span class="username">${escapeHtml(username)}</span>
        <span class="time">${escapeHtml(time)}</span>
    `;

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    if (isMarkdown) {
        try {
            textDiv.innerHTML = renderMarkdown(text);
        } catch (error) {
            window.location.href = `/error?code=500`;
        }
    } else {
        textDiv.textContent = text;
    }

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(textDiv);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showTypingIndicator() {
    removeTypingIndicator();
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'typing-indicator';
    indicatorDiv.id = 'typingIndicator';
    indicatorDiv.innerHTML = `
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
        <span class="typing-label">LandarevAI печатает...</span>
    `;
    chatWindow.appendChild(indicatorDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    typingIndicator = indicatorDiv;
}

function removeTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.remove();
        typingIndicator = null;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getCurrentTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' +
           now.getMinutes().toString().padStart(2, '0');
}

async function sendMessageToAPI(text) {
    try {
        const response = await fetch(`/api/v1/ai/?message=${encodeURIComponent(text)}`);
        if (!response.ok) {
            window.location.href = `/error?code=${response.status}`;
        }
        const data = await response.json();
        return data.message;
    } catch (error) {
        window.location.href = `/error?code=500`;
    }
}

function switchToChatMode() {
    if (!appArea.classList.contains('chat-mode')) {
        appArea.classList.add('chat-mode');
        setTimeout(() => {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }, 50);
    }
}

async function sendMessage() {
    const text = messageInput.value.trim();
    // Имя берем из localStorage или ставим по умолчанию, так как поля имени больше нет в UI
    const username = localStorage.getItem('username') || 'Пользователь';

    if (!text) {
        messageInput.focus();
        messageInput.style.borderColor = '#ef4444';
        setTimeout(() => {
            messageInput.style.borderColor = 'transparent';
        }, 1000);
        return;
    }

    if (isFirstMessage) {
        switchToChatMode();
        isFirstMessage = false;
    }

    sendButton.disabled = true;
    messageInput.disabled = true;
    // Меняем иконку на спиннер / текст
    sendButton.innerHTML = `<span style="font-size:12px;font-weight:600;">...</span>`;

    const userTime = getCurrentTime();
    addMessageToChat(username, text, userTime, false);
    messageInput.value = '';

    try {
        showTypingIndicator();
        const apiResponse = await sendMessageToAPI(text);
        removeTypingIndicator();
        const aiTime = getCurrentTime();
        addMessageToChat('LandarevAI', apiResponse, aiTime, true);
    } catch (error) {
        removeTypingIndicator();
        console.error('Ошибка:', error);
        const errorTime = getCurrentTime();
        addMessageToChat('LandarevAI', 'Извините, произошла ошибка. Попробуйте позже.', errorTime, false);
    } finally {
        sendButton.disabled = false;
        messageInput.disabled = false;
        // Возвращаем иконку отправки
        sendButton.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="19" x2="12" y2="5"></line>
                <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
        `;
        messageInput.focus();
    }
}

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !messageInput.disabled) {
        e.preventDefault();
        sendMessage();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    messageInput.focus();
    if (chatWindow.children.length > 0) {
        switchToChatMode();
        isFirstMessage = false;
    }
});