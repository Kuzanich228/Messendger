#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Максимально простой сервер для тестирования подключения Android
"""

import socket
import threading
import time
import os
from datetime import datetime

class SimpleTestServer:
    def __init__(self, port=8888):
        self.port = port
        self.clients = {}
        self.server_running = False
        self.server_socket = None
        self.start_time = None
        
    def start(self):
        """Запуск сервера"""
        try:
            self.start_time = datetime.now()
            
            # Создаем сервер
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            
            self.server_running = True
            
            # Показываем информацию
            self.clear_screen()
            self.show_header()
            
            # Запускаем поток для принятия подключений
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Консоль управления
            self.start_console()
            
        except Exception as e:
            print(f"[ERROR] Ошибка запуска: {e}")
            print(f"[DEBUG] Детали: {type(e).__name__}: {e}")
            
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_header(self):
        """Показать заголовок"""
        print("[TEST] Simple Test Server - Максимально простой")
        print("=" * 60)
        print(f"[PORT] Сервер на порту: {self.port}")
        print(f"[IP] Локальный IP: {self.get_local_ip()}")
        print(f"[CLIENTS] Подключений: {len(self.clients)}")
        print("=" * 60)
        print("[ANDROID] Для подключения Android:")
        print(f"   IP: {self.get_local_ip()}")
        print(f"   Порт: {self.port}")
        print()
        print("[DEBUG] Отладочная информация:")
        print("   - Сервер слушает ВСЕ интерфейсы (0.0.0.0)")
        print("   - Порт переиспользуется (SO_REUSEADDR)")
        print("   - Таймауты отключены для стабильности")
        print("   - Логирование всех подключений")
        print("=" * 60)
        print("[COMMANDS] Команды:")
        print("   status  - показать статус")
        print("   clients - список клиентов")
        print("   test    - тест подключения")
        print("   clear   - очистить экран")
        print("   stop    - остановить сервер")
        print("   help    - показать помощь")
        print("=" * 60)
        
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
            
    def accept_connections(self):
        """Принятие подключений"""
        print(f"[LISTEN] Слушаю порт {self.port} на всех интерфейсах...")
        while self.server_running:
            try:
                # Без таймаута для максимальной совместимости
                client_socket, client_address = self.server_socket.accept()
                
                print(f"\n[CONNECT] === НОВОЕ ПОДКЛЮЧЕНИЕ ===")
                print(f"[CLIENT] IP: {client_address[0]}")
                print(f"[PORT] Порт: {client_address[1]}")
                print(f"[TIME] Время: {datetime.now().strftime('%H:%M:%S')}")
                print(f"[INFO] Всего клиентов: {len(self.clients) + 1}")
                print("=" * 40)
                
                client_id = f"{client_address[0]}:{client_address[1]}"
                
                self.clients[client_id] = {
                    'socket': client_socket,
                    'address': client_address,
                    'connected': datetime.now()
                }
                
                # Отправляем приветствие
                try:
                    welcome = f"SERVER_CONNECTED|{datetime.now().strftime('%H:%M:%S')}"
                    client_socket.send(welcome.encode())
                    print(f"[SENT] Отправлено приветствие клиенту")
                except Exception as e:
                    print(f"[ERROR] Ошибка отправки приветствия: {e}")
                
                # Запускаем обработку клиента
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address, client_id)
                )
                client_thread.daemon = True
                client_thread.start()
                    
            except Exception as e:
                if self.server_running:
                    print(f"[ERROR] Ошибка принятия подключения: {e}")
                    print(f"[DEBUG] {type(e).__name__}: {e}")
                time.sleep(0.1)
                    
    def handle_client(self, client_socket, client_address, client_id):
        """Обработка клиента"""
        print(f"[THREAD] Запущен поток для клиента {client_id}")
        
        try:
            # Главный цикл приема сообщений
            while self.server_running:
                try:
                    # Устанавливаем таймаут
                    client_socket.settimeout(30.0)
                    
                    data = client_socket.recv(1024)
                    if not data:
                        print(f"[DISCONNECT] Клиент {client_id} отключился (нет данных)")
                        break
                        
                    message = data.decode('utf-8').strip()
                    if message:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"\n[MESSAGE] === ПОЛУЧЕНО СООБЩЕНИЕ ===")
                        print(f"[FROM] Клиент: {client_id}")
                        print(f"[TIME] Время: {timestamp}")
                        print(f"[TEXT] Сообщение: {message}")
                        print("=" * 40)
                        
                        # Отправляем подтверждение
                        try:
                            response = f"RECEIVED|{timestamp}|{len(message)}"
                            client_socket.send(response.encode())
                            print(f"[SENT] Отправлено подтверждение")
                        except Exception as e:
                            print(f"[ERROR] Ошибка отправки подтверждения: {e}")
                        
                except socket.timeout:
                    print(f"[TIMEOUT] Таймаут клиента {client_id}, продолжаем...")
                    continue
                except Exception as e:
                    print(f"[ERROR] Ошибка приема от {client_id}: {e}")
                    break
                    
        except Exception as e:
            print(f"[ERROR] Ошибка обработки клиента {client_id}: {e}")
        finally:
            self.disconnect_client(client_id)
            
    def disconnect_client(self, client_id):
        """Отключение клиента"""
        if client_id in self.clients:
            client_info = self.clients[client_id]
            
            try:
                client_info['socket'].close()
                print(f"[CLOSE] Сокет клиента {client_id} закрыт")
            except Exception as e:
                print(f"[ERROR] Ошибка закрытия сокета: {e}")
                
            del self.clients[client_id]
            print(f"[DISCONNECTED] Клиент {client_id} отключен")
            print(f"[REMAINING] Осталось клиентов: {len(self.clients)}")
            
    def start_console(self):
        """Консоль управления"""
        while self.server_running:
            try:
                print()
                command = input("[CMD] Введите команду: ").strip()
                
                if command.lower() == 'stop':
                    self.stop()
                    break
                elif command.lower() == 'status':
                    self.show_status()
                elif command.lower() == 'clients':
                    self.show_clients()
                elif command.lower() == 'test':
                    self.test_connection()
                elif command.lower() == 'clear':
                    self.clear_screen()
                    self.show_header()
                elif command.lower() == 'help':
                    self.show_help()
                elif command == '':
                    continue
                else:
                    # Отправляем сообщение всем клиентам
                    self.broadcast_to_all(f"SERVER: {command}")
                    
            except KeyboardInterrupt:
                print("\n[STOP] Остановка сервера...")
                self.stop()
                break
            except EOFError:
                break
                
    def broadcast_to_all(self, message):
        """Рассылка сообщения всем клиентам"""
        print(f"[BROADCAST] Отправка сообщения: {message}")
        
        disconnected = []
        for client_id, client_info in self.clients.items():
            try:
                client_info['socket'].send(message.encode())
                print(f"[SENT] Отправлено клиенту {client_id}")
            except Exception as e:
                print(f"[ERROR] Ошибка отправки {client_id}: {e}")
                disconnected.append(client_id)
                
        for client_id in disconnected:
            self.disconnect_client(client_id)
            
    def test_connection(self):
        """Тест подключения"""
        print(f"\n[TEST] ТЕСТ ПОДКЛЮЧЕНИЯ")
        print("-" * 40)
        
        local_ip = self.get_local_ip()
        
        # Тест локального подключения
        print(f"[LOCAL_TEST] Тест локального подключения...")
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(5)
            result = test_socket.connect_ex((local_ip, self.port))
            test_socket.close()
            
            if result == 0:
                print(f"[OK] Локальное подключение работает!")
                print(f"[INFO] IP: {local_ip}, Порт: {self.port}")
            else:
                print(f"[FAIL] Локальное подключение не работает (код: {result})")
                print(f"[DEBUG] Проверьте что сервер запущен")
        except Exception as e:
            print(f"[ERROR] Ошибка локального теста: {e}")
        
        print()
        print("[ANDROID_CHECK] Проверка настроек Android:")
        print(f"   1. IP адрес в приложении: {local_ip}")
        print(f"   2. Порт в приложении: {self.port}")
        print("   3. Телефон в той же сети (для локального теста)")
        print("   4. Права интернета в приложении разрешены")
        print("   5. Файрвол/антивирус не блокируют")
        
        print("-" * 40)
        
    def show_status(self):
        """Показать статус"""
        print(f"\n[STATUS] СТАТУС ТЕСТОВОГО СЕРВЕРА")
        print("-" * 50)
        print(f"[PORT] Порт: {self.port}")
        print(f"[IP] Локальный IP: {self.get_local_ip()}")
        print(f"[CLIENTS] Подключено: {len(self.clients)}")
        print(f"[UPTIME] Время работы: {self.get_uptime()}")
        print(f"[STATE] Статус: {'Активен' if self.server_running else 'Остановлен'}")
        print("-" * 50)
        
    def show_clients(self):
        """Показать клиентов"""
        print(f"\n[CLIENTS] ПОДКЛЮЧЕННЫЕ КЛИЕНТЫ ({len(self.clients)})")
        print("-" * 60)
        
        if not self.clients:
            print("[EMPTY] Нет подключенных клиентов")
        else:
            for i, (client_id, client_info) in enumerate(self.clients.items(), 1):
                connected_time = datetime.now() - client_info['connected']
                minutes = int(connected_time.total_seconds() / 60)
                seconds = int(connected_time.total_seconds() % 60)
                
                print(f"{i:2d}. [CLIENT] {client_id}")
                print(f"     [TIME] Подключен: {minutes:02d}:{seconds:02d} назад")
                print()
                
        print("-" * 60)
        
    def show_help(self):
        """Показать справку"""
        print(f"\n[HELP] СПРАВКА ТЕСТОВОГО СЕРВЕРА")
        print("-" * 50)
        print("[PURPOSE] Назначение:")
        print("   - Максимально простой сервер для теста")
        print("   - Подробное логирование всех событий")
        print("   - Отладка проблем с подключением")
        print()
        print("[COMMANDS] Команды:")
        print("   status  - показать статус сервера")
        print("   clients - список подключенных клиентов")
        print("   test    - тест подключения")
        print("   clear   - очистить экран")
        print("   stop    - остановить сервер")
        print("   help    - показать эту справку")
        print()
        print("[DEBUG] Если не подключается:")
        print("   1. Проверьте IP адрес в приложении")
        print("   2. Проверьте порт в приложении")
        print("   3. Запустите 'test' команду")
        print("   4. Проверьте права интернета на телефоне")
        print("-" * 50)
        
    def get_uptime(self):
        """Получить время работы"""
        if self.start_time:
            uptime = datetime.now() - self.start_time
            hours = int(uptime.total_seconds() / 3600)
            minutes = int((uptime.total_seconds() % 3600) / 60)
            return f"{hours:02d}:{minutes:02d}"
        return "00:00"
        
    def stop(self):
        """Остановка сервера"""
        print("\n[STOP] Остановка тестового сервера...")
        self.server_running = False
        
        for client_id in list(self.clients.keys()):
            self.disconnect_client(client_id)
            
        if self.server_socket:
            try:
                self.server_socket.close()
                print("[CLOSE] Серверный сокет закрыт")
            except:
                pass
                
        print("[STOPPED] Тестовый сервер остановлен")

def main():
    print("[TEST] Simple Test Server - Максимально простой")
    print("=" * 60)
    
    server = SimpleTestServer(port=8888)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[EXIT] До свидания!")

if __name__ == "__main__":
    main()
