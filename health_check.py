#!/usr/bin/env python3
"""
Простой веб-сервер для health check Railway
"""
from flask import Flask, jsonify
import threading
import time
import logging
import os

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Глобальная переменная для отслеживания состояния
system_status = {
    "status": "running",
    "uptime": 0,
    "last_check": None
}

@app.route('/health')
def health_check():
    """Health check endpoint для Railway"""
    return jsonify({
        "status": "healthy",
        "service": "telegram-automation",
        "uptime": system_status["uptime"],
        "last_check": system_status["last_check"]
    })

@app.route('/')
def index():
    """Главная страница"""
    return jsonify({
        "service": "Telegram Automation Bot",
        "status": "running",
        "endpoints": ["/health"]
    })

def update_status():
    """Обновляет статус системы"""
    global system_status
    start_time = time.time()
    
    while True:
        system_status["uptime"] = int(time.time() - start_time)
        system_status["last_check"] = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(60)  # Обновляем каждую минуту

def run_health_server():
    """Запускает веб-сервер для health check"""
    try:
        logger.info("Запуск health check сервера...")
        # Запускаем обновление статуса в отдельном потоке
        status_thread = threading.Thread(target=update_status)
        status_thread.daemon = True
        status_thread.start()
        
        # Запускаем Flask сервер
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
    except Exception as e:
        logger.error(f"Ошибка запуска health check сервера: {e}")

if __name__ == "__main__":
    import os
    run_health_server()
