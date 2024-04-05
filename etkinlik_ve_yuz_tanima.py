import random
import requests
from datetime import datetime, timedelta
import cv2
import dlib
from facial_emotion_recognition import EmotionRecognition

def kelime_onerisi_al():
    response = requests.get("https://api.dailysmarty.com/word")
    if response.status_code == 200:
        data = response.json()
        return data['word']
    else:
        return None

etkinlikler = [
    "Yeni bir dil öğren.",
    "Bir müzik enstrümanı çalmayı dene.",
    "Bir kitap oku ve özetini yaz.",
    "Yürüyüş yap ve doğayı keşfet.",
    "Yeni bir tarif deneyerek yemek yap.",
    "Bir arkadaşınla iletişime geç ve sohbet et.",
    "Bir bilim makalesi oku ve öğrendiklerini paylaş.",
    "Farklı bir kültüre ait bir film izle.",
    "Bir hayvan barınağına gönüllü olarak yardım et.",
    "Yeni bir hobiyi denemeye başla."
]

tarih_formati = "%d %B %Y"

bugun = datetime.now()
bitis_tarihi = bugun + timedelta(days=30)

with open("etkinlikler.txt", "w") as dosya:
    while bugun < bitis_tarihi:
        secilen_etkinlik = random.choice(etkinlikler)
        kelime_onerisi = kelime_onerisi_al()
        dosya.write(f"{bugun.strftime(tarih_formati)}: {secilen_etkinlik} ({kelime_onerisi})\n")
        bugun += timedelta(days=1)

print("Etkinlikler başarıyla oluşturuldu ve 'etkinlikler.txt' dosyasına kaydedildi.")

emotion_recognition = EmotionRecognition()

kamera = cv2.VideoCapture(0)

while True:
    ret, frame = kamera.read()
    if not ret:
        break

    gri_tonlamali = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detektor = dlib.get_frontal_face_detector()
    yuzler = detektor(gri_tonlamali)

    for yuz in yuzler:
        x, y, w, h = yuz.left(), yuz.top(), yuz.width(), yuz.height()

        duygular = emotion_recognition.recognise_emotion(frame[y:y + h, x:x + w].copy())
        if duygular:
            if duygular["mutlu"] > duygular["üzgün"]:
                geri_bildirim = input("Yüz ifadeniz mutlu, etkinliklerle ilgili mutlu musunuz? (Evet/Hayır): ")
            else:
                geri_bildirim = input("Yüz ifadeniz üzgün, etkinliklerle ilgili mutlu musunuz? (Evet/Hayır): ")

            if geri_bildirim.lower() == "evet":
                print("Harika! Mutluluk önemli, bu etkinlikler size iyi gelmiş demektir.")
            elif geri_bildirim.lower() == "hayır":
                print("Üzgünüz. Daha iyi etkinlikler için bir sonraki güne geçebilirsiniz.")
            else:
                print("Lütfen geçerli bir yanıt verin (Evet/Hayır).")

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Yüz Tanıma", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()
