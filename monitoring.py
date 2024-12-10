import psutil
import time
import mysql.connector
import wmi

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pier123+",
    database="system_monitor_db"
)

# sql sorgularını çalıştırmak, sonuçları almak ve  veritabanı ile  etkileşim kurmak için kullnılır
cursor = db.cursor()

def get_cpu_temp():
    try:
        # WMI kullanarak CPU sıcaklığını alıyoruz
        w = wmi.WMI(namespace=r"root\wmi") 
        temperature_info = w.MSAcpi_ThermalZoneTemperature()
        for temp in temperature_info:
            cpu_temp = temp.CurrentTemperature / 10.0 - 273.15 
            return cpu_temp
    except Exception as e:
        return None  

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    cpu_temp = get_cpu_temp()  
    if cpu_temp is None: 
        cpu_temp = "Bilinmiyor" 
    return cpu_usage, ram_usage, cpu_temp

def insert_data(minute, cpu, ram, temp):
    query = "INSERT INTO system_info (minute, cpu_usage, ram_usage, cpu_temp) VALUES (%s, %s, %s, %s)"
    if temp == "Bilinmiyor":
        temp = None
    values = (minute, cpu, ram, temp)
    cursor.execute(query, values)
    db.commit()

minute = 1
while True:
    cpu, ram, temp = get_system_info()
    insert_data(minute, cpu, ram, temp)
    print(f"Veri eklendi: Dakika {minute}, CPU: {cpu}%, RAM: {ram}%, Sıcaklık: {temp}")
    time.sleep(60)
    minute += 1
