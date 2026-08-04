const chatWindow = document.getElementById('chatWindow');
const messageInput = document.getElementById('messageInput');
const usernameInput = document.getElementById('usernameInput');
const sendButton = document.getElementById('sendButton');

let typingIndicator = null;

function renderMarkdown(text) {
    if (typeof marked !== 'undefined') {
        // Настройка marked для безопасности
        marked.setOptions({
            breaks: true,  // Переносы строк в <br>
            gfm: true,     // GitHub Flavored Markdown
            sanitize: false // Не санитизировать (мы это делаем вручную)
        });
        return marked.parse(text);
    }
    // Если marked не загружен, возвращаем текст как есть
    return text;
}

// Функция для добавления сообщения в чат
function addMessageToChat(username, text, time, isMarkdown = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    if (username === 'LandarevAI') {
        messageDiv.classList.add('ai-message');
    }

    const headerDiv = document.createElement('div');
    headerDiv.className = 'message-header';
    headerDiv.innerHTML = `
        <span class="username">${escapeHtml(username)}</span>
        <span class="time">${escapeHtml(time)}</span>
    `;

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';

    // Если это Markdown - преобразуем в HTML
    if (isMarkdown) {
        try {
            // Преобразуем Markdown в HTML
            const htmlContent = renderMarkdown(text);
            textDiv.innerHTML = htmlContent;
        } catch (error) {
            console.error('Ошибка рендеринга Markdown:', error);
            textDiv.textContent = text;
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
            <span></span>
            <span></span>
            <span></span>
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
        const response = await fetch(`/api?message=${encodeURIComponent(text)}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.message;
    } catch (error) {
        console.error('Ошибка API:', error);
        throw error;
    }
}

async function sendMessage() {
    const text = messageInput.value.trim();
    const username = usernameInput.value.trim() || 'Пользователь';

    if (!text) {
        messageInput.focus();
        messageInput.style.borderColor = '#ef4444';
        setTimeout(() => {
            messageInput.style.borderColor = 'rgba(255, 255, 255, 0.06)';
        }, 1000);
        return;
    }

    sendButton.disabled = true;
    messageInput.disabled = true;
    sendButton.innerHTML = 'Отправка...';

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
        sendButton.innerHTML = `
            <span>Отправить</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
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
});