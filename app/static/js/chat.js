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

// --- НОВЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ С БД ---

// Сохраняет сообщение в БД через POST /chat/
async function saveMessageToDB(text, roleName) {
    const response = await fetch('/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: text,
            role_name: roleName
        })
    });
    if (!response.ok) {
        throw new Error(`Ошибка сохранения сообщения: ${response.status}`);
    }
    return await response.json();
}

// --- ОСТАВЛЯЕМ ВЫЗОВ AI ---

async function sendMessageToAI(text) {
    const response = await fetch(`/api/v1/ai/?message=${encodeURIComponent(text)}`);
    if (!response.ok) {
        throw new Error(`Ошибка AI: ${response.status}`);
    }
    const data = await response.json();
    return data.message;
}

// --- ПЕРЕДЕЛАННАЯ ОСНОВНАЯ ФУНКЦИЯ ---

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

    // Блокируем интерфейс
    sendButton.disabled = true;
    messageInput.disabled = true;
    sendButton.innerHTML = `<span style="font-size:12px;font-weight:600;">...</span>`;

    const userTime = getCurrentTime();

    try {
        // 1. Сохраняем сообщение пользователя в БД
        await saveMessageToDB(text, username);
        // 2. Отображаем его в чате
        addMessageToChat(username, text, userTime, false);
        messageInput.value = '';

        // 3. Получаем ответ от AI
        showTypingIndicator();
        const aiResponse = await sendMessageToAI(text);
        removeTypingIndicator();

        // 4. Сохраняем ответ AI в БД
        await saveMessageToDB(aiResponse, 'LandarevAI');
        // 5. Отображаем ответ AI
        const aiTime = getCurrentTime();
        addMessageToChat('LandarevAI', aiResponse, aiTime, true);

    } catch (error) {
        removeTypingIndicator();
        console.error('Ошибка:', error);
        const errorTime = getCurrentTime();
        // Показываем сообщение об ошибке (без сохранения)
        addMessageToChat('LandarevAI', 'Извините, произошла ошибка. Попробуйте позже.', errorTime, false);
    } finally {
        // Разблокируем интерфейс
        sendButton.disabled = false;
        messageInput.disabled = false;
        sendButton.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="19" x2="12" y2="5"></line>
                <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
        `;
        messageInput.focus();
    }
}

// Обработчики событий (без изменений)
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

// --- Функция удаления всех сообщений ---
async function deleteAllMessages() {
    // Подтверждение
    if (!confirm('Вы уверены, что хотите удалить всю историю чата?')) {
        return;
    }

    try {
        const response = await fetch('/chat/', {
            method: 'DELETE'
        });
        if (!response.ok) {
            throw new Error(`Ошибка удаления: ${response.status}`);
        }
        // Успешно – очищаем DOM
        // Удаляем все сообщения и индикатор печати
        const messages = chatWindow.querySelectorAll('.message');
        messages.forEach(msg => msg.remove());
        removeTypingIndicator(); // если он висит

        // Переключаем обратно в приветственный режим
        appArea.classList.remove('chat-mode');
        isFirstMessage = true;

        // Показываем приветствие (оно скрыто в режиме чата)
        // Оно уже есть в DOM, просто скрыто через display:none в .chat-mode .welcome-content
        // Поэтому после снятия класса оно появится

    } catch (error) {
        console.error('Ошибка при очистке чата:', error);
        alert('Не удалось очистить чат. Попробуйте позже.');
    }
}

// --- Обработчик для кнопки очистки ---
document.getElementById('clearChatBtn').addEventListener('click', deleteAllMessages);