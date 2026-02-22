@echo off
title Auto Port Forwarding - Автоматическая настройка
color 0E
echo.
echo [AUTO] Автоматическая настройка Port Forwarding
echo ===============================================
echo.
echo [AUTO] АВТОМАТИЧЕСКАЯ НАСТРОЙКА:
echo    [UPNP] Автоматическая настройка через UPnP
echo    [NATPMP] Автоматическая настройка через NAT-PMP
echo    [FIREWALL] Автоматическая настройка файрвола
echo    [DETECT] Автоматическое определение роутера
echo    [TEST] Автоматический тест подключения
echo.
echo [IMPORTANT] ВАЖНО:
echo    1. Запустите от имени АДМИНИСТРАТОРА
echo    2. Убедитесь что роутер поддерживает UPnP
echo    3. Если не сработает - будет ручная инструкция
echo.
echo [START] Запускаю автоматическую настройку...
echo ===============================================
echo.

python auto_port_forwarding.py

echo.
echo [EXIT] Автоматическая настройка завершена. Нажмите Enter для выхода...
pause >nul
