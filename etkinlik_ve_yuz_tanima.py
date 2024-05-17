import random
import requests
from datetime import datetime, timedelta
import cv2
import dlib
from facial_emotion_recognition import EmotionRecognition

# API'den kelime önerisi alıp döndüren fonksiyon
def kelime_onerisi_al():
    """
    Günlük kelime önerisi almak için bir API isteği gönderir.
    
    Dailysmarty API'sine bir GET isteği yaparak yanıtın JSON formatında olup olmadığını kontrol eder.
    Eğer istek başarılıysa, JSON yanıtından 'word' anahtarının değerini döner.
    Başarısız olursa None döner.
    """
    try:
        response = requests.get("https://api.dailysmarty.com/word")
        response.raise_for_status()  # İstek başarılı mı kontrol eder
        data = response.json()
        return data.get('word', None)
    except requests.RequestException as e:
        print(f"Kelime önerisi alınırken hata oluştu: {e}")
        return None

# Günlük etkinlik önerilerini içeren liste
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

# Tarih formatı
tarih_formati = "%d %B %Y"

# Bugünün tarihi
bugun = datetime.now()
# Bir ay sonrasının tarihi
bitis_tarihi = bugun + timedelta(days=30)

# Etkinliklerin yazılacağı dosyanın açılması
with open("etkinlikler.txt", "w") as dosya:
    while bugun < bitis_tarihi:
        # Günlük rastgele bir etkinlik seçilir
        secilen_etkinlik = random.choice(etkinlikler)
        # Günlük kelime önerisi alınır
        kelime_onerisi = kelime_onerisi_al()
        
        # Dosyaya yazılacak metin hazırlanır
        satir = f"{bugun.strftime(tarih_formati)}: {secilen_etkinlik}"
        if kelime_onerisi:
            satir += f" ({kelime_onerisi})"
        satir += "\n"
        
        # Dosyaya yazılır
        dosya.write(satir)
        
        # Tarih bir gün ileri alınır
        bugun += timedelta(days=1)

print("Etkinlikler başarıyla oluşturuldu ve 'etkinlikler.txt' dosyasına kaydedildi.")

# Duygu tanıma için EmotionRecognition nesnesi oluşturulması
emotion_recognition = EmotionRecognition()

# Bilgisayar kamerasının açılması
kamera = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare alınır
    ret, frame = kamera.read()
    if not ret:
        print("Kamera ile bağlantı kurulamadı!")
        break

    # Görüntü gri tonlamalıya çevrilir
    gri_tonlamali = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüz tanıma detektörü kullanılarak yüzler tespit edilir
    detektor = dlib.get_frontal_face_detector()
    yuzler = detektor(gri_tonlamali)

    # Tespit edilen her yüz için
    for yuz in yuzler:
        x, y, w, h = yuz.left(), yuz.top(), yuz.width(), yuz.height()

        # Yüz bölgesinden duygu tanıma yapılır
        duygular = emotion_recognition.recognise_emotion(frame[y:y + h, x:x + w].copy())
        if duygular:
            # Duygu analizine göre geri bildirim alınır
            if duygular["happy"] > duygular["sad"]:
                geri_bildirim = input("Yüz ifadeniz mutlu, etkinliklerle ilgili mutlu musunuz? (Evet/Hayır): ")
            else:
                geri_bildirim = input("Yüz ifadeniz üzgün, etkinliklerle ilgili mutlu musunuz? (Evet/Hayır): ")

            # Kullanıcıdan alınan geri bildirime göre cevap verilir
            if geri_bildirim.lower() == "evet":
                print("Harika! Mutluluk önemli, bu etkinlikler size iyi gelmiş demektir.")
            elif geri_bildirim.lower() == "hayır":
                print("Üzgünüz. Daha iyi etkinlikler için bir sonraki güne geçebilirsiniz.")
            else:
                print("Lütfen geçerli bir yanıt verin (Evet/Hayır).")

        # Tespit edilen yüz kare içine alınır
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Görüntü ekranda gösterilir
    cv2.imshow("Yüz Tanıma", frame)

    # 'q' tuşuna basılırsa döngü sonlandırılır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera ve tüm pencereler kapatılır
kamera.release()
cv2.destroyAllWindows()
