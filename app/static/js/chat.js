const chatWindow = document.getElementById('chatWindow');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const appArea = document.getElementById('appArea');

let typingIndicator = null;
let isFirstMessage = true;

// Получаем ID текущего чата из data-атрибута
let currentChatId = parseInt(chatWindow.dataset.chatId) || null;

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

// --- Сохранение сообщения в БД (привязка к текущему чату) ---
async function saveMessageToDB(text, roleName) {
    try {
        const response = await fetch(`/chat/api/${currentChatId}/message`, {
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
    } catch (error) {
        console.error('Ошибка saveMessageToDB:', error);
        window.location.href = '/error?code=500';
    }
}

// --- Отправка запроса к AI ---
async function sendMessageToAI(text) {
    try {
        const response = await fetch(`/api/v1/ai/?message=${encodeURIComponent(text)}`);
        if (!response.ok) {
            throw new Error(`Ошибка AI: ${response.status}`);
        }
        const data = await response.json();
        return data.message;
    } catch (error) {
        console.error('Ошибка sendMessageToAI:', error);
        window.location.href = '/error?code=500';
    }
}

// --- Генерация названия чата через AI (новый эндпоинт) ---
async function generateChatTitle(firstMessage) {
    try {
        const response = await fetch('/api/v1/ai/generate-title', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                messages: [{role: 'user', content: firstMessage}]
            })
        });
        if (!response.ok) {
            throw new Error(`Ошибка generate-title: ${response.status}`);
        }
        const data = await response.json();
        const title = data.title || 'Новый чат';
        // Обновляем имя чата на сервере
        const updateResp = await fetch(`/chat/api/${currentChatId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: title})
        });
        if (!updateResp.ok) {
            throw new Error(`Ошибка обновления имени: ${updateResp.status}`);
        }
        // Перезагружаем страницу, чтобы обновить название в сайдбаре
        window.location.reload();
    } catch (error) {
        console.error('Ошибка generateChatTitle:', error);
        // Не редиректим на ошибку, просто игнорируем, так как это не критично
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

// --- Основная функция отправки сообщения ---
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

    sendButton.disabled = true;
    messageInput.disabled = true;
    sendButton.innerHTML = `<span style="font-size:12px;font-weight:600;">...</span>`;

    const userTime = getCurrentTime();

    try {
        // 1. Сохраняем сообщение пользователя
        await saveMessageToDB(text, username);
        addMessageToChat(username, text, userTime, false);
        messageInput.value = '';

        // 2. Получаем ответ AI
        showTypingIndicator();
        const aiResponse = await sendMessageToAI(text);
        removeTypingIndicator();

        // 3. Сохраняем ответ AI
        await saveMessageToDB(aiResponse, 'LandarevAI');
        const aiTime = getCurrentTime();
        addMessageToChat('LandarevAI', aiResponse, aiTime, true);

        // 4. Если чат новый (имя "Новый чат"), генерируем название
        const chatNameSpan = document.getElementById('currentChatName');
        if (chatNameSpan && chatNameSpan.textContent === 'Новый чат') {
            await generateChatTitle(text);
        }
    } catch (error) {
        removeTypingIndicator();
        console.error('Ошибка в sendMessage:', error);
        // Показываем сообщение об ошибке
        const errorTime = getCurrentTime();
        addMessageToChat('LandarevAI', 'Извините, произошла ошибка. Попробуйте позже.', errorTime, false);
    } finally {
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

// Обработчики отправки сообщения
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !messageInput.disabled) {
        e.preventDefault();
        sendMessage();
    }
});

// При загрузке страницы фокус и переключение режима, если есть сообщения
document.addEventListener('DOMContentLoaded', () => {
    messageInput.focus();
    if (chatWindow.children.length > 0) {
        switchToChatMode();
        isFirstMessage = false;
    }
});

// --- Управление чатами (тулбар и сайдбар) ---

// Блокировка повторного нажатия на кнопку "+"
let isCreatingChat = false;

// Кнопка "Новый чат" – создаёт только если текущий чат не пуст
document.getElementById('newChatBtn').addEventListener('click', async () => {
    // Если уже идет создание, игнорируем повторный клик
    if (isCreatingChat) return;

    // Проверяем, есть ли в текущем чате сообщения
    const messages = chatWindow.querySelectorAll('.message');
    if (messages.length === 0) {
        // Если сообщений нет, ничего не делаем (остаёмся в текущем чате)
        return;
    }

    isCreatingChat = true;
    const btn = document.getElementById('newChatBtn');
    btn.style.opacity = '0.5';
    btn.disabled = true;

    try {
        const resp = await fetch('/chat/api/', { method: 'POST' });
        if (!resp.ok) {
            throw new Error(`Ошибка создания чата: ${resp.status}`);
        }
        const data = await resp.json();
        // Проверяем наличие id
        if (data && typeof data.id === 'number') {
            window.location.href = `/chat?chat_id=${data.id}`;
        } else {
            // Если id не пришёл, редирект на ошибку
            window.location.href = '/error?code=500';
        }
    } catch (error) {
        console.error('Ошибка создания чата:', error);
        window.location.href = '/error?code=500';
    } finally {
        isCreatingChat = false;
        btn.style.opacity = '1';
        btn.disabled = false;
    }
});

// Кнопка "Удалить все чаты"
document.getElementById('deleteAllChatsBtn').addEventListener('click', async () => {
    if (!confirm('Удалить все чаты?')) return;
    try {
        const resp = await fetch('/chat/api/', { method: 'DELETE' });
        if (!resp.ok) {
            throw new Error(`Ошибка удаления: ${resp.status}`);
        }
        window.location.href = '/chat';
    } catch (error) {
        console.error('Ошибка удаления всех чатов:', error);
        window.location.href = '/error?code=500';
    }
});

// Кнопка открытия/закрытия сайдбара
document.getElementById('chatListToggle').addEventListener('click', () => {
    document.getElementById('chatSidebar').classList.toggle('open');
});
document.getElementById('closeSidebar').addEventListener('click', () => {
    document.getElementById('chatSidebar').classList.remove('open');
});

// Закрытие сайдбара при клике вне его
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('chatSidebar');
    const toggle = document.getElementById('chatListToggle');
    if (sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

// 3. Удаление отдельного чата (обработчик через делегирование событий)
document.getElementById('chatList').addEventListener('click', async (e) => {
    const deleteBtn = e.target.closest('.delete-chat-btn');
    if (!deleteBtn) return;

    // Останавливаем всплытие, чтобы не сработал переход по ссылке чата
    e.stopPropagation();
    e.preventDefault();

    const chatId = parseInt(deleteBtn.dataset.chatId);
    if (!chatId) return;

    if (!confirm('Удалить этот чат?')) return;

    try {
        const resp = await fetch(`/chat/api/${chatId}`, { method: 'DELETE' });
        if (!resp.ok) throw new Error(resp.status);

        // Если удалили текущий чат, переходим на главную (которая выберет следующий)
        if (currentChatId === chatId) {
            window.location.href = '/chat';
        } else {
            // Иначе просто перезагружаем список
            window.location.reload();
        }
    } catch (error) {
        // Любая ошибка на сервере кидает на страницу ошибки
        window.location.href = '/error?code=500';
    }
});