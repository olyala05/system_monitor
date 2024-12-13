#random, uniform fonksiyonu


# Random modülü bizim için rastgeler sayılar veya değerler üreten fonksiyonları barındırıyor :

import random 

# brada 0 ile 9 aralıgında rastgele  ondalık sayılar üretiyor 10 tane üret dedim 
for i in range(10):
    print(random.random())


# !! ================== kendi istediğim rastgele sayılar üretmek istersem uniform kullanacağım ===========
"""kendi istediğim rastgele sayılar üretmek istersem uniform kullanacağım """
print("===============================================================")
for i in range(10):
    print(random.uniform(10, 30))

print("================================================================")
# !! Tam Sayılarını  üretmek için randint() fonksiyonu (Sadece burada üst sınır dahil)
for i in range(10):
    print(random.randint(1,5))

print("================================================================")
# !! Tam Sayılarını  üretmek için ranrange() fonksiyonu (üst sınır dahil değil) 
for i in range(10):
    print(random.randrange(1,10,2))