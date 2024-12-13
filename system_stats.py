import psutil
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
        ram_usage = psutil.virtual_memory().percent 
        
        try:
            temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        except (KeyError, IndexError):
            temp = None
        
        return cpu_usage, ram_usage, temp

    def insert_data(self, cpu_usage, ram_usage, temp):
        """Verileri MySQL veritabanına ekliyoruz."""
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            query = """INSERT INTO system_info (cpu_usage, ram_usage, cpu_tepm) 
                       VALUES (%s, %s, %s, %s)"""
            values = (timestamp, cpu_usage, ram_usage, temp)
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"Veri başarıyla eklendi: {timestamp}")
        except Error as e:
            print(f"Veri eklenirken hata oluştu: {e}")

    def monitor(self, duration=60):
        """Verileri 1 dakika arayla alıp kaydediyoruz."""
        for _ in range(duration):
            cpu_usage, ram_usage, temp = self.collect_system_info()
            self.insert_data(cpu_usage, ram_usage, temp)
            time.sleep(60)

    def close_connection(self):
        """Veritabanı bağlantısını kapatıyoruz."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Veritabanı bağlantısı kapatıldı.")

db_host = "localhost"  
db_user = "root"   
db_password = "Pier123+" 
db_name = "system_monitor_db"


monitor = SystemMonitor(db_host, db_user, db_password, db_name)
monitor.monitor(duration=60)  
monitor.close_connection()
