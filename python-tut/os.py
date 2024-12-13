# Operating System
import os

print(os.getcwd())

# Bu Klasörümün içinde değişiklik yapılacağını ilk başta belirtiyoruz !! 
os.chdir("C:\Python-Project\system_monitor\python-tut")
# print(os.listdir("\Python-Project\system_monitor"))

for dosya in os.listdir():
    print(dosya)

# !! Nasıl Yeni Klasör oluşturabiliriiz !! mkdir() !!
# os.mkdir("DenemeKlasor")

# !! iç içe birden fazla klasör oluşturmak istersem !! makedirs() !!
# os.makedirs("Deneme1/Deneme2/Deneme3")

# !! klasör silmek için !! os.rmdir("") !!
# os.rmdir("DenemeKlasor")
os.rmdir("Deneme1/Deneme2/Deneme3")
