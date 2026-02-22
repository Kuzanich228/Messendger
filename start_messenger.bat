@echo off
title Simple Test Server - Максимально простой
color 0A
echo.
echo [TEST] Simple Test Server - Максимально простой
echo ================================================
echo.
echo [PURPOSE] Для отладки проблем с подключением Android
echo [DEBUG] Подробное логирование всех событий
echo [SIMPLE] Максимально простой код
echo.
echo [INSTRUCTIONS] Что делать:
echo    1. Запустите этот сервер
echo    2. Введите в Android приложении IP с экрана
echo    3. Нажмите Connect в приложении
echo    4. Смотрите логи на экране
echo.
echo [STOP] Для остановки нажмите Ctrl+C
echo ================================================
echo.

python simple_test_server.py

echo.
echo [EXIT] Тестовый сервер остановлен. Нажмите Enter для выхода...
pause >nul
