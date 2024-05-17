
```markdown
# Günlük Etkinlik ve Duygu Tanıma Programı

Bu Python programı, kullanıcılara günlük etkinlik önerileri sunar ve bilgisayar kamerası aracılığıyla yüz ifadelerini tanıyarak duygusal geri bildirim alır. Program, bir API kullanarak günlük kelime önerileri alır ve bu önerileri etkinliklerle birlikte bir dosyaya yazar.

## Gereksinimler

Bu programın çalışabilmesi için aşağıdaki Python kütüphanelerine ihtiyacınız vardır:

- `random`
- `requests`
- `datetime`
- `cv2` (OpenCV)
- `dlib`
- `facial_emotion_recognition`

Bu kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:

```sh
pip install requests opencv-python dlib facial_emotion_recognition
```

## Kullanım

### 1. Etkinlik Önerileri Oluşturma

Program, günlük etkinlik önerilerini ve kelime önerilerini içeren bir dosya oluşturur. Etkinlik önerileri rastgele seçilir ve her güne bir etkinlik atanır. Dosya, programın çalıştırıldığı dizine `etkinlikler.txt` adıyla kaydedilir.

### 2. Yüz Tanıma ve Duygu Analizi

Program, bilgisayar kamerası aracılığıyla kullanıcının yüz ifadelerini analiz eder. Kullanıcının yüz ifadesine göre mutlu veya üzgün olduğu belirlenir ve kullanıcıdan etkinliklerle ilgili geri bildirim alınır.

### Programın Detaylı Açıklaması

#### 1. Kelime Önerisi Alma

`kelime_onerisi_al` fonksiyonu, bir API'ye istek göndererek günlük kelime önerisi alır. Başarılı bir yanıt alınırsa kelime döner, aksi takdirde `None` döner.

```python
def kelime_onerisi_al():
    try:
        response = requests.get("https://api.dailysmarty.com/word")
        response.raise_for_status()
        data = response.json()
        return data.get('word', None)
    except requests.RequestException as e:
        print(f"Kelime önerisi alınırken hata oluştu: {e}")
        return None
```

#### 2. Etkinlik Önerileri

`etkinlikler` listesi, her biri günlük öneri olarak kullanılabilecek etkinlikleri içerir.

#### 3. Etkinlik ve Kelime Önerilerini Dosyaya Yazma

Program, 30 günlük bir döngü içinde her gün için rastgele bir etkinlik seçer ve API'den alınan kelime önerisi ile birlikte dosyaya yazar.

```python
tarih_formati = "%d %B %Y"
bugun = datetime.now()
bitis_tarihi = bugun + timedelta(days=30)

with open("etkinlikler.txt", "w") as dosya:
    while bugun < bitis_tarihi:
        secilen_etkinlik = random.choice(etkinlikler)
        kelime_onerisi = kelime_onerisi_al()
        
        satir = f"{bugun.strftime(tarih_formati)}: {secilen_etkinlik}"
        if kelime_onerisi:
            satir += f" ({kelime_onerisi})"
        satir += "\n"
        
        dosya.write(satir)
        bugun += timedelta(days=1)
```

#### 4. Yüz Tanıma ve Duygu Analizi

Bilgisayar kamerası kullanılarak kullanıcının yüz ifadeleri analiz edilir ve duygu durumuna göre geri bildirim alınır.

```python
emotion_recognition = EmotionRecognition()
kamera = cv2.VideoCapture(0)

while True:
    ret, frame = kamera.read()
    if not ret:
        print("Kamera ile bağlantı kurulamadı!")
        break

    gri_tonlamali = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detektor = dlib.get_frontal_face_detector()
    yuzler = detektor(gri_tonlamali)

    for yuz in yuzler:
        x, y, w, h = yuz.left(), yuz.top(), yuz.width(), yuz.height()
        duygular = emotion_recognition.recognise_emotion(frame[y:y + h, x:x + w].copy())
        if duygular:
            if duygular["happy"] > duygular["sad"]:
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
```

## Programı Çalıştırma

Programı çalıştırmak için, Python dosyasını terminal veya komut satırından çalıştırın:

```sh
python program_adı.py
```

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.
```

Bu `README.md` dosyası, programınızın ne yaptığını, nasıl çalıştığını ve kullanıcıların programı nasıl kullanabileceklerini açıklayan detaylı bir belgedir. Ayrıca, programın gereksinimlerini, kurulum adımlarını ve çalıştırma talimatlarını içerir.
