#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
АВТОМАТИЧЕСКАЯ НАСТРОЙКА PORT FORWARDING
Максимально простая настройка роутера
"""

import socket
import subprocess
import urllib.request
import requests
import json
import time
from datetime import datetime

class AutoPortForwarding:
    def __init__(self, port=8888):
        self.port = port
        self.local_ip = self.get_local_ip()
        self.public_ip = None
        self.router_ip = None
        self.router_info = {}
        
    def get_local_ip(self):
        """Получить локальный IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
            
    def get_public_ip(self):
        """Получить публичный IP"""
        try:
            ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
            return ip
        except:
            return None
            
    def find_router_ip(self):
        """Найти IP роутера"""
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if 'Default Gateway' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        gateway = parts[1].strip()
                        if gateway and gateway != '0.0.0.0':
                            return gateway
        except:
            pass
            
        # Стандартные IP роутеров
        common_ips = ['192.168.1.1', '192.168.0.1', '192.168.1.254', '192.168.0.254']
        
        for ip in common_ips:
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(1)
                result = test_socket.connect_ex((ip, 80))
                test_socket.close()
                
                if result == 0:
                    return ip
            except:
                continue
                
        return "192.168.1.1"
        
    def detect_router_model(self):
        """Определить модель роутера"""
        print("[DETECT] Определение модели роутера...")
        
        try:
            # Пытаемся получить информацию с роутера
            response = requests.get(f"http://{self.router_ip}", timeout=5)
            
            # Анализируем ответ для определения модели
            content = response.text.lower()
            
            if 'tp-link' in content:
                self.router_info = {
                    'brand': 'TP-Link',
                    'login_url': f"http://{self.router_ip}",
                    'login_field': 'password',
                    'port_forwarding_path': '/userRpm/NatPortMappingRpm.htm'
                }
            elif 'd-link' in content:
                self.router_info = {
                    'brand': 'D-Link',
                    'login_url': f"http://{self.router_ip}",
                    'login_field': 'password',
                    'port_forwarding_path': '/PortForwarding/PortForwarding.html'
                }
            elif 'asus' in content:
                self.router_info = {
                    'brand': 'ASUS',
                    'login_url': f"http://{self.router_ip}",
                    'login_field': 'login_authorization',
                    'port_forwarding_path': '/Advanced_VirtualServer_Content.asp'
                }
            elif 'netgear' in content:
                self.router_info = {
                    'brand': 'Netgear',
                    'login_url': f"http://{self.router_ip}",
                    'login_field': 'password',
                    'port_forwarding_path': '/PORT_forwarding.htm'
                }
            else:
                self.router_info = {
                    'brand': 'Unknown',
                    'login_url': f"http://{self.router_ip}",
                    'login_field': 'password',
                    'port_forwarding_path': '/port_forwarding'
                }
                
            print(f"[DETECTED] Роутер: {self.router_info['brand']}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Не удалось определить роутер: {e}")
            self.router_info = {
                'brand': 'Unknown',
                'login_url': f"http://{self.router_ip}",
                'login_field': 'password',
                'port_forwarding_path': '/port_forwarding'
            }
            return False
            
    def auto_setup_upnp(self):
        """Автоматическая настройка через UPnP"""
        print("[UPNP] Пробую автоматическую настройку через UPnP...")
        
        try:
            # Используем miniupnpc для автоматической настройки
            import miniupnpc
            
            upnp = miniupnpc.UPnP()
            upnp.discover()
            upnp.selectigd()
            
            # Добавляем порт
            result = upnp.addportmapping(
                self.port,
                'TCP',
                self.local_ip,
                self.port,
                'AndroidChatServer',
                ''
            )
            
            if result:
                print(f"[UPNP_SUCCESS] Порт {self.port} добавлен через UPnP")
                return True
            else:
                print("[UPNP_FAIL] UPnP не сработал")
                return False
                
        except ImportError:
            print("[UPNP_INFO] Библиотека miniupnpc не установлена")
            print("[UPNP_INFO] Установите: pip install miniupnpc")
            return False
        except Exception as e:
            print(f"[UPNP_ERROR] Ошибка UPnP: {e}")
            return False
            
    def auto_setup_natpmp(self):
        """Автоматическая настройка через NAT-PMP"""
        print("[NATPMP] Пробую автоматическую настройку через NAT-PMP...")
        
        try:
            # Используем natpmp для автоматической настройки
            import natpmp
            
            nat = natpmp.NATPMP()
            nat.init()
            
            # Добавляем порт
            result = nat.request_port_mapping(
                self.port,
                self.port,
                natpmp.NATPMP_PROTOCOL_TCP,
                3600  # 1 час
            )
            
            if result:
                print(f"[NATPMP_SUCCESS] Порт {self.port} добавлен через NAT-PMP")
                return True
            else:
                print("[NATPMP_FAIL] NAT-PMP не сработал")
                return False
                
        except ImportError:
            print("[NATPMP_INFO] Библиотека natpmp не установлена")
            print("[NATPMP_INFO] Установите: pip install natpmp")
            return False
        except Exception as e:
            print(f"[NATPMP_ERROR] Ошибка NAT-PMP: {e}")
            return False
            
    def setup_firewall(self):
        """Автоматическая настройка файрвола"""
        print("[FIREWALL] Автоматическая настройка файрвола...")
        
        try:
            # Проверяем права администратора
            result = subprocess.run(['net', 'session'], capture_output=True, text=True)
            if result.returncode != 0:
                print("[FIREWALL_ADMIN] Требуются права администратора!")
                return False
            
            # Удаляем старое правило
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 
                          'name="AndroidChatServer"'], capture_output=True)
            
            # Добавляем новое правило
            cmd = f'netsh advfirewall firewall add rule name="AndroidChatServer" dir=in action=allow protocol=TCP localport={self.port}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[FIREWALL_OK] Порт {self.port} добавлен в файрвол")
                return True
            else:
                print(f"[FIREWALL_ERROR] Ошибка добавления порта")
                return False
                
        except Exception as e:
            print(f"[FIREWALL_ERROR] Ошибка настройки файрвола: {e}")
            return False
            
    def test_port_forwarding(self):
        """Тест Port Forwarding"""
        print("[TEST] Тест Port Forwarding...")
        
        # Тест локального подключения
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(5)
            result = test_socket.connect_ex((self.local_ip, self.port))
            test_socket.close()
            
            if result != 0:
                print("[TEST_FAIL] Локальное подключение не работает")
                return False
        except:
            print("[TEST_FAIL] Ошибка локального теста")
            return False
        
        # Тест внешнего подключения
        if self.public_ip:
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(10)
                result = test_socket.connect_ex((self.public_ip, self.port))
                test_socket.close()
                
                if result == 0:
                    print("[TEST_SUCCESS] Внешнее подключение работает!")
                    return True
                else:
                    print("[TEST_FAIL] Внешнее подключение не работает")
                    return False
            except:
                print("[TEST_FAIL] Ошибка внешнего теста")
                return False
                
        return False
        
    def auto_setup_all(self):
        """Полная автоматическая настройка"""
        print("="*70)
        print("[AUTO] АВТОМАТИЧЕСКАЯ НАСТРОЙКА PORT FORWARDING")
        print("="*70)
        
        # Получаем информацию
        self.public_ip = self.get_public_ip()
        self.router_ip = self.find_router_ip()
        
        print(f"[INFO] Информация о сети:")
        print(f"   Локальный IP: {self.local_ip}")
        print(f"   Публичный IP: {self.public_ip}")
        print(f"   IP роутера: {self.router_ip}")
        print(f"   Порт: {self.port}")
        print()
        
        # Шаг 1: Настройка файрвола
        print("[STEP1] Настройка файрвола Windows")
        firewall_ok = self.setup_firewall()
        print()
        
        # Шаг 2: Определение роутера
        print("[STEP2] Определение модели роутера")
        self.detect_router_model()
        print()
        
        # Шаг 3: Автоматическая настройка UPnP
        print("[STEP3] Автоматическая настройка UPnP")
        upnp_ok = self.auto_setup_upnp()
        print()
        
        # Шаг 4: Автоматическая настройка NAT-PMP
        print("[STEP4] Автоматическая настройка NAT-PMP")
        natpmp_ok = self.auto_setup_natpmp()
        print()
        
        # Шаг 5: Тест
        print("[STEP5] Тест подключения")
        time.sleep(2)  # Даем время на настройку
        
        if self.test_port_forwarding():
            print("="*70)
            print("[SUCCESS] ✅ Port Forwarding настроен АВТОМАТИЧЕСКИ!")
            print("="*70)
            print(f"[ANDROID] Настройки для Android:")
            print(f"   IP адрес: {self.public_ip}")
            print(f"   Порт: {self.port}")
            print(f"   Адрес: {self.public_ip}:{self.port}")
            print("="*70)
            return True
        else:
            print("="*70)
            print("[AUTO_FAIL] ❌ Автоматическая настройка не сработала")
            print("="*70)
            print("[MANUAL] Требуется ручная настройка:")
            print(f"   1. Откройте: {self.router_info['login_url']}")
            print(f"   2. Логин: admin, Пароль: admin/password")
            print(f"   3. Найдите: Port Forwarding")
            print(f"   4. Создайте правило:")
            print(f"      - Имя: AndroidChatServer")
            print(f"      - Внешний порт: {self.port}")
            print(f"      - Внутренний порт: {self.port}")
            print(f"      - Внутренний IP: {self.local_ip}")
            print(f"      - Протокол: TCP")
            print("="*70)
            return False

def main():
    print("[AUTO_PORT_FORWARDING] Автоматическая настройка")
    print("="*50)
    
    auto = AutoPortForwarding(port=8888)
    
    # Проверяем права администратора
    try:
        result = subprocess.run(['net', 'session'], capture_output=True, text=True)
        if result.returncode != 0:
            print("[ADMIN] Требуются права администратора!")
            print("[ADMIN] Запустите от имени администратора")
            input("Нажмите Enter для выхода...")
            return
    except:
        pass
    
    # Запускаем автоматическую настройку
    success = auto.auto_setup_all()
    
    if not success:
        print("\n[RETRY] Хотите попробовать еще раз? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            auto.auto_setup_all()
    
    print("\n[EXIT] Нажмите Enter для выхода...")
    input()

if __name__ == "__main__":
    main()
