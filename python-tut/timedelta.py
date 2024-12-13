from datetime import datetime, timedelta

current_time = datetime.now()

new_time = current_time + timedelta(minutes=5)

print("Şu anki zman: ", current_time)
print("5 dk sonrası: ", new_time)

print("========================================")
start_time = datetime.now()

event_duration = timedelta(hours=2, minutes=30)

end_time = start_time + event_duration

print("Etkinlik Başlangıç zamanı: ", start_time.strftime("%Y-%m-%d %H:%M:%S"))
print("Etkinlik Süresi: ", event_duration)
print("Etkinlik bitiş zamanı: ", end_time.strftime("%Y-%m-%d %H:%M:%S"))