import psutil
import time
import mysql.connector
import wmi

class SystemMonitor:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db = mysql.connector.connect(
            host=db_host, 
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.cursor = self.db.cursor()

    def get_cpu_temp(self):
        try:
            w = wmi.WMI(namespace=r"root\wmi") 
            temperature_info = w.MSAcpi_ThermalZoneTemperature()
            for temp in temperature_info:
                cpu_temp = temp.CurrentTemperature / 10.0 - 273.15 
                return cpu_temp
        except Exception as e:
            print(f"Hata: {e}")
            return None  

    def get_system_info(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        cpu_temp = self.get_cpu_temp()
        if cpu_temp is None:
            cpu_temp = "Bilinmiyor" 
        return cpu_usage, ram_usage, cpu_temp

    def insert_data(self, cpu, ram, temp):
        query = "INSERT INTO system_info (cpu_usage, ram_usage, cpu_temp) VALUES (%s, %s, %s)"
        if temp == "Bilinmiyor":
            temp = None 
        values = (cpu, ram, temp)
        self.cursor.execute(query, values)
        self.db.commit()

    def start_monitoring(self, interval=60):
        while True:
            cpu, ram, temp = self.get_system_info()
            self.insert_data(cpu, ram, temp)
            print(f"CPU: {cpu}%, RAM: {ram}%, Sıcaklık: {temp}")
            time.sleep(interval)


db_host = "localhost"
db_user = "root"
db_password = "Pier123+"
db_name = "system_monitor_db"

monitor = SystemMonitor(db_host, db_user, db_password, db_name)

monitor.start_monitoring()
