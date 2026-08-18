// ============================================================
// 1. DOM-ссылки и состояние
// ============================================================
const chatWindow = document.getElementById('chatWindow');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const appArea = document.getElementById('appArea');

const settingsBtn = document.getElementById('settingsBtn');
const settingsPopover = document.getElementById('settingsPopover');
const modelListContainer = document.getElementById('modelListContainer');
const closeSettingsBtn = document.getElementById('closeSettings');
const currentModelIdInput = document.getElementById('currentModelId');
const modelDisplaySpan = document.getElementById('modelDisplay');

let typingIndicator = null;
let isFirstMessage = true;
const currentChatId = parseInt(chatWindow.dataset.chatId) || null;
let currentModelId = currentModelIdInput ? parseInt(currentModelIdInput.value) || null : null;

// ============================================================
// 2. Вспомогательные утилиты
// ============================================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getCurrentTime() {
    const now = new Date();
    return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
}

function renderMarkdown(text) {
    if (typeof marked !== 'undefined' && marked.parse) {
        marked.setOptions({ breaks: true, gfm: true, sanitize: false });
        return marked.parse(text);
    }
    return text; // fallback
}

// ============================================================
// 3. Отображение сообщений и индикатора печати
// ============================================================
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
    textDiv.innerHTML = isMarkdown ? renderMarkdown(text) : escapeHtml(text);

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(textDiv);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showTypingIndicator() {
    removeTypingIndicator();
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = `
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
        <span class="typing-label">LandarevAI печатает...</span>
    `;
    chatWindow.appendChild(indicator);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    typingIndicator = indicator;
}

function removeTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.remove();
        typingIndicator = null;
    }
}

// Показ ошибки в чате (без редиректа)
function showErrorMessage(text) {
    addMessageToChat('LandarevAI', `❌ ${text}`, getCurrentTime(), false);
}

// ============================================================
// 4. API-запросы
// ============================================================
async function saveMessageToDB(text, roleName) {
    try {
        const response = await fetch(`/chat/api/${currentChatId}/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, role_name: roleName })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('saveMessageToDB error:', error);
        showErrorMessage('Не удалось сохранить сообщение. Попробуйте позже.');
        throw error;
    }
}

async function sendMessageToAI(text) {
    try {
        // Новый эндпоинт: POST /api/v1/ai/chat/{chatId}/message
        const response = await fetch(`/api/v1/ai/chat/${currentChatId}/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        return data.message;
    } catch (error) {
        console.error('sendMessageToAI error:', error);
        showErrorMessage('Ошибка при получении ответа от AI. Попробуйте ещё раз.');
        throw error;
    }
}

async function generateChatTitle(firstMessage) {
    try {
        const response = await fetch('/api/v1/ai/generate-title', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                messages: [{ role: 'user', content: firstMessage }],
                chat_id: currentChatId
            })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        const title = data.title || 'Новый чат';

        const updateResp = await fetch(`/chat/api/${currentChatId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: chatName, model_id: modelId })
        });
        if (!updateResp.ok) throw new Error(`HTTP ${updateResp.status}`);
        // Обновляем название на странице без перезагрузки
        const nameSpan = document.getElementById('currentChatName');
        if (nameSpan) nameSpan.textContent = title;
        // Обновляем ссылку в сайдбаре
        const activeItem = document.querySelector('.sidebar-content .chat-item.active .chat-link');
        if (activeItem) activeItem.textContent = title;
    } catch (error) {
        console.error('generateChatTitle error:', error);
        // Не критично, просто логируем
    }
}

// ============================================================
// 5. Загрузка моделей и выбор
// ============================================================
async function loadModels() {
    try {
        const response = await fetch('/api/v1/ai/ai-model');
        if (!response.ok) throw new Error('Failed to load models');
        const models = await response.json();
        return models;
    } catch (error) {
        console.error('loadModels error:', error);
        return [];
    }
}

function renderModelList(models, selectedId) {
    if (!modelListContainer) return;
    modelListContainer.innerHTML = '';
    if (models.length === 0) {
        modelListContainer.innerHTML = '<p style="color:rgba(255,255,255,0.5);">Нет доступных моделей</p>';
        return;
    }
    models.forEach(model => {
        const div = document.createElement('div');
        div.className = 'model-option';
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'ai_model';
        radio.value = model.id;
        radio.id = `model_${model.id}`;
        if (selectedId === model.id) radio.checked = true;
        // При выборе сразу отправляем на сервер
        radio.addEventListener('change', function() {
            if (this.checked) {
                selectModel(model.id);
            }
        });
        const label = document.createElement('label');
        label.htmlFor = `model_${model.id}`;
        label.textContent = model.url; // или model.name, если есть
        div.appendChild(radio);
        div.appendChild(label);
        modelListContainer.appendChild(div);
    });
}

async function selectModel(modelId) {
    if (!currentChatId) {
        alert('Сначала создайте чат');
        return;
    }
    try {
        // Получаем текущее имя чата
        const nameSpan = document.getElementById('currentChatName');
        const chatName = nameSpan ? nameSpan.textContent : 'Новый чат';
        const response = await fetch(`/chat/api/${currentChatId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: chatName, model_id: modelId })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        // Обновляем текущий model_id
        currentModelId = modelId;
        // Обновляем отображение модели в интерфейсе
        updateModelDisplay(modelId);
        // Закрываем popover
        settingsPopover.classList.remove('open');
        // Перезагружаем страницу, чтобы обновить все данные (простой способ)
        window.location.reload();
    } catch (error) {
        console.error('selectModel error:', error);
        alert('Не удалось изменить модель');
    }
}

