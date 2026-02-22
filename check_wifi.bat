@echo off
title WiFi Direct Checker - Проверка поддержки
color 0B
echo.
echo [WIFI_DIRECT] Проверка поддержки WiFi Direct
echo ============================================
echo.
echo [PURPOSE] Проверка возможностей WiFi Direct на PC:
echo    [ADAPTERS] Проверка WiFi адаптеров
echo    [HOSTED_NETWORK] Проверка размещенной сети
echo    [LIBRARIES] Проверка доступных библиотек
echo    [CAPABILITIES] Тест WiFi возможностей
echo    [SUPPORT] Итоговая поддержка WiFi Direct
echo.
echo [RESULT] Получите полную информацию о поддержке:
echo    ✅ Поддерживается ли WiFi Direct
echo    ✅ Какие адаптеры доступны
echo    ✅ Можно ли использовать точку доступа
echo    ✅ Какие библиотеки нужны
echo.
echo [START] Запускаю проверку...
echo ============================================
echo.

python wifi_direct_checker.py

echo.
echo [EXIT] Проверка завершена. Нажмите Enter для выхода...
pause >nul
