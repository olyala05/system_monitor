import psutil
import socket
import time
import mysql.connector
from mysql.connector import Error

class SystemMonitor:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Veritabanına başarıyla bağlanıldı.")
        except Error as e:
            print(f"Veritabanı bağlantısı başarısız: {e}")

    def collect_system_info(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.used / (1024 ** 3)
        try:
            temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        except (KeyError, IndexError):
            temp = None

        # Disk bilgisi
        disk = psutil.disk_usage('/')
        total_disk = disk.total / (1024 ** 3) 
        used_disk = disk.used / (1024 ** 3) 

        # MAC adresi ve IP adresi
        mac_address = self.get_mac_address()
        ip_address = self.get_ip_address()

        return cpu_usage, ram_usage, temp, total_disk, used_disk, mac_address, ip_address

    def get_mac_address(self):
        """Ağ arayüzü üzerinden MAC adresini alır."""
        addrs = psutil.net_if_addrs()
        for interface, addrs_list in addrs.items():
            for addr in addrs_list:
                if addr.family == psutil.AF_LINK: 
                    return addr.address
        return None

    def get_ip_address(self):
        """Aktif ağ arayüzü üzerinden IP adresini alır."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    def insert_data(self, cpu_usage, ram_usage, temp, total_disk, used_disk, mac_address, ip_address):
        """Verileri MySQL veritabanına ekliyoruz."""
        try:
            query = """INSERT INTO system_info (cpu_usage, ram_usage, cpu_temp, total_disk, used_disk, mac_address, ip_address) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (cpu_usage, ram_usage, temp, total_disk, used_disk, mac_address, ip_address)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Error as e:
            print(f"Veri eklenirken hata oluştu: {e}")

    def monitor(self, duration=60):
        """Verileri 1 dakika arayla alıp kaydediyoruz."""
        for _ in range(duration):
            cpu_usage, ram_usage, cpu_temp, total_disk, used_disk, mac_address, ip_address = self.collect_system_info()
            self.insert_data(cpu_usage, ram_usage, cpu_temp, total_disk, used_disk, mac_address, ip_address)
            time.sleep(60)

    def close_connection(self):
        """Veritabanı bağlantısını kapatıyoruz."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Veritabanı bağlantısı kapatıldı.")

db_host = "localhost"  
db_user = "root"   
db_password = "123" 
db_name = "system_monitor_db"

monitor = SystemMonitor(db_host, db_user, db_password, db_name)
monitor.monitor(duration=60)  
monitor.close_connection()