function updateModelDisplay(modelId) {
    // Поскольку мы перезагружаем страницу, это не нужно, но оставим для возможного будущего
    if (modelDisplaySpan) {
        // Можно найти URL модели, но проще перезагрузить
    }
}

// ============================================================
// 6. Переключение режима чата
// ============================================================
function switchToChatMode() {
    if (!appArea.classList.contains('chat-mode')) {
        appArea.classList.add('chat-mode');
        setTimeout(() => chatWindow.scrollTop = chatWindow.scrollHeight, 50);
    }
}

// ============================================================
// 7. Основная отправка сообщения
// ============================================================
async function sendMessage() {
    const text = messageInput.value.trim();
    const username = localStorage.getItem('username') || 'Пользователь';

    if (!text) {
        messageInput.focus();
        messageInput.style.borderColor = '#ef4444';
        setTimeout(() => messageInput.style.borderColor = 'transparent', 1000);
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
        // Сохраняем сообщение пользователя
        await saveMessageToDB(text, username);
        addMessageToChat(username, text, userTime, false);
        messageInput.value = '';

        // Получаем ответ AI
        showTypingIndicator();
        const aiResponse = await sendMessageToAI(text);
        removeTypingIndicator();

        // Сохраняем и показываем ответ AI
        await saveMessageToDB(aiResponse, 'LandarevAI');
        const aiTime = getCurrentTime();
        addMessageToChat('LandarevAI', aiResponse, aiTime, true);

        // Если чат новый, генерируем название
        const chatNameSpan = document.getElementById('currentChatName');
        if (chatNameSpan && chatNameSpan.textContent === 'Новый чат') {
            await generateChatTitle(text);
        }
    } catch (error) {
        removeTypingIndicator();
        // Ошибка уже показана в showErrorMessage, дополнительно логируем
        console.error('sendMessage error:', error);
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

// ============================================================
// 8. Обработчики событий (ввод, кнопки)
// ============================================================
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !messageInput.disabled) {
        e.preventDefault();
        sendMessage();
    }
});

// При загрузке – фокус и переключение режима, если есть сообщения
document.addEventListener('DOMContentLoaded', () => {
    messageInput.focus();
    if (chatWindow.children.length > 0) {
        switchToChatMode();
        isFirstMessage = false;
    }
    // Обновить отображение модели, если есть
    if (currentModelId && modelDisplaySpan) {
        // Можно загрузить название модели, но пока оставим как есть
    }
});

// ============================================================
// 9. Управление чатами (тулбар, сайдбар)
// ============================================================
let isCreatingChat = false;

document.getElementById('newChatBtn').addEventListener('click', async () => {
    if (isCreatingChat) return;
    const messages = chatWindow.querySelectorAll('.message');
    if (messages.length === 0) return;

    isCreatingChat = true;
    const btn = document.getElementById('newChatBtn');
    btn.style.opacity = '0.5';
    btn.disabled = true;

    try {
        const resp = await fetch('/chat/api/', { method: 'POST' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        if (data && typeof data.id === 'number') {
            window.location.href = `/chat?chat_id=${data.id}`;
        } else {
            throw new Error('Invalid response');
        }
    } catch (error) {
        console.error('create chat error:', error);
        showErrorMessage('Не удалось создать чат.');
    } finally {
        isCreatingChat = false;
        btn.style.opacity = '1';
        btn.disabled = false;
    }
});

document.getElementById('deleteAllChatsBtn').addEventListener('click', async () => {
    if (!confirm('Удалить все чаты?')) return;
    try {
        const resp = await fetch('/chat/api/', { method: 'DELETE' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        window.location.href = '/chat';
    } catch (error) {
        console.error('delete all chats error:', error);
        showErrorMessage('Не удалось удалить чаты.');
    }
});

document.getElementById('chatListToggle').addEventListener('click', () => {
    document.getElementById('chatSidebar').classList.toggle('open');
});
document.getElementById('closeSidebar').addEventListener('click', () => {
    document.getElementById('chatSidebar').classList.remove('open');
});

document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('chatSidebar');
    const toggle = document.getElementById('chatListToggle');
    if (sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

// Удаление отдельного чата (делегирование)
document.getElementById('chatList').addEventListener('click', async (e) => {
    const deleteBtn = e.target.closest('.delete-chat-btn');
    if (!deleteBtn) return;
    e.stopPropagation();
    e.preventDefault();

    const chatId = parseInt(deleteBtn.dataset.chatId);
    if (!chatId) return;
    if (!confirm('Удалить этот чат?')) return;

    try {
        const resp = await fetch(`/chat/api/${chatId}`, { method: 'DELETE' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        window.location.href = (currentChatId === chatId) ? '/chat' : window.location.href;
    } catch (error) {
        console.error('delete chat error:', error);
        showErrorMessage('Не удалось удалить чат.');
    }
});

// ============================================================
// 10. Настройки – popover
// ============================================================
settingsBtn.addEventListener('click', async () => {
    if (settingsPopover.classList.contains('open')) {
        settingsPopover.classList.remove('open');
        return;
    }
    // Загружаем список моделей
    const models = await loadModels();
    renderModelList(models, currentModelId);
    settingsPopover.classList.add('open');
});

closeSettingsBtn.addEventListener('click', () => {
    settingsPopover.classList.remove('open');
});

// Закрыть по клику вне
document.addEventListener('click', (e) => {
    if (settingsPopover.classList.contains('open') &&
        !settingsPopover.contains(e.target) &&
        !settingsBtn.contains(e.target)) {
        settingsPopover.classList.remove('open');
    }
});