#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка поддержки WiFi Direct на PC
Простая проверка возможностей
"""

import subprocess
import platform
import socket
import sys
from datetime import datetime

class WiFiDirectChecker:
    def __init__(self):
        self.system = platform.system()
        self.wifi_adapters = []
        self.wifi_direct_support = False
        self.hosted_network_support = False
        
    def check_system_info(self):
        """Проверить информацию о системе"""
        print("[SYSTEM] Информация о системе:")
        print(f"   ОС: {self.system}")
        print(f"   Python: {sys.version}")
        print()
        
    def check_wifi_adapters(self):
        """Проверить WiFi адаптеры"""
        print("[WIFI] Проверка WiFi адаптеров...")
        
        try:
            if self.system == "Windows":
                result = subprocess.run(['netsh', 'wlan', 'show', 'drivers'], 
                                   capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'Interface name' in line or 'Имя интерфейса' in line:
                            adapter = line.split(':')[1].strip() if ':' in line else ''
                            if adapter:
                                self.wifi_adapters.append(adapter)
                                
                if self.wifi_adapters:
                    print(f"[OK] Найдено WiFi адаптеров: {len(self.wifi_adapters)}")
                    for i, adapter in enumerate(self.wifi_adapters, 1):
                        print(f"   {i}. {adapter}")
                else:
                    print("[FAIL] WiFi адаптеры не найдены")
                    
            elif self.system == "Linux":
                result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'wlan' in line and 'no wireless extensions' not in line.lower():
                            adapter = line.split()[0]
                            self.wifi_adapters.append(adapter)
                            
                if self.wifi_adapters:
                    print(f"[OK] Найдено WiFi адаптеров: {len(self.wifi_adapters)}")
                    for i, adapter in enumerate(self.wifi_adapters, 1):
                        print(f"   {i}. {adapter}")
                else:
                    print("[FAIL] WiFi адаптеры не найдены")
                    
            elif self.system == "Darwin":  # macOS
                result = subprocess.run(['networksetup', '-listallhardwareports'], 
                                   capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'Wi-Fi' in line or 'AirPort' in line:
                            adapter = line.split(':')[1].strip() if ':' in line else ''
                            if adapter:
                                self.wifi_adapters.append(adapter)
                                
                if self.wifi_adapters:
                    print(f"[OK] Найдено WiFi адаптеров: {len(self.wifi_adapters)}")
                    for i, adapter in enumerate(self.wifi_adapters, 1):
                        print(f"   {i}. {adapter}")
                else:
                    print("[FAIL] WiFi адаптеры не найдены")
                    
        except Exception as e:
            print(f"[ERROR] Ошибка проверки WiFi адаптеров: {e}")
            
        print()
        
    def check_hosted_network_support(self):
        """Проверить поддержку размещенной сети"""
        print("[HOSTED_NETWORK] Проверка поддержки размещенной сети...")
        
        if self.system != "Windows":
            print("[INFO] Проверка размещенной сети доступна только для Windows")
            self.hosted_network_support = False
            print()
            return
            
        try:
            # Проверяем поддержку размещенной сети
            result = subprocess.run(['netsh', 'wlan', 'show', 'settings'], 
                               capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Размещенная сеть' in line or 'Hosted network' in line:
                        if 'Разрешено' in line or 'Allowed' in line:
                            self.hosted_network_support = True
                            print("[OK] Размещенная сеть поддерживается")
                            break
                        elif 'Запрещено' in line or 'Disallowed' in line:
                            self.hosted_network_support = False
                            print("[FAIL] Размещенная сеть запрещена")
                            break
                            
                if self.hosted_network_support:
                    # Проверяем драйвер
                    result = subprocess.run(['netsh', 'wlan', 'show', 'drivers'], 
                                       capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if 'Размещенная сеть' in line or 'Hosted network' in line:
                                if 'Да' in line or 'Yes' in line:
                                    print("[OK] Драйвер поддерживает размещенную сеть")
                                    break
                                elif 'Нет' in line or 'No' in line:
                                    print("[FAIL] Драйвер не поддерживает размещенную сеть")
                                    self.hosted_network_support = False
                                    break
                else:
                    print("[FAIL] Размещенная сеть не поддерживается системой")
            else:
                print("[FAIL] Не удалось проверить настройки WLAN")
                
        except Exception as e:
            print(f"[ERROR] Ошибка проверки размещенной сети: {e}")
            
        print()
        
    def check_wifi_direct_libraries(self):
        """Проверить доступные библиотеки для WiFi Direct"""
        print("[LIBRARIES] Проверка библиотек WiFi Direct...")
        
        libraries = {
            'pywifi': 'Библиотека для управления WiFi',
            'wifi': 'Простая библиотека WiFi',
            'subprocess': 'Системные команды',
            'socket': 'Сетевые возможности'
        }
        
        available_libs = []
        unavailable_libs = []
        
        for lib_name, description in libraries.items():
            try:
                if lib_name == 'subprocess' or lib_name == 'socket':
                    # Встроенные модули
                    available_libs.append((lib_name, description))
                    print(f"[OK] {lib_name}: {description}")
                else:
                    # Внешние библиотеки
                    __import__(lib_name)
                    available_libs.append((lib_name, description))
                    print(f"[OK] {lib_name}: {description}")
            except ImportError:
                unavailable_libs.append((lib_name, description))
                print(f"[MISSING] {lib_name}: {description}")
                
        print()
        return available_libs, unavailable_libs
        
    def test_wifi_capabilities(self):
        """Тест WiFi возможностей"""
        print("[CAPABILITIES] Тест WiFi возможностей...")
        
        if self.system == "Windows":
            try:
                # Проверяем состояние WiFi
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                   capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'State' in line or 'Состояние' in line:
                            if 'connected' in line.lower() or 'подключено' in line.lower():
                                print("[OK] WiFi подключен и активен")
                                break
                    else:
                        print("[WARN] WiFi не подключен")
                        
                # Проверяем возможность сканирования
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], 
                                   capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("[OK] Сканирование WiFi сетей работает")
                else:
                    print("[FAIL] Сканирование WiFi сетей не работает")
                    
            except Exception as e:
                print(f"[ERROR] Ошибка теста WiFi: {e}")
                
        print()
        
    def check_wifi_direct_support(self):
        """Проверить поддержку WiFi Direct"""
        print("[WIFI_DIRECT] Проверка поддержки WiFi Direct...")
        
        # WiFi Direct поддерживается если:
        # 1. Есть WiFi адаптер
        # 2. Поддерживается размещенная сеть (Windows)
        # 3. Есть необходимые библиотеки
        
        if not self.wifi_adapters:
            print("[FAIL] WiFi Direct не поддерживается: нет WiFi адаптеров")
            self.wifi_direct_support = False
        elif self.system == "Windows" and not self.hosted_network_support:
            print("[FAIL] WiFi Direct не поддерживается: запрещена размещенная сеть")
            self.wifi_direct_support = False
        else:
            print("[OK] WiFi Direct поддерживается!")
            self.wifi_direct_support = True
            
            # Дополнительная информация
            if self.system == "Windows":
                print("[INFO] Можно использовать размещенную сеть (Hosted Network)")
                print("[INFO] Точка доступа будет создана автоматически")
            else:
                print("[INFO] Требуется дополнительная настройка")
                
        print()
        
    def show_summary(self):
        """Показать итоговую информацию"""
        print("=" * 60)
        print("[SUMMARY] ИТОГОВАЯ ИНФОРМАЦИЯ")
        print("=" * 60)
        
        print(f"[WIFI_ADAPTERS] WiFi адаптеры: {len(self.wifi_adapters)}")
        for adapter in self.wifi_adapters:
            print(f"   - {adapter}")
            
        if self.system == "Windows":
            print(f"[HOSTED_NETWORK] Размещенная сеть: {'Поддерживается' if self.hosted_network_support else 'Не поддерживается'}")
            
        print(f"[WIFI_DIRECT] WiFi Direct: {'Поддерживается' if self.wifi_direct_support else 'Не поддерживается'}")
        print()
        
        if self.wifi_direct_support:
            print("[SUCCESS] ✅ WiFi Direct можно использовать!")
            print()
            print("[NEXT] Что дальше:")
            print("   1. Можно создать точку доступа")
            print("   2. Android подключится как к обычному WiFi")
            print("   3. Наш сервер будет работать через WiFi Direct")
            print()
            print("[RECOMMENDATION] Рекомендация:")
            print("   Используйте размещенную сеть (Hosted Network)")
            print("   Это самый простой способ WiFi Direct")
        else:
            print("[FAIL] ❌ WiFi Direct не поддерживается")
            print()
            print("[ALTERNATIVES] Альтернативы:")
            print("   1. Использовать обычный WiFi роутер")
            print("   2. Использовать ngrok для интернета")
            print("   3. Использовать кабельное подключение")
            
        print("=" * 60)
        
    def run_full_check(self):
        """Запустить полную проверку"""
        print("[WIFI_DIRECT_CHECKER] Проверка поддержки WiFi Direct")
        print("=" * 60)
        print(f"[TIME] Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Пошаговая проверка
        self.check_system_info()
        self.check_wifi_adapters()
        self.check_hosted_network_support()
        self.check_wifi_direct_libraries()
        self.test_wifi_capabilities()
        self.check_wifi_direct_support()
        self.show_summary()

def main():
    print("[WIFI_DIRECT_CHECKER] Проверка WiFi Direct")
    print("=" * 50)
    
    checker = WiFiDirectChecker()
    checker.run_full_check()
    
    print("\n[EXIT] Нажмите Enter для выхода...")
    input()

if __name__ == "__main__":
    main()
