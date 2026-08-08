(function() {
    'use strict';

    const urlParams = new URLSearchParams(window.location.search);
    const errorCode = urlParams.get('code') || '500';

    const codeElement = document.getElementById('errorCode');
    const messageElement = document.getElementById('errorMessage');

    const errorMap = {
        '400': { code: 'Ошибка 400', msg: 'Неверный запрос. Проверьте введённые данные.' },
        '401': { code: 'Ошибка 401', msg: 'Требуется авторизация. Пожалуйста, войдите в систему.' },
        '403': { code: 'Ошибка 403', msg: 'Доступ запрещён. У вас недостаточно прав.' },
        '404': { code: 'Ошибка 404', msg: 'Страница не найдена. Возможно, она была удалена.' },
        '500': { code: 'Ошибка 500', msg: 'Внутренняя ошибка сервера. <code>LandarevAI</code> временно недоступен.' },
        '502': { code: 'Ошибка 502', msg: 'Плохой шлюз. Проблемы с сетевым соединением.' },
        '503': { code: 'Ошибка 503', msg: 'Сервис временно недоступен. Попробуйте позже.' },
        '504': { code: 'Ошибка 504', msg: 'Время ожидания истекло. Сервер не отвечает.' },
    };

    const selected = errorMap[errorCode] || errorMap['500'];
    if (codeElement) codeElement.textContent = selected.code;
    if (messageElement) messageElement.innerHTML = selected.msg;

    let counter = 30;
    const statusSpan = document.querySelector('.error-hint span:first-child span:last-child');
    if (statusSpan) {
        statusSpan.textContent = `перезагрузка через ${counter}с`;
        const interval = setInterval(() => {
            counter -= 1;
            statusSpan.textContent = `перезагрузка через ${counter}с`;
            if (counter <= 0) {
                clearInterval(interval);
                statusSpan.textContent = 'обновление...';
                // Имитация перезагрузки (просто перезагружаем страницу)
                window.location.reload();
            }
        }, 1000);
    }
    const tsElement = document.getElementById('timestamp');
    if (tsElement) {
        function updateTime() {
            const now = new Date();
            const timeStr = now.getHours().toString().padStart(2, '0') + ':' +
                           now.getMinutes().toString().padStart(2, '0') + ':' +
                           now.getSeconds().toString().padStart(2, '0');
            tsElement.textContent = timeStr;
        }
        updateTime();
        setInterval(updateTime, 1000);
    }

    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', (e) => {
            e.preventDefault();
            // Эффект нажатия
            refreshBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                refreshBtn.style.transform = '';
                window.location.href = '/';
            }, 200);
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.shiftKey && e.key === 'E') {
            const codes = ['400','401','403','404','500','502','503','504'];
            const current = errorCode;
            let idx = codes.indexOf(current);
            if (idx === -1) idx = 4; // 500
            const next = codes[(idx + 1) % codes.length];
            window.location.href = `?code=${next}`;
        }
    });

    console.log('✨ LandarevAI — страница ошибки (динамическая)');
})();