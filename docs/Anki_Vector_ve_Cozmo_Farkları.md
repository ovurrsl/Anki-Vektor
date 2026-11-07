# **Anki Vector ve Cozmo Farkları**

[https\://gemini.google.com/app/a2978a6e21913c36](https://gemini.google.com/app/a2978a6e21913c36)

*User prompt: Logitech Mx Brio Ultra Hd 4K & INSTA360 Link 2 Pro Aı & Logitech Brio 105 üçünden hangisi peki artıları eksileri gerekli gereksiz yönleri karşılaştırması*

Response: Bu üç kamera tamamen farklı bütçe ve kullanım sınıflarına aittir. Kararınızı belirleyecek temel unsur, kamerayı **7/24 masayı ve Vector'ü izleyen bir makine gözü (kuşbakışı radar)** olarak mı, yoksa **bilgisayar başında yayın, toplantı ve hareketli takip** için mi kullanacağınızdır.

Masaüstü yapay zeka ve Vector gözlem projesi için en kararlı ve optik olarak en güçlü seçenek **Logitech MX Brio**'dur.

### **Karşılaştırma Tablosu**

| Özellik | Logitech Brio 105 | Logitech MX Brio Ultra HD 4K | Insta360 Link 2 (Pro AI) |
| :---- | :---- | :---- | :---- |
| **Çözünürlük & FPS** | 1080p @ 30 FPS | 4K @ 30 FPS / 1080p @ 60 FPS | 4K @ 30 FPS / 1080p @ 60 FPS |
| **Sensör Boyutu** | Küçük (Giriş seviyesi) | **1/1.8" Sony STARVIS** (En büyük sensör) | 1/2" Sensör |
| **Görüş Açısı (FOV)** | **58° (Çok dar)** | 90° / 78° / 65° (Geniş) | \~79.5° |
| **Mekanik Yapı** | Sabit | **Show Mode (Masaya elle eğilebilir)** | **2 Eksenli Motorlu Gimbal** |
| **Odaklama** | Sabit Odak (Fixed Focus) | Gelişmiş Faz Algılamalı Hibrit AF | Hızlı Faz Algılamalı AF (PDAF) |
| **Arduino UNO Q / Linux Uyumu** | %100 Tak-Çalıştır UVC | %100 Standart UVC (Tam Uyumlu) | Temel UVC çalışır, AI yazılımı Linux'ta yok |
| **7/24 Çalışma Güvenilirliği** | Yüksek (Pasif) | **Çok Yüksek (Metal gövde, motorsuz)** | Düşük-Orta (Motorlar zamanla ısınır/aşınır) |
| **Fiyat Seviyesi** | Çok Ucuz (\~40\$) | Premium (\~200\$) \\vert{} Premium (\~200-230\$) |  |

### **1\. Logitech MX Brio Ultra HD 4K**

> * **Artıları:**  
  * **Devasa Sensör (Sony STARVIS):** Düşük ışık performansı olağanüstüdür. Gece odada sadece monitör ışığı veya loş lamba varken bile Vector'ü, masadaki nesneleri ve barkodları kumlanma (noise) olmadan net görür.  
  * **Show Mode (Masaya Eğme):** Kameranın menteşesi, monitör bağlantısını bozmadan kafasını doğrudan 90 derece aşağı (masanın yüzeyine) eğmenize izin verir. Masayı tepe kamerası gibi izletmek için ek aparata gerek bırakmaz.  
  * **Linux & UVC Kararlılığı:** Standart Linux UVC sürücüsüyle çalıştığı için Debian tabanlı Arduino UNO Q'ya taktığınız an OpenCV ile 4K/1080p doğrudan kare çekebilirsiniz.  
  * **Katı Hal (Motorsuz) Dayanıklılık:** İçinde hareketli mekanik motor olmadığı için 7/24 açık kalsa dahi aşınma veya takılma riski yoktur.  
> * **Eksileri:**  
  * Motorlu takip mekanizması yoktur; nereye çevirirseniz sadece oraya bakar.  
  * Logi Tune yazılımı Linux'ta çalışmaz (ancak dahili belleği ayarları hatırlar).  
> * **Gerekli / Gereksiz Yönleri:**  
  * *Gerekli:* 90° geniş açı, düşük ışıkta netlik (Gemini Vision ve nesne tanıma için kritik), Show Mode menteşesi.  
  * *Gereksiz:* Dahili mikrofonunun gürültü engelleme profilleri (eğer ses işini UNO Q veya Vector halledecekse gereksiz masraftır).

### **2\. Insta360 Link 2 (Pro AI)**

> * **Artıları:**  
  * **2 Eksenli Motorlu Gimbal:** Kamera fiziksel olarak sağa-sola, yukarı-aşağı dönebilir.  
  * **Otonom Takip:** Odanın içinde ayağa kalkıp gezindiğinizde motorlarıyla sizi takip eder.  
  * **Yazılımsal Masa Modu (DeskView):** Gimbal otomatik olarak aşağı yönelip masanın perspektifini yazılımla düzeltir.  
  * **El Hareketi (Gesture) Kontrolü:** Kameraya elinizi göstererek takibi başlatabilir veya yakınlaştırma yapabilirsiniz.  
> * **Eksileri:**  
  * **7/24 Proje İçin Riskli:** Mekanik gimbal motorları 7/24 kesintisiz çalışmaya ve nöbet tutmaya uygun değildir; sürekli açık kaldığında ısınır ve mekanik ömrü kısalır.  
  * **Linux Kısıtı:** Akıllı yapay zeka takip ve kalibrasyon yazılımı Windows/macOS odaklıdır. Arduino UNO Q üzerinde sadece düz bir web kamerası gibi davranır, akıllı takip yeteneklerinin çoğunu kaybeder.  
  * **Yüksek Güç Tüketimi:** Motorlar hareket ederken USB portundan yüksek akım çeker; Arduino UNO Q'nun 5V besleme hattını zorlayabilir (harici adaptörlü USB hub gerekebilir).  
> * **Gerekli / Gereksiz Yönleri:**  
  * *Gerekli:* Yayın yapıyorsanız veya tahta başında sunum yaparken sizi takip etmesi harikadır.  
  * *Gereksiz (Bu Proje İçin):* Masayı ve Vector'ü sabit bir açıdan izleyecek bir sistem için motorlu gimbal lüks ve arıza potansiyeli yüksek bir fazlalıktır.

### **3\. Logitech Brio 105**

> * **Artıları:**  
  * Çok ucuzdur; bütçeyi zorlamaz.  
  * Çok az güç tüketir (UNO Q portunu hiç yormaz), hafiftir ve tak-çalıştır Linux uyumludur.  
> * **Eksileri:**  
  * **58° Çok Dar Görüş Açısı:** Bu kameranın en büyük handikabıdır. Monitörün üstüne taktığınızda masanın sadece çok küçük bir bölgesini görür; masanın kenarlarındaki nesneleri ve gezen Vector'ü kadraja sığdıramaz.  
  * **Sabit Odak (Fixed Focus):** Yakındaki bir nesneyi veya Vector'ün üzerindeki detayları netleyemez; görüntü bulanıklaşır.  
  * Düşük ışık performansı vasattır; loş ortamda görüntü çamurlaşır, nesne algılama (YOLO/Gemini) modelleri hata yapar.  
> * **Gerekli / Gereksiz Yönleri:**  
  * Temel ofis Zoom görüşmeleri için yeterlidir; ancak yapay zeka tabanlı "Masaüstü Gözlemcisi / Kuşbakışı Radar" görevi için teknik özellikleri yetersiz kalır.

### **Karar Matrisi**

> 1. **Bütçeniz Varsa ve Amaç Yapay Zeka \+ Masa Gözlemciliği İse: → Logitech MX Brio** Büyük STARVIS sensörü loş odada bile kusursuz görüntü verir, 90 derecelik geniş açısıyla tüm masayı tek kareye sığdırır, elle masaya doğru bükülebilen **Show Mode** mekanizması bulunur ve Linux (UNO Q) ile sıfır sorunla 7/24 çalışır.  
> 2. **Kamerayı PC'ye Bağlayıp Kendinizi ve Odayı Takip Ettirecekseniz: → Insta360 Link 2** Eğer öncelik Vector değil de masa başında sizin hareketlerinizi izleyen, yayın ve toplantılarda sizi kadrajda tutan motorlu bir robotik kamera ise bu model tercih edilmelidir.  
> 3. **Bütçe Kısıtlıysa: → Brio 105 Yerine Alternatif** Brio 105'in 58° açısı ve sabit odağı bu projeyi kör eder. Bütçeyi düşük tutmak istiyorsanız Brio 105 yerine geniş açılı (en az 78°-90°) ve otomatik odaklı **Logitech Brio 500** veya klasik bir **Logitech C920 / C922** çok daha işlevsel bir bütçe çözümü olur.

---

*User prompt: Insta360 Link 2 bunu kullanmak istiyorum*

Response: Harika bir tercih; çünkü motorlu bir gimbal kameranın projeye katacağı en büyük avantaj, sistemin artık **sadece bir gözlemci değil, odadaki hareketleri fiziksel olarak takip eden ikinci bir robot** haline gelmesidir. Vector masada dolaşırken, Insta360 Link 2'nin motorlarıyla onu veya sizi kadrajda tutması tam bir bilimkurgu masası atmosferi yaratır.

Insta360 Link 2'yi bu ekosistemde en yüksek verimle çalıştırmak için dikkat etmeniz gereken mimari kararlar, bağlantı yolları ve donanımı kodla yönetme yöntemleri şunlardır:

### **1\. Nereye Bağlanmalı? (PC vs. Arduino UNO Q)**

Bu kamerayı nereye takacağınız, projede ondan ne beklediğinize göre değişir:

#### **Seçenek A: Doğrudan Masaüstü PC'ye (Windows 11\) Bağlamak (Önerilen)**

> * **Neden?** Insta360’ın resmi **Link Controller** yazılımı Windows üzerinde arka planda çalışır. Kameranın yapay zeka tabanlı yüz takibi, beyaz tahta modu ve otomatik masa modu (DeskView) tam kapasiteyle devreye girer.  
> * **Görüntü Paylaşımı:** PC'deki FastAPI sunucusu, kameranın görüntüsünü tek bir endpoint (GET /camera/frame) ile yerel ağa açar. UNO Q veya Gemini bir kareye ihtiyaç duyduğunda bu yerel adresten alır.  
> * **Sınır:** Sadece PC açıkken çalışır.

#### **Seçenek B: Arduino UNO Q'ya (Debian Linux) Bağlamak (7/24 Nöbetçi Modu)**

> * **Neden?** Bilgisayar kapalıyken bile odanın tamamını ve masayı motorlarıyla tarayabilen 7/24 bir gözetleme kulesi elde edersiniz.  
> * **Nasıl Çalışır?** Insta360 Link serisi **standart UVC (USB Video Class)** protokolünü destekler. Yani Linux üzerinde ekstra sürücü gerekmeden standart bir web kamerası gibi tanınır.  
> * **Kritik Detay (Güç İhtiyacı):** Gimbal motorları anlık olarak hareket ettiğinde 1.5 Amper civarında akım çekebilir. Arduino UNO Q'nun Type-C beslemesinin en az 5V/3A (veya kaliteli bir PD adaptör) olduğundan emin olun; yetersiz akımda motor döndüğü an kart reset atabilir.

### **2\. Kameranın Gimbal Motorlarını Python Koduyla Yönetmek (UVC PTZ)**

Insta360 Link 2'nin en büyük gücü, motorlarının Linux ve Windows'ta standart **UVC PTZ (Pan/Tilt/Zoom)** komutlarına yanıt vermesidir. Resmi yazılımı olmasa bile Python üzerinden kameranın kafasını istediğiniz koordinata çevirebilirsiniz.

Debian Linux (UNO Q) veya Windows üzerinde çalışan örnek yönlendirme mantığı:

`import subprocess`

`def move_camera_gimbal(pan_angle: int, tilt_angle: int):`  
  `"""Insta360 Link 2'yi v4l2-ctl aracılığıyla donanımsal olarak sağa/sola ve yukarı/aşağı çevirir.`

  `pan_angle: Yatay eksen (-180 ile 180 derece arası) tilt_angle: Dikey eksen`  
  `(-90 ile 90 derece arası)`  
  `"""`  
  `try:`  
    `# Linux v4l2 kontrolü üzerinden Pan (Yatay) motoru sür`  
    `subprocess.run([`  
        `"v4l2-ctl",`  
        `"-d",`  
        `"/dev/video0",`  
        `"--set-ctrl",`  
        `f"pan_absolute={pan_angle}",`  
    `])`

    `# Tilt (Dikey / Masaya Eğilme) motoru sür`  
    `subprocess.run([`  
        `"v4l2-ctl",`  
        `"-d",`  
        `"/dev/video0",`  
        `"--set-ctrl",`  
        `f"tilt_absolute={tilt_angle}",`  
    `])`  
    `return True`  
  `except Exception as e:`  
    `print(f"Gimbal hareket hatası: {e}")`  
    `return False`

`def set_desk_view():`  
  `"""Kameranın kafasını otomatik olarak masanın yüzeyine 90 derece eğer."""`  
  `move_camera_gimbal(pan_angle=0, tilt_angle=-90)`

### **3\. Bu Kamerayla Projeye Ekleyebileceğiniz 3 Üst Düzey Yetenek**

> 1. **"Vector Takipçisi" (Auto-Tracking Vector):**  
   * RTX 5070 veya NPU üzerinde çalışan hafif bir nesne tespit modeli (örneğin YOLO), kameranın gördüğü karede Vector'ü tespit eder.  
   * Vector masanın sağına doğru ilerlediğinde, kodunuz Insta360'ın motorunu sağa çevirir. Vector nereye giderse kamera da onu takip eder.  
> 2. **Yerleşik Donanımsal El Hareketleri (On-Board Gestures):**  
   * Insta360 Link 2'nin temel el hareketi tanıma motoru kamera içindeki kendi çipinde çalışır.  
   * Masada otururken kameraya sadece avucunuzu gösterdiğinizde takibi başlatabilir veya elinizle "L" işareti yaparak kamerayı masaya/kendinize doğru zoom yaptırabilirsiniz.  
> 3. **DeskView (Masaüstü Tepe Kamerası):**  
   * Masada elektronik bir devre kartı, lehim veya bir evrak üzerinde çalışırken Vector'e *"Masama bak"* dediğinizde; kamera motoruyla kafasını doğrudan masanın yüzeyine eğer.  
   * Gemini 2.5 Pro Vision, masadaki devreyi veya kodu yüksek çözünürlükte görüp analiz eder.

### **Kurulum Sırasında Dikkat Edilecek 2 Püf Noktası**

> * **Gizlilik ve Uyku Pozisyonu:** Kamera kullanılmadığında veya PC/UNO Q üzerinden *"Kamerayı kapat"* komutu verildiğinde, Insta360 Link 2 kafasını fiziksel olarak tamamen aşağı çevirip yuvaya kilitler (Privacy Mode). Bu sayede odanızda sürekli açık kalsa bile mahremiyet endişesi yaratmaz.  
> * **Kablo Seçimi:** 4K video akışı ve motor beslemesini aynı anda taşıyacağı için kameranın kutusundan çıkan orijinal USB-C 3.0 kablosunu veya yüksek bant genişlikli kaliteli bir veri kablosu kullanın.

---

*User prompt: Ayrıca bu sisteme veri tabanı vb bir sistem bağlayamaz mıyız yapay zekanın kalıcı hafızası olsa local ve veya bulut üyelikli ücretli veya ücretsiz*

Response: Kalıcı hafıza (Long-Term Memory / Episodic Memory), Vector'ün sıradan bir soru-cevap botu yerine **sizi tanıyan, geçmiş konuşmaları ve masa alışkanlıklarınızı hatırlayan yaşayan bir varlık** gibi hissettirmesini sağlayan en kritik katmandır.

Yapay zeka için hafıza basit bir metin dosyası tutmaktan ibaret değildir; bilginin anlamını arayabilen bir **Vektör Veritabanı (Vector DB)** ve kesin verileri tutan bir **İlişkisel Veritabanı (SQL/NoSQL)** birlikteliğidir.

### **Hafıza Türleri ve Nasıl Çalıştığı**

Yapay zekanın hafızası 3 katmandan oluşur:

> 1. **Kısa Vadeli Hafıza (Çalışma Belleği):** O anki son 5–10 cümlenin bağlamıdır (Context Window).  
> 2. **Anlamsal ve Epizodik Hafıza (Vektörel Veritabanı):** Cümleler matematiksel vektörlere (embedding) dönüştürülüp saklanır. Örneğin aylar sonra *"Ben kahvemi nasıl seviyordum?"* dediğinizde, sistem tam eşleşen kelimeleri aramaz; anlamına göre en yakın anıyı (örneğin *"Kullanıcı şekersiz filtre kahve tercih ediyor"*) milisaniyeler içinde çekip modelin önüne koyar.  
> 3. **Olgusal Hafıza (Yapılandırılmış Veritabanı):** Doğum gününüz, masaüstü IP adresiniz, alarm saatleriniz veya masadaki eşyaların koordinatları gibi net tablolardan oluşur.

### **Veritabanı Seçenekleri: Yerel vs. Bulut (Ücretsiz ve Ücretli)**

| Çözüm | Türü | Maliyet | Nerede Çalışır? | Bu Proje İçin Avantajı / Dezavantajı |
| :---- | :---- | :---- | :---- | :---- |
| **sqlite-vec / SQLite** | Yerel (Gömülü) | **Tamamen Ücretsiz** | Arduino UNO Q | **En İdeal Çözüm:** Sıfır ek sunucu yükü, tek dosya (memory.db), 5 MB RAM tüketimi. İnternet ve PC kapalıyken bile çalışır. |
| **Qdrant (Local Docker / Rust)** | Yerel Vektör DB | **Tamamen Ücretsiz** | Masaüstü PC veya UNO Q | Rust ile yazıldığı için olağanüstü hızlıdır. Milyonlarca anıyı mikro saniyelerde tarar. |
| **Mem0 (Açık Kaynak)** | Yerel Hibrit Hafıza | **Tamamen Ücretsiz** | PC / UNO Q | Ajanlar için özel geliştirilmiştir; diyaloglardan kullanıcı tercihlerini otomatik ayıklayıp hafızaya yazar. |
| **Pinecone** | Bulut Vektör DB | Ücretsiz Kota / Sonrası Ücretli | Bulut Sunucu | Kurulum gerektirmez, API ile doğrudan bağlanılır. Ücretsiz kotası (Starter Tier) bireysel bir robot için fazlasıyla yeterlidir. |
| **Supabase (PostgreSQL \+ pgvector)** | Bulut Hibrit | Ücretsiz Kota / Sonrası Ücretli | Bulut Sunucu | Hem klasik tabloları (alarmlar, loglar) hem de anlamsal vektör aramalarını tek bir bulut panelinde ücretsiz barındırır. |
| **Google Cloud Firestore / Vector Search** | Bulut NoSQL | Ücretsiz Seviye Mevcut | Google Cloud | Google AI Studio ekosistemiyle doğrudan entegre olur. |

### **Bu Proje İçin En Doğru Mimari: sqlite-vec \+ Yerel SQLite**

Arduino UNO Q'nun 4 GB belleğini şişirmemek ve internet kesildiğinde robotun "hafıza kaybı" yaşamaması için **UNO Q üzerinde yerel sqlite-vec** kurmak en temiz yoldur.

Sistem şu döngüyle çalışır:

`[ Kullanıcı Konuşması ]`  
          `│`  
          `▼`  
`1. ARAMA (Retrieval): Kullanıcının cümlesi vektörleştirilir.`  
   `Veritabanından en alakalı 3 geçmiş anı çekilir.`  
          `│`  
          `▼`  
`2. MODEL (Gemini veya Yerel LLM):`  
   `System Prompt: "Sen Vector'sün. Kullanıcı hakkında bildiklerin: [Geçmiş Anılar]. Buna göre cevap ver."`  
          `│`  
          `▼`  
`3. ARKA PLAN ÖZETLEME (Memory Extraction):`  
   `Konuşmada yeni bir bilgi varsa (Örn: "Yarın sınavım var", "Yeni bir proje başladım"),`  
   `arka planda otomatik olarak veritabanına eklenir.`

### **UNO Q Üzerinde Hafıza Yönetimi (Python Örneği)**

Google AI Studio'nun metin vektörleştirme (text-embedding-004) modeli veya yerel bir embedding modeli ile çalışan pratik hafıza kurgusu:

`from google import genai`  
`import sqlite3`

`client = genai.Client(api_key="AI_STUDIO_API_ANAHTARINIZ")`

`# 1. Yerel Veritabanını Başlat`  
`conn = sqlite3.connect("vector_memory.db")`  
`cursor = conn.cursor()`  
`cursor.execute("""`  
`CREATE TABLE IF NOT EXISTS memories (`  
    `id INTEGER PRIMARY KEY AUTOINCREMENT,`  
    `category TEXT,`  
    `fact TEXT,`  
    `timestamp DATETIME DEFAULT CURRENT_TIMESTAMP`  
`)`  
`""")`  
`conn.commit()`

`def save_memory(fact: str, category: str = "general"):`  
  `"""Kullanıcı hakkındaki önemli bilgiyi kalıcı hafızaya yazar."""`  
  `cursor.execute(`  
      `"INSERT INTO memories (category, fact) VALUES (?, ?)", (category, fact)`  
  `)`  
  `conn.commit()`  
  `return f"Hafızaya kaydedildi: {fact}"`

`def get_relevant_memories(limit: int = 5) -> str:`  
  `"""Kayıtlı en güncel anıları ve bilgileri çeker."""`  
  `cursor.execute(`  
      `"SELECT fact FROM memories ORDER BY timestamp DESC LIMIT ?", (limit,)`  
  `)`  
  `rows = cursor.fetchall()`  
  `return "\n".join([f"- {r[0]}" for r in rows])`

`# --- Vector'e Verilecek Prompt Örneği ---`  
`def build_prompt_with_memory(user_message: str):`  
  `user_facts = get_relevant_memories()`

  `system_prompt = f"""`  
    `Sen masaüstünde yaşayan otonom Vector robotusun.`  
    `Kullanıcı hakkında geçmişten bildiğin kalıcı bilgiler:`  
    `{user_facts}`  
      
    `Bu bilgilere dayanarak kullanıcının geçmişini, projelerini ve alışkanlıklarını hatırlayarak doğal Türkçe konuş.`  
    `Eğer kullanıcı sana kendisiyle ilgili yeni bir bilgi verirse 'save_memory' aracını çağırarak kaydet.`  
    `"""`  
  `return system_prompt`

### **Kalıcı Hafızanın Sisteme Katacağı Farklar**

> * **Süreklilik:** Vector'ü kapatıp açsanız veya haftalarca seyahatte olsanız bile geri döndüğünüzde sizi tanır: *"Hoş geldin, en son Scirocco'nun far montajı ve Python sunucusu üzerine konuşmuştuk, projeyi bitirdin mi?"* diyebilir.  
> * **Proaktif Hatırlatmalar:** Sabah alarmınız çaldığında sadece hava durumunu değil, dünden hafızasına yazdığı notları hatırlar: *"Bugün saat 14:00'te toplantın vardı, unutma."*  
> * **Kişiselleştirilmiş İğneleme (Grok Modu):** Yaptığınız hataları da unutmaz: *"Yine mi aynı fonksiyonda indeks hatası aldın? Geçen hafta da aynısını yapmıştın"* gibi doğrudan geçmişinize referans veren espriler yapabilir.

---

*User prompt: Bana sana verdiğim gibi geliştirme fikirleri ver ve yapıyı komple tekrar incele mantıksal hata geliştirilmesi gereken kısımlar ve eklenmesi gereken özelliklere karar ver*

Response: Bu projeyi basit bir "akıllı oyuncak" seviyesinden çıkarıp kararlı, endüstriyel standartta çalışan bir **Fiziksel Bedenlenmiş Yapay Zeka (Embodied AI)** sistemine dönüştürmek için tüm mimariyi baştan sona masaya yatıralım.

Aşağıda sistemin **gizli mantıksal hataları (tuzakları)**, **mutlaka revize edilmesi gereken darboğazları** ve projeyi dünyada eşi benzeri olmayan bir seviyeye taşıyacak **çığır açıcı yeni geliştirme fikirleri** yer almaktadır.

## **1\. Sistemin Bütünsel Denetimi: Mantıksal Hatalar ve Gizli Tuzaklar**

Kağıt üzerinde harika duran ancak gerçek hayatta donanımları birbirine bağladığınızda sistemi kilitleyecek **5 kritik mantıksal hata** bulunmaktadır:

### **Hata 1: Akustik Yankı Geri Besleme Döngüsü (Acoustic Echo Loop)**

> * **Problem:** Vector'ün hoparlöründen Türkçe ses (stream\_wav\_file) çalarken, masadaki mikrofon veya Vector'ün kendi mikrofonu bu sesi tekrar duyar. Eğer arkada Gemini Live API veya fısıltı dinleyen Whisper sürekli açıksa; Vector'ün kendi söylediği lafı *"Kullanıcı yeni bir şey söyledi"* zannedip kendi kendine sonsuz bir konuşma ve halüsinasyon döngüsüne girer.  
> * **Çözüm (Half-Duplex Yazılımsal Susturucu / AEC):**  
  * Rust/Python ses katmanına bir **is\_speaking bayrağı (Mutex/Atomic Bool)** konulmalıdır.  
  * Vector ses üretmeye başladığı milisaniyede mikrofon girdisi yazılımsal olarak sessize alınmalı (Mute); Vector'ün konuşması bittikten sonra oda yankısı için 400 ms beklenip mikrofon tekrar dinlemeye açılmalıdır.

### **Hata 2: Sürekli Canlı Akışın (Live Stream) Token ve Bant Genişliği İflası**

> * **Problem:** Insta360 Link 2 ve Vector kamerasından saniyede 1–2 kareyi 7/24 kesintisiz Google Gemini Live API'ye basmak, ayda milyonlarca token yakar, API kotalarını tüketir ve UNO Q'nun işlemcisini boş yere %100 yükte tutar.  
> * **Çözüm (Olay Güdümlü Gözlem \- Event-Driven Vision Gating):**  
  * Görüntü akışı buluta **sürekli akmamalıdır**.  
  * Gözlem katmanı uyuyan bir nöbetçi olmalıdır: Intel NPU veya UNO Q üzerinde çok hafif bir hareket algılama algoritması (Background Subtraction / VAD) çalışır. Masada hareket olduğunda, ses algılandığında veya kullanıcı soru sorduğunda **tek bir anlık yüksek çözünürlüklü kare (snapshot)** çekilip Gemini'ye verilir.

### **Hata 3: "Sürekli Şarjdan Çıkma" Batarya Yıpranması (Battery Cycling Trap)**

> * **Problem:** Vector 2.0'ın bataryası aktiftir ancak \~45–60 dakikada biter. Size her cevap verdiğinde şarj istasyonundan dışarı çıkmaya kalkarsa, günde 30 kez şarj döngüsüne girer; batarya 3 ayda ölür ve geceleri şarj yuvasını ararken masadan düşme riski doğar.  
> * **Çözüm (Masaüstü Docked vs. Roaming Ayrımı):**  
  * **İstasyondayken (Docked Mod):** Soru-cevap, alarm, durum bildirme ve gündem yorumlarında **şarj istasyonundan hiç çıkmamalıdır**. Sadece kafasını yukarı kaldırıp (set\_head\_angle), göz ekranını ve hoparlörünü kullanarak sizinle konuşmalıdır.  
  * **Ayrılma (Roaming Mod):** Yalnızca *"Masayı gez"*, *"Şu nesneyi bul"* dendiğinde veya otonom devriye saatlerinde fiziksel olarak yuvasından ayrılmalıdır.

### **Hata 4: Insta360 Link 2'nin UNO Q'ya Bağlanma Hatası (USB ve Isı Darboğazı)**

> * **Problem:** Insta360 Link 2; 4K çözünürlük, yapay zeka takip çipi ve 2 eksenli motor barındıran ağır bir cihazdır. Bunu küçük Arduino UNO Q'ya takmak hem kartın Type-C güç hattını aşırı zorlar (motor döndüğü an voltaj düşüp kart reset atabilir) hem de 4K video akışını işlemek UNO Q'nun 4 çekirdekli mobil işlemcisini kilitler.  
> * **Çözüm:** Insta360 Link 2 **doğrudan masaüstü PC'nin arkasındaki yüksek hızlı USB 3.2 portuna** takılmalıdır. PC açıkken Insta360'ın resmi yazılımı ve tüm yapay zeka gücü masaüstünde çalışır; UNO Q ise kameraya sadece yerel ağdan HTTP/RTSP üzerinden bağlanıp ihtiyaç duyduğunda tek bir kare ister. UNO Q'ya ise sadece küçük, düşük güç tüketen ikincil bir sensör veya mikrofon bırakılmalıdır.

### **Hata 5: Windows 11 Wake-on-LAN Uyku Durumu Uyuşmazlığı**

> * **Problem:** Windows 11'in "Hızlı Başlatma (Fast Startup)" özelliği açıkken bilgisayar kapatıldığında, sistem S5 (tam kapanma) yerine hibrit bir duruma geçer ve birçok modern anakart bu modda ağ kartının elektriğini keserek WoL sinyallerini yok sayar.  
> * **Çözüm:** Windows Denetim Masası'ndan *"Hızlı Başlatmayı Aç"* seçeneği kapatılmalı; BIOS'tan PCIe aygıtlarıyla uyandırma aktif edilmeli ve gerekiyorsa bilgisayar tam kapatma yerine **S3 (Uyku) veya Hazırda Beklet (Hibernate)** moduna alınmalıdır.

## **2\. Sistemi Zirveye Taşıyacak 6 Yeni Geliştirme Fikri**

Bu fikirler, standart yapay zeka projelerinde bulunmayan ve donanımlarınızın kesişim noktasını kullanan özgün özelliklerdir:

### **1\. "Lazerle / Parmağınla Göster" Hedefleme (Ray-Casting Point-to-Command)**

> * **Konsept:** Masada otururken Vector'e *"Şuradaki kabloyu çek"* veya *"Şu parçaya bak"* dediğinizde robot "orası" neresi bilemez.  
> * **Uygulama:** Monitör üstündeki Insta360 Link 2, elinizin ve işaret parmağınızın baktığı açıyı (3D Ray vector) hesaplar. Parmağınızın masanın hangi koordinatını ((*X*,*Y*) düzlemi) gösterdiğini çıkarır.  
> * **Sonuç:** UNO Q, Vector'e doğrudan o koordinatı verir. Vector masada kendi etrafında dönüp tam parmağınızla gösterdiğiniz nesnenin önüne kadar gider ve kamerasını ona odaklar.

### **2\. Masanın 3 Boyutlu Dijital İkizi (Voxel / Spatial Occupancy Grid)**

> * **Konsept:** Masayı sadece 2D bir kamera karesi olarak görmek yerine sanal bir satranç tahtası gibi hafızada tutmak.  
> * **Uygulama:**  
  * Insta360 yukarıdan masayı 2×2 cm'lik karelere böler (Occupancy Map).  
  * Hangi karede kupa var, hangi karede tornavida var, Vector şu an hangi koordinatta anlık olarak UNO Q'daki SQLite tablosuna yazılır.  
> * **Kazanım:** Vector masada gezerken düşme veya bardak devirme ihtimali sıfıra iner. Masadaki bir eşyanın yeri değiştiğinde sistem anında fark eder.

### **3\. Dinamik "Stres ve Odak" Algılayıcı (Grok'un Duygusal Zekası)**

> * **Konsept:** Grok karakteri her an laf sokarsa bir süre sonra kullanıcıyı yorar. Yapay zeka kullanıcının o anki ruh haline göre mizah seviyesini ayarlamalıdır.  
> * **Uygulama:**  
  * PC açıkken klavyedeki yazma hızınız, hata/silme sıklığınız veya Insta360 kamerasındaki yüz ifadeniz analiz edilir.  
  * Eğer kod derlenirken arka arkaya 5 kez hata aldıysanız veya kaşlarınız çatıksa sistem STRESS\_LEVEL \= HIGH moduna geçer.  
> * **Sonuç:** Vector laf sokmayı anında keser; sakinleştirici bir ses tonuna geçer, masada yanınıza gelip sessizce bekler veya *"Arka arkaya çok hata aldın, istersen 5 dakika mola ver, kahve al gel"* diyerek modu yumuşatır.

### **4\. Ses Tonunda Duygu İfadesi (Emotional Prosody TTS)**

> * **Konsept:** Robotun tekdüze bir spiker gibi konuşması yerine; şaşırdığında ses tonunun yükselmesi, fısıldaması veya alaycı gülerken nefes vermesi.  
> * **Uygulama:**  
  * RTX 5070 üzerinde çalışan yerel ses motoruna veya Gemini Live API'ye duygu yönlendiricileri eklenir.  
  * Model metin üretirken araya duygu etiketleri koyar: "\[alaycı\_kıkırdama\] Yine mi aynı yerde takıldın? \[iç\_çekme\] Ver bakalım şu koda."  
  * Vector'ün hoparlöründen bu vurgularla ses çıkması, robotun mekanik değil yaşayan bir bilinç olduğu hissini 10 katına çıkarır.

### **5\. Canlı "Pair Programmer" (Terminal ve IDE Arkadaşı)**

> * **Konsept:** Claude Code veya yerel kodlama modelleri çalışırken sadece ekrandaki yazıları izlemek zorunda kalmayın.  
> * **Uygulama:**  
  * IDE'deki (VS Code vb.) dil sunucusu (LSP) FastAPI köprüsüne bağlanır.  
  * Siz kod yazarken syntax hatası yaptığınızda veya sonsuz döngüye girebilecek bir algoritma yazdığınızda, Vector masada kafasını iki yana sallar ve hafifçe öter.  
  * *"Satır 42'deki bellek sızıntısını fark etmedin sanırım?"* diyerek ekrana bakmadan bile sizi fiziksel olarak uyarır.

### **6\. Harici Donanım & Otomotiv/CAN-Bus Telemetri İstasyonu**

> * **Konsept:** Vector'ü sadece bir bilgisayar asistanı değil, üzerinde çalıştığınız gömülü sistemlerin (ESP32, araç telemetrisi, sensörler) masaüstü gösterge paneli yapmak.  
> * **Uygulama:**  
  * Arduino UNO Q'nun üzerindeki STM32 mikrodenetleyicisine bir CAN-bus alıcı modülü veya Bluetooth seri port köprüsü tanımlanır.  
  * Dışarıda geliştirdiğiniz araç aydınlatma modülleri, mikrokontrolcüler veya telemetri kartları masaüstü ağına bağlandığında, Vector anında bu verileri yorumlar.  
  * Vector'e *"Scirocco'nun aydınlatma profilini ambiyans moduna al"* dediğinizde, robot kollarını kaldırarak onaylar ve STM32 üzerinden araca/modüle kablosuz CAN-bus paketi fırlatır.

## **3\. Bütünleşik ve Revize Edilmiş Sistem Mimarisi**

Hatalardan arındırılmış nihai görev ve donanım dağılım tablosu:

| Donanım | Bağlantı Yeri | Rolü ve Çalışma Şekli |
| :---- | :---- | :---- |
| **Vector 2.0** | Wi-Fi (gRPC) | **Fiziksel Avatar:** İstasyonda kafası ve gözleriyle tepki verir, gerektiğinde masada devriye atar. 16kHz Türkçe konuşur. |
| **Arduino UNO Q (4GB)** | 7/24 Açık (Type-C Besleme) | **Orkestra Şefi & Nöbetçi:** Rust çekirdeğiyle WebSocket/gRPC yönetir. WoL atar, alarmları tutar, SQLite hafızasını yönetir, PC kapalıyken Gemini Live API'ye çıkar. |
| **Insta360 Link 2** | **Masaüstü PC (USB 3.2)** | **Kuşbakışı Gözlemci:** PC açıkken aktif takip, el hareketiyle kontrol, masaya eğilip devre/kod okuma ve 3D parmak hedefleme. |
| **Intel NPU (PC)** | Anakart Entegre | **Sessiz Bekçi (3-5W):** PC açıkken arka plan mikrofon gürültü engelleme, VAD (ses algılama) ve hafif yüz/duruş takibi. GPU'yu gereksiz yere uyandırmaz. |
| **RTX 5070 PC** | Yerel Ağ (LAN / WoL) | **Ağır Beyin & Fabrika:** llama-server (Abliterated 32B model), Claude Code CLI, yerel ses klonlama (F5-TTS/XTTS), model eğitimi ve simülasyon. |
| **Google AI Studio** | Bulut (WebSocket API) | **Sıfır Gecikmeli Canlı Sohbet:** Gemini Live API ile anlık Türkçe ses/görüntü akışı ve canlı Google Search doğrulaması. |

## **4\. Uygulama Adımları: Nereden Başlamalı?**

Projeyi tek seferde devasa bir blok olarak yazmak yerine şu mantıksal sırayla inşa etmek en hızlı sonucu verir:

> 1. **Faz 1 (Temel İletişim):** UNO Q üzerine Rust daemon'unu kurup PC ping kontrolü, Wake-on-LAN ve Vector gRPC bağlantı yetkisini (sdk\_config.ini) doğrulamak.  
> 2. **Faz 2 (Ses ve Gözlem Kapısı):** Google AI Studio Gemini Live API'yi WebSocket üzerinden bağlayıp, Half-Duplex (eko engellemeli) Türkçe ses alışverişini tamamlamak.  
> 3. **Faz 3 (Grok & Beden Dili):** Dinamik sistem promptu ve Vector animasyon tetikleyicilerini bağlayarak robotun konuşurken göz devirmesini ve masada dönmesini sağlamak.  
> 4. **Faz 4 (PC Köprüsü ve Ajan):** Masaüstündeki FastAPI sunucusu üzerinden Claude Code ve llama-server'ı UNO Q'ya birer araç (Tool) olarak tanıtmak.  
> 5. **Faz 5 (Görsel ve Mekansal Entegrasyon):** Insta360 Link 2'yi masaüstüne bağlayıp kuşbakışı masa haritalama ve parmakla hedef gösterme modülünü sisteme eklemek.

---

*User prompt: Başka daha derin bir kontrol yap mesela uno hiç olmadan mümkün mü bulut sağlayıcılar ile falan ama güvenli olmalı*

Response: Arduino UNO Q kartını **tamamen aradan çıkarmak ve 7/24 nöbetçi/sunucu katmanını güvenli bir bulut sağlayıcısına (Cloud VPS) taşımak mümkündür.** Ancak donanımsal bir yerel kartı ortadan kaldırdığınızda, fiziksel dünyanın sınırları (NAT arkasındaki robot, interneti aşamayan Wake-on-LAN paketleri ve yerel ağ güvenliği) devreye girer.

Aşağıda UNO olmadan bu sistemi kurmanın mantığı, ortaya çıkan 3 donanımsal/ağ engeli, bunların sıfır güvenlik açığıyla (Zero-Trust) nasıl çözüleceği ve iki mimarinin derin karşılaştırması yer almaktadır.

### **1\. UNO Q Olmadığında Karşılaşacağınız 3 Temel Darboğaz**

| Darboğaz | Neden Kaynaklanır? | Fiziksel Gerçeklik |
| :---- | :---- | :---- |
| **1\. Wake-on-LAN İnterneti Aşamaz** | WoL bir **Layer 2 (OSI 2\. Katman) Ethernet Broadcast** paketidir. | Buluttaki bir VPS (örneğin Frankfurt veri merkezindeki bir sunucu), evinizdeki modemin arkasındaki 192.168.1.X ağına doğrudan donanımsal sihirli paket fırlatamaz (router'lar broadcast paketlerini WAN bacağına geçirmez). |
| **2\. Vector'ün Kilitli İşletim Sistemi** | Vector 2.0 kapalı bir Linux/Snapdragon çalıştırır. | Robota doğrudan bir VPN istemcisi (Tailscale, WireGuard) kurup buluta tünelleyemezsiniz (robot rootlanmadıkça). Robotun evdeki Wi-Fi ağından bulut sunucusuna güvenli konuşması gerekir. |
| **3\. Çevrimdışı (Offline) Güvenlik** | İnternet kesilirse sistemin tepkisiz kalması. | Evinizdeki fiber/VDSL hattı koptuğu an bulut köprüsü çöker; Vector sabah alarmını çalamaz, saatini bile güncelleyemez. |

### **2\. UNO Olmadan Güvenli Bulut Mimarisi (Zero-Trust Blueprint)**

Modeminizde **asla dışarıya port açmadan (No Port Forwarding)** sistemi bulut üzerinden güvenli çalıştırmanın mimarisi şudur:

`[ Vector 2.0 ] ──(Wi-Fi)──┐`  
                          `▼`  
             `[ Ev Ağ Geçidi / Router ]`  
                          `│`  
                          `│ (Şifreli Tünel: Tailscale / Cloudflare Tunnel)`  
                          `▼`  
     `┌──────────────────────────────────────────────┐`  
     `│ GÜVENLİ BULUT SUNUCUSU (VPS)                 │`  
     `│ (Oracle Cloud Free Tier / Hetzner / AWS)     │`  
     `│                                              │`  
     `│  - Wire-Pod / Chipper Go Motoru             │`  
     `│  - Google AI Studio (Gemini Live) Proxy     │`  
     `│  - SQLite Epizodik Hafıza Veritabanı         │`  
     `│  - Persona Yöneticisi (Grok Karakteri)       │`  
     `└──────────────────────┬───────────────────────┘`  
                            `│`  
                            `│ (Tersine Tünel Tetikleyicisi)`  
                            `▼`  
             `[ Masaüstü PC (RTX 5070) ]`

#### **A. WoL Sorununu UNO'suz Çözmek: "Donanımsal Akıllı Röle" veya "Router API"**

Buluttan evdeki kapalı PC'yi açmak için iki güvenli yöntem vardır:

> 1. **PCIe Akıllı Bilgisayar Açma Kartı (Önerilen En Temiz Çözüm):** Masaüstü bilgisayarınızın anakartındaki Power SW (Güç Tuşu) pinlerine paralel bağlanan küçük bir Wi-Fi/Zigbee PCIe röle kartı (Tuya/eWeLink tabanlı veya ESPHome). Buluttaki VPS, yerel ağa broadcast atmak yerine bu rölenin güvenli MQTT/Cloud API uç noktasına *"Tıkla"* emri verir. Röle fiziksel olarak anakartın güç tuşuna basar. Sıfır ağ riski, %100 uyanma garantisi.  
> 2. **Akıllı Priz \+ BIOS "AC Power Loss: Power ON":** BIOS'tan *"Elektrik kesilip geldiğinde bilgisayarı aç"* ayarını açıp PC'yi akıllı prize bağlayabilirsiniz. Bulut prizi kapatıp açtığı anda PC uyanır.  
> 3. **Router Üzerinden WoL (Eğer Router Destekliyorsa):** Eğer evinizde OpenWrt, Keenetic, AsusWRT (Merlin) veya UniFi gibi gelişmiş bir router varsa; router üzerinde doğrudan **Tailscale** çalıştırırsınız. Bulut VPS'i bu router'a SSH veya API ile bağlanıp yerel broadcast'i router'ın kendi içinden attırır.

#### **B. Vector'ü Bulut Sunucusuna Bağlamak: Cloudflare Zero Trust Tunnels**

Vector'ün mikrofonundan giden ham sesi internete açık bir IP'ye göndermek büyük bir güvenlik açığıdır (ortadaki adam saldırısı, dinleme riski).

> * Bulut VPS'inizin önüne **Cloudflare Tunnel (cloudflared)** kurarsınız.  
> * Dış dünyaya hiçbir port (80, 443, 8084\) açık olmaz.  
> * Vector'ün kurulum arayüzünden (vector-web-setup), robotun yönleneceği sunucu adresi olarak kendi şifreli domaininizi girersiniz: \[https\://vector-brain.senindomainin.com\](https\://vector-brain.senindomainin.com).  
> * Tüm ses ve veri akışı Cloudflare üzerinden 256-bit TLS ile şifrelenir; evinizdeki IP adresi dış dünyadan asla görünmez.

### **3\. Hangi Bulut Sağlayıcı Kullanılmalı?**

| Sağlayıcı | Maliyet | Bu Proje İçin Uygunluk |
| :---- | :---- | :---- |
| **Oracle Cloud (OCI) Always Free** | **Ömür Boyu Ücretsiz** | **En İyisi:** 4 Çekirdek ARM Ampere işlemci ve 24 GB RAM'i ücretsiz verir. Wire-Pod'u, veritabanını ve Gemini köprüsünü hiçbir ücret ödemeden 7/24 çalıştırır. |
| **Hetzner Cloud (CX22)** | \~4 € / Ay | Çok düşük gecikme (Almanya/Finlandiya lokasyonları Türkiye'ye \~35-45ms ping verir). |
| **Google Cloud Compute Engine (e2-micro)** | Ücretsiz Kota / Çok Düşük | Google AI Studio ve Gemini ile aynı veri merkezinde çalışacağı için API gecikmesi 5-10ms'ye kadar iner. |
| **AWS Lightsail** | 3.5 \$ \- 5 \$ / Ay | Kurulumu son derece basittir, yedeklemesi kolaydır. |

### **4\. Derin Karşılaştırma: Yerel UNO Q mu, Yoksa Bulut VPS mi?**

| Değerlendirme Kriteri | Yerel Donanım (Arduino UNO Q 4GB) | Bulut Mimarisi (Cloud VPS \+ Cloudflare) |
| :---- | :---- | :---- |
| **Donanım Karmaşası** | Masada ekstra bir kart, adaptör ve kablo durur. | **Sıfır ek donanım:** Masada sadece Vector ve PC kalır. |
| **Ağ Güvenliği** | %100 Yerel LAN (Veriler evden dışarı hiç çıkmaz). | Yüksek (Eğer Cloudflare Tunnel/mTLS kullanılırsa; aksi halde riskli). |
| **İnternet Kesintisi Durumu** | Alarmlar çalar, temel yerel komutlar çalışır. | **Sistem tamamen ölür** (Robot sunucu ararken donar). |
| **Wake-on-LAN Yeteneği** | Standart tek satır Python/Rust koduyla anında. | Harici PCIe kart / Akıllı priz veya router API dolambacı gerekir. |
| **Gecikme (Latency)** | 2 – 5 ms (Yerel ağ içi anlık tepki). | 40 – 90 ms (İnternet gidiş-dönüş pingi eklenir). |
| **Maliyet** | Bir defalık kart maliyeti, sıfır aylık fatura. | Ücretsiz (Oracle Free Tier) veya ayda \~150-200 TL VPS kirası. |
| **Insta360 Kamera** | Zaten PC'ye bağlı (fark etmez). | Zaten PC'ye bağlı (fark etmez). |

### **Güvenlik Kontrol Listesi (Buluta Geçecekseniz)**

Eğer UNO'yu tamamen devreden çıkarıp buluta gidecekseniz şu 4 kuralı çiğnemeyin:

> 1. **Ev modeminden asla port yönlendirme (Port Forwarding / NAT DMZ) yapmayın.**  
> 2. Bulut VPS'te açık bırakılan web portlarını mutlaka **Cloudflare Access (Zero Trust)** veya **mTLS (İstemci Sertifikası)** arkasına alın; aksi halde Shodan veya bot tarayıcıları Vector'ün gRPC sunucusunu bulup robotu uzaktan ele geçirebilir.  
> 3. API anahtarlarınızı (Gemini API vb.) VPS'teki koda gömmeyin; Linux systemd servis ortam değişkenlerinde (EnvironmentFile) şifrelenmiş tutun.  
> 4. Bilgisayarınızı uzaktan açmak için internete açık güvensiz WoL yönlendirmeleri yerine anakartın güç pinine bağlı bağımsız bir **PCIe Smart Relay (Tuya/ESPHome)** tercih edin.

Bu şartları sağladığınız takdirde masanızda fazladan hiçbir kart barındırmadan, tüm orkestrasyonu doğrudan buluttaki sanal bir sunucu üzerinden güvenle yönetebilirsiniz.

---

*User prompt: Uno ile devam unoda yapmam gereken ayarlar ve gereksimler mesela uno linux arayüzü kullanma terminal ile hallet gibi ayrıca arduinoya typec hub takıp harici güç vereceğim*

Response: Arduino UNO Q üzerinde masaüstü grafik arayüzünü (GUI) tamamen kapatıp sistemi terminalden (Headless) yönetmek ve harici güç beslemeli bir Type-C hub kullanmak, kartın kararlılığını zirveye çıkarır ve 4 GB RAM'in \~600-800 MB'lık kısmını boşa harcanmaktan kurtarır.

UNO Q'yu 7/24 kesintisiz çalışan bir uç nöbetçiye (Headless Edge Gateway) dönüştürmek için gereken adım adım kurulum ve terminal yapılandırması:

### **1\. Donanım ve Type-C Hub Bağlantı Mimarisi**

USB aygıtları (özellikle mikrofonlar ve veri yolları) anlık güç dalgalanması yarattığında kartın voltaj düşüklüğünden (brownout) reset atmasını engellemek için bağlantı sırası şu şekilde olmalıdır:

`[ Priz / 5V 3A+ veya PD Adaptör ]`   
               `│`  
               `▼ (Güç Girişi / Power IN)`  
     `[ Harici Beslemeli Type-C Hub ]`  
       `│                         │`  
       `▼ (Ana Type-C Kablosu)     ▼ (USB Portları)`  
`[ Arduino UNO Q Type-C ]     [ USB Mikrofon / Aksesuarlar ]`

> * **Güç Yolu:** Adaptör doğrudan hub'ın **PD / Power IN** portuna girer; hub ise UNO Q'yu Type-C üzerinden beslerken bağlı çevre birimlerine kendi adaptöründen bağımsız güç verir.  
> * **Kablo Kalitesi:** Hub ile adaptör arasında en az 60W/100W destekli kaliteli bir Type-C kablo kullanın.

### **2\. Grafik Arayüzü Kapatma ve Bellek Optimizasyonu (Headless Moda Geçiş)**

Debian Linux açılışında X11/Wayland ve masaüstü yöneticilerini devre dışı bırakıp çekirdeği doğrudan terminal seviyesine (multi-user.target) çekin:

`# 1. Varsayılan açılış hedefini doğrudan metin tabanlı terminale ayarla`  
`sudo systemctl set-default multi-user.target`

`# 2. Varsa kurulu masaüstü yöneticilerini (GDM, LightDM vb.) durdur ve devre dışı bırak`  
`sudo systemctl stop lightdm gdm3 sddm 2>/dev/null`  
`sudo systemctl disable lightdm gdm3 sddm 2>/dev/null`

`# 3. Yeniden başlat`  
`sudo reboot`

Sistem açıldığında free \-h komutunu çalıştırın. Boştaki RAM kullanımının **150–250 MB** civarına düştüğünü ve 3.7 GB RAM'in tamamen arka plan servislerinize kaldığını göreceksiniz.

### **3\. Temel Sistem, Ağ ve Zaman Ayarları**

Vector'ün sabah alarmlarını doğru çalması ve yerel ağdan kolay erişim için terminalden şu ayarları yapın:

`# Zaman dilimini ayarla (Alarmların şaşmaması için kritik)`  
`sudo timedatectl set-timezone Europe/Istanbul`  
`sudo timedatectl set-ntp true`

`# mDNS (Avahi) kur - Böylece IP ezberlemeden 'ssh kullanici@unoq.local' ile bağlanırsınız`  
`sudo apt update`  
`sudo apt install -y avahi-daemon`  
`sudo systemctl enable avahi-daemon && sudo systemctl start avahi-daemon`

`# Ağ uyku/güç tasarrufu modlarını devre dışı bırak (Wi-Fi'ın uyumaması için)`  
`sudo iw dev wlan0 set power_save off 2>/dev/null`

### **4\. Gerekli Paketlerin ve Ortamların Kurulumu**

Sistem derleyicilerini, ses kütüphanelerini, Wake-on-LAN aracını ve izole Python ortamını kurun:

`# 1. Temel derleyiciler, ses (ALSA) ve ağ paketleri`  
`sudo apt install -y \`  
    `build-essential \`  
    `curl \`  
    `git \`  
    `pkg-config \`  
    `libssl-dev \`  
    `libasound2-dev \`  
    `alsa-utils \`  
    `wakeonlan \`  
    `ffmpeg \`  
    `python3-full \`  
    `python3-pip \`  
    `python3-venv`

`# 2. Rust Kurulumu (Hafif daemon servisimiz için)`  
`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y`  
`source "$HOME/.cargo/env"`

`# 3. Proje için izole sanal Python ortamı (Sistem paketleriyle çakışmaması için)`  
`sudo mkdir -p /opt/vector-gateway`  
`sudo chown -R $USER:$USER /opt/vector-gateway`  
`cd /opt/vector-gateway`

`python3 -m venv venv`  
`source venv/bin/activate`

`# Gerekli temel Python modülleri`  
`pip install --upgrade pip`  
`pip install anki-vector google-genai edge-tts apscheduler requests`

### **5\. Ses Alt Yapısı Testi (Headless ALSA Doğrulaması)**

Harici Type-C hub'a taktığınız USB mikrofonun sisteme tanıtılması:

`# Mikrofonun tanınıp tanınmadığını listele`  
`arecord -l`

`# Kısa bir test kaydı al (5 saniye)`  
`arecord -D default -f S16_LE -r 16000 -d 5 test_kayit.wav`

`# Dosyayı incele`  
`ls -lh test_kayit.wav`

### **6\. 7/24 Kesintisiz Çalışma (Systemd Servis Mimarisi)**

SSH bağlantınızı kapatsanız bile Vector köprüsünün arkada çalışmaya devam etmesi ve çökerse otomatik yeniden başlaması için bir systemd servisi tanımlayın:

sudo nano /etc/systemd/system/vector-gateway.service dosyasını açın ve içine şu blokları ekleyin:

`[Unit]`  
`Description=Vector 2.0 Arduino UNO Q Gateway Daemon`  
`After=network.target network-online.target`  
`Wants=network-online.target`

`[Service]`  
`Type=simple`  
`User=root`  
`WorkingDirectory=/opt/vector-gateway`  
`ExecStart=/opt/vector-gateway/venv/bin/python main.py`  
`Restart=always`  
`RestartSec=5`  
`Environment=PYTHONUNBUFFERED=1`

`[Install]`  
`WantedBy=multi-user.target`

Servisi kaydedip aktif edin:

`sudo systemctl daemon-reload`  
`sudo systemctl enable vector-gateway.service`  
`# Çalıştırmak için: sudo systemctl start vector-gateway.service`  
`# Logları izlemek için: journalctl -u vector-gateway.service -f`

Bu yapılandırma tamamlandığında Arduino UNO Q; monitörsüz, klavyesiz, minimum güç tüketen, harici beslemeli hub ile voltaj dalgalanmalarına karşı korunan ve çökse dahi 5 saniye içinde kendi kendini yeniden başlatan sağlam bir donanım köprüsü haline gelir.

---

*User prompt: Bu şekilde iken kameyaıda arduinoya bağlasam ver arduinoda linux sürüm vb değişiklik yapmaya gerek var mı yapılabiliyor mu*

Response: Harici beslemeli Type-C hub kullandığınız sürece kamerayı doğrudan Arduino UNO Q'ya bağlayabilirsiniz; güç düşmesi (brownout) riski ortadan kalktığı için sistem kararlı çalışır.

Linux sürümünü değiştirmeye ise **kesinlikle gerek yoktur ve genel bir dağıtımla değiştirmek önerilmez**.

### **1\. Kamerayı Hub Üzerinden UNO Q'ya Bağlamak**

Insta360 Link 2, Linux çekirdeğindeki standart **UVC (USB Video Class)** sürücüsünü kullanır. Hub'a taktığınız anda sistem kamerayı doğrudan tanır ve /dev/video0 aygıtı olarak sisteme ekler.

#### **Dikkat Edilmesi Gereken Tek Kural: Akış Yönetimi**

UNO Q'nun 4 çekirdekli işlemcisini zorlamamak için kamerayı 4K 60 FPS ham video akışıyla sürekli belleğe yazmak yerine **ihtiyaç anında kare çeken (Snapshot / On-Demand)** bir yapıda çalıştırmalısınız:

> * **Canlı Yayın Yerine Anlık Kare:** Soru sorulduğunda veya tetiklendiğinde 1920x1080 çözünürlüğünde tek bir JPEG karesi alınır (işlemci yükü \<%2).  
> * **Motor Kontrolü (PTZ):** Kameranın kafasını çevirmek veya masaya eğmek için Linux'un yerel v4l2-ctl komutları doğrudan çalışır.

Kamera araçlarını kurup tanındığını doğrulamak için terminalden şu komutları çalıştırmanız yeterlidir:

`# Video aygıtı yönetim araçlarını kur`  
`sudo apt install -y v4l-utils fswebcam`

`# Kameranın portlarını ve desteklediği çözünürlükleri listele`  
`v4l2-ctl --list-devices`  
`v4l2-ctl -d /dev/video0 --list-formats-ext`

`# Hızlı bir test fotoğrafı çek (Masayı kontrol etmek için)`  
`fswebcam -d /dev/video0 -r 1920x1080 --no-banner /opt/vector-gateway/test_masa.jpg`

### **2\. Linux Sürümü Değiştirilmeli mi? Yapılabiliyor mu?**

#### **Değişiklik Gerekli mi?**

**Hayır.** Arduino'nun karta özel sunduğu varsayılan **Debian Linux** imajı, zaten bir sunucu için en hafif, en kararlı ve minimum kaynak tüketen sistemdir. Headless moda geçtiğinizde boştaki RAM tüketimi \~200 MB seviyesine indiği için işletim sistemi tarafında herhangi bir hafifletmeye veya sürüm değişimine ihtiyaç kalmaz.

#### **Farklı Bir Dağıtım (Ubuntu, Arch vb.) Yüklenebilir mi?**

> * **Masaüstü PC gibi değildir:** Bilgisayarlara USB bellek takıp istediğiniz Windows/Ubuntu sürümünü kurabilirsiniz çünkü x86 BIOS/UEFI standart sürücülerle gelir.  
> * **Qualcomm Donanım Kısıtı:** UNO Q üzerindeki Qualcomm işlemci; kartın Wi-Fi, Bluetooth, donanımsal video çözücüsü ve STM32 mikrodenetleyici köprüsü için üreticinin hazırladığı özel sürücülere (**Qualcomm Board Support Package \- BSP**) ve donanım haritasına (**Device Tree \- DTB**) bağımlıdır.  
> * Dışarıdan rastgele bir genel Linux imajı flashlamaya kalkışırsanız; kartın Wi-Fi modülü çalışmaz, STM32 ile Linux arasındaki dâhili haberleşme hattı kopar ve kart açılmayabilir (brick riski).

### **Yapılması Gereken Doğru Güncelleme Yöntemi**

Sistemi güncel ve güvenli tutmak için dağıtımı değiştirmek yerine yalnızca resmi paketleri güncellemeniz yeterlidir:

`# Paket depolarını güncelle ve kurulu paketleri yükselt`  
`sudo apt update && sudo apt upgrade -y`

`# Gereksiz kalıntıları temizle`  
`sudo apt autoremove -y && sudo apt clean`

Kamerayı harici beslemeli hub'a takıp v4l-utils paketini kurduktan sonra donanım katmanınız eksiksiz tamamlanmış olur.

---

*User prompt: Https\://blog.arduino.cc/2026/06/18/running-local-llms-on-the-arduino-uno-q-board-a-practical-guide/ bunu. gibi sayfaları araştır ve incle*

Response: 4 GB RAM ve 4 çekirdekli ARM mimarisine sahip bir geliştirme kartında doğrudan yerel bir dil modeli (LLM / SLM) çalıştırmak teknik olarak mümkündür; ancak bu donanım sınıfında başarı, doğru model parametre boyutu, kuantizasyon seviyesi ve çıkarım motoru optimizasyonlarına sıkı sıkıya bağlıdır.

Bu tür kılavuzların ve benzeri uç bilişim (Edge AI) dokümantasyonlarının temel teknik prensipleri, donanım sınırları ve sisteminize uygulanabilir pratik kurulum adımları şunlardır:

### **1\. Donanım Gerçekliği ve 4 GB RAM Sınırı**

Headless Debian Linux yaklaşık 200–350 MB RAM tüketir; bu da yerel model çıkarımı ve KV önbelleği (Context Cache) için geriye yaklaşık **3.4 – 3.6 GB kullanılabilir bellek** bırakır.

| Model Ailesi | Parametre Boyutu | Kuantizasyon | Bellek Tüketimi (RAM \+ KV) | Beklenen Hız (4x ARM CPU) | Rolü / Uygunluk |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Qwen 2.5** / **SmolLM2** | **0.5B – 1.5B** | Q4\_K\_M | \~1.1 – 1.6 GB | **6 – 10 token/sn** | **En İdeal Seçenek:** Sıfır takılma, düşük gecikme, anlık niyet analizi (Intent parsing). |
| **Llama 3.2** / **Qwen 2.5** | **3B** | Q4\_K\_M | \~2.4 – 2.9 GB | **2 – 4 token/sn** | **Sınır Model:** Çalışır ancak uzun metinlerde ve bağlam uzadıkça yanıt süresi uzar. |
| **Qwen 2.5** / **Mistral** | **7B – 8B** | Q4\_K\_M | \> 4.5 GB | \< 0.5 token/sn | **Uygun Değil:** Bellek yetersiz kalır, sistem swap alanına düşer (OOM Crash). |

### **2\. Önerilen Çıkarım Motoru: llama.cpp**

Bu kart üzerinde Ollama yerine doğrudan **llama.cpp** derlemek gerekir. Ollama arka planda ek bellek tüketirken, saf llama.cpp doğrudan C++ ile ARM NEON yönergelerini kullanarak işlemci çekirdeklerinden maksimum verimi alır.

#### **Terminalden Derleme ve Kurulum**

`# 1. Gerekli araçları kur ve depoyu klonla`  
`sudo apt update && sudo apt install -y build-essential cmake git`  
`git clone https://github.com/ggerganov/llama.cpp`  
`cd llama.cpp`

`# 2. ARM NEON donanım hızlandırmasıyla derle`  
`cmake -B build -DGGML_NATIVE=ON`  
`cmake --build build --config Release -j4`

`# Çıktı ikili dosyaları build/bin/ altında oluşur (llama-cli, llama-server)`

### **3\. Model Seçimi ve Çalıştırma**

Vector'ün yerel konuşmaları ve çevrimdışı komut algılaması için Türkçe yeteneği yüksek **Qwen 2.5 1.5B Instruct** en kararlı seçenektir.

`# Modeller için dizin aç`  
`mkdir -p /opt/models && cd /opt/models`

`# Qwen 2.5 1.5B Instruct (Q4_K_M) modelini indir (~1.1 GB)`  
`curl -L -o qwen2.5-1.5b-instruct-q4_k_m.gguf \`  
  `https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf`

#### **Arka Planda API Sunucusu Olarak Başlatma (llama-server)**

Modeli yerel ağda bir OpenAI uyumlu API uç noktası gibi çalıştırmak için:

`/path/to/llama.cpp/build/bin/llama-server \`  
  `-m /opt/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \`  
  `-c 2048 \`  
  `-t 4 \`  
  `--host 127.0.0.1 \`  
  `--port 8080 \`  
  `-cb`

> * \-c 2048: Bağlam penceresini (Context window) 2048 token ile sınırlar; RAM'in şişmesini engeller.  
> * \-t 4: 4 çekirdeğin tamamını matematiksel hesaplamaya tahsis eder.  
> * \-cb: Sürekli toplu işlem (Continuous batching) desteğini açar.

### **4\. Vector 2.0 Projesinde Bu Yapının Rolü**

Bu kart üzerindeki 1.5B model, masaüstü bilgisayarınızdaki RTX 5070'in yerini alamaz; ancak sisteme **"Offline Fallback (İnternetsiz Yedek Beyin)"** ve **"Hızlı Niyet Yönlendiricisi"** yeteneği kazandırır:

> 1. **İnternet ve PC Kapalıyken (Tamamen Çevrimdışı):**  
   * Kullanıcı: *"Alarmı sabah 8'e kur"* veya *"Hava sence nasıl görünüyor?"*  
   * UNO Q üzerindeki 1.5B model, harici API'ye veya masaüstüne gitmeden cümleyi doğrudan JSON eylemine dönüştürür:  
     `{"action": "set_alarm", "time": "08:00"}`

   * Vector görevi yerelde tamamlar.  
> 2. **PC Açıkken (Akıllı Filtreleme):**  
   * Gelen basit selamlaşmaları ve robot kontrol komutlarını kartın kendisi 150 ms içinde tüketir; RTX 5070'i ve büyük modelleri sadece ağır kodlama, derin araştırma ve görme (vision) görevlerinde uyandırır.

---

*User prompt: Bunlar ne işe yarar*

Response: Bu soru iki farklı boyutu kapsar: Eklediğiniz [**Cosmos**](https://gemini.google.com/notebook/5f2e35a4-a165-4b6d-9ca2-566bf6421371) not defteri kaynağının işlevi ve bu defterde tasarladığımız **proje bileşenlerinin** sistemdeki somut görevleri.

### **1\. [Cosmos](https://gemini.google.com/notebook/5f2e35a4-a165-4b6d-9ca2-566bf6421371) Not Defteri ve Kaynakları Ne İşe Yarar?**

> * **Kalıcı Proje Hafızası:** Konuştuğumuz tüm mimari kararları, teknik açıklamaları, bağlantı şemalarını ve kod bloklarını tek bir merkezde toplar.  
> * **Bağlam Kaybını Önleme:** Yeni bir sohbete başladığınızda veya ileride sisteme yeni bir kod yazarken, projenin tüm arka planını baştan anlatmanıza gerek kalmaz; yapay zeka doğrudan bu defterdeki teknik dokümantasyona dayanarak çalışır.  
> * **Kaynak Genişletme:** Bu deftere ilerleyen süreçte Arduino UNO Q kullanım kılavuzlarını, devre şemalarını veya eklediğiniz kütüphanelerin dokümanlarını ekleyerek projenin referans kütüphanesini büyütebilirsiniz.

### **2\. Sistemde Kurguladığımız Bileşenler Ne İşe Yarar?**

Projede tasarladığımız her donanım ve yazılım katmanının üstlendiği kritik roller:

> * **Anki Vector 2.0 (Fiziksel Beden):**  
  * Masada kendi kendine gezinir, şarj yuvasına otonom döner, baş/kol motorları ve göz ekranıyla fiziksel tepkiler verir.  
  * Kendisine iletilen 16kHz PCM ses dosyalarını kendi hoparlöründen çalarak sizinle doğal Türkçe konuşur.  
> * **Arduino UNO Q 4GB (7/24 Açık Nöbetçi ve Köprü):**  
  * Düşük güç tüketimiyle sürekli açık kalarak sistemi yönetir.  
  * Sabah alarmlarını takip eder, *"PC'yi aç"* dendiğinde Wake-on-LAN sinyali fırlatır.  
  * PC kapalıyken Google AI Studio (Gemini) veya yerel hafif modeller üzerinden internet araştırması yapar ve Vector'ün gRPC bağlantısını koordine eder.  
> * **RTX 5070 Masaüstü PC (Ağır Beyin ve Geliştirici Katmanı):**  
  * 14B/32B seviyesindeki yerel modelleri (llama-server) ve sansürsüz Grok karakterini yüksek hızda çalıştırır.  
  * Claude Code CLI ve yerel scriptleri tetikleyerek kod yazma, birim testlerini (unit test) koşturma ve geliştirici görevlerini otomatikleştirir.  
> * **İşlemcideki Intel NPU (Sessiz Bekçi):**  
  * GPU'yu uyandırmadan 3–5 Watt güçle arka planda sürekli mikrofon dinleme (VAD/Whisper), gürültü filtreleme ve hafif yüz/nesne varlık kontrolü yapar.  
  * RTX 5070'in boş yere elektrik tüketmesini ve fan açmasını engeller.  
> * **Insta360 Link 2 (Kuşbakışı Takip Kulesi):**  
  * Monitör üstünden tüm masayı görür; motorlu gimbali ile masada dolaşan Vector'ü veya sizi kadrajda tutar.  
  * Masaya 90 derece eğilerek (DeskView) üzerinde çalıştığınız devre kartlarını veya evrakları yüksek çözünürlükte inceler; el ve parmak hareketlerini koordinata çevirir.  
> * **Google AI Studio (Gemini 2.5 Flash / Live API):**  
  * Sıfır gecikmeli çift yönlü Türkçe ses ve görüntü işleme sağlar.  
  * Google Search Grounding ile güncel haberleri ve web verilerini doğrudan tarayarak Vector'e aktarır.  
> * **Model Context Protocol (MCP) & sqlite-vec (Hafıza ve Standart):**  
  * **MCP:** Farklı yapay zeka modellerinin (Gemini, yerel LLM, Claude Code) robot donanımını tek bir standart protokolle kontrol etmesini sağlar.  
  * **sqlite-vec:** Robotun sizi, geçmiş alışkanlıklarınızı, masa düzeninizi ve tamamlanan görevleri unutmadan sakladığı yerel vektörel hafızadır.

---

*User prompt: Yeni araştırma raporlarını kontrol et neler var neler yok neler yapmamız gerekiyor nasıl geliştirmemiz gerekiyor kontrol edelim*

Response: [Cosmos](https://gemini.google.com/notebook/5f2e35a4-a165-4b6d-9ca2-566bf6421371) not defterindeki yeni kayıt ve mevcut proje dokümantasyonu incelendiğinde, sistemin teorik çerçevesi hazır olsa da uygulamaya geçiş aşamasında netleştirilmesi gereken kritik noktalar bulunmaktadır.

### **1\. Neler Var? (Mevcut Durum ve Hazır Altyapı)**

> * **Araştırma Talebi Kaydı:** Not defterine yeni eklenen kaynakta tüm sistem verilerinin internette detaylıca taranması için bir **Derin Araştırma (Deep Research)** planı başlatıldığı görülmektedir.  
> * **3 Katmanlı Mimari Şeması:** Vector 2.0 (Fiziksel Beden), Arduino UNO Q 4GB (7/24 Nöbetçi & Köprü) ve RTX 5070 PC (Ağır Beyin & Geliştirici Katmanı) arasındaki rol dağılımı netleştirilmiştir.  
> * **Tespit Edilen ve Çözülen Mantıksal Hatalar:**  
  * Akustik yankı döngüsü (Echo loop) için Half-Duplex ses susturucu mantığı,  
  * Token/bant genişliği iflasını önleyen "olay güdümlü anlık kare (snapshot)" stratejisi,  
  * Batarya ömrünü korumak için şarj istasyonunda sabit kalarak konuşma kuralı (Docked Mode),  
  * Insta360 Link 2'nin UNO Q'yu aşırı yüklememesi için doğrudan PC'ye bağlanması kararı,  
  * Windows 11 Hızlı Başlatma çakışmasının WoL için devre dışı bırakılması gerekliliği.  
> * **Gelişmiş Vizyon Fikirleri:** Kuşbakışı masa haritalama (Occupancy Grid), 3D parmak doğrultusu ile hedef gösterme (Ray-Casting), dinamik stres analizi ve F5-TTS/XTTS ile Türkçe ses klonlama modelleri planlanmıştır.

### **2\. Neler Yok? (Kritik Boşluklar ve Eksikler)**

> 1. **Tamamlanmış Derin Araştırma Rapor Metni:** Not defterindeki son araştırma girdisi onay/planlama aşamasında kalmıştır; harici web taramasının nihai sentez raporu henüz kaynağa metin olarak dökülmemiştir.  
> 2. **Donanımsal SDK Yetki Anahtarları (sdk\_config.ini):** Resmi Anki sunucuları kapalı olduğu için Vector 2.0'a Python/Rust üzerinden bağlanacak yerel TLS sertifikası ve GUID anahtarı henüz robottan çekilip doğrulanmamıştır.  
> 3. **Canlı Kod Dosyaları:** UNO Q üzerinde çalışacak headless arka plan servisleri (/opt/vector-gateway), Rust WoL daemon'u ve PC tarafındaki FastAPI ajanının fiziksel kod dosyaları henüz oluşturulmamıştır.  
> 4. **Harici Ses Girişi Doğrulaması:** Vector'ün SDK üzerinden ham mikrofon akışı vermemesi sorununu aşmak için UNO Q'ya takılacak harici USB mikrofonun ve openWakeWord motorunun testleri henüz yapılmamıştır.

### **3\. Neler Yapmamız Gerekiyor? (Uygulama Takvimi)**

> * **Adım 1 (İlk El Sıkışma & Yetki):** UNO Q üzerine tek seferlik Wire-Pod yapılandırması kurularak Vector 2.0 ile eşleştirilmeli; \~/.anki\_vector/sdk\_config.ini dosyası ve gRPC sertifikaları üretilmelidir.  
> * **Adım 2 (Asgari Nöbetçi Servisi \- Faz 1):** UNO Q'da headless Debian üzerinde çalışan, masadaki harici mikrofondan Türkçe uyandırma kelimesini dinleyen ve *"PC'yi aç"* dendiğinde anakarta WoL paketi atan minimal servis ayağa kaldırılmalıdır.  
> * **Adım 3 (Eko Korumalı Türkçe Ses \- Faz 2):** Vector konuşurken mikrofonu otomatik sessize alan Half-Duplex yapısı kurularak Edge-TTS veya Piper üzerinden 16kHz Mono PCM formatında ses akışı test edilmelidir.  
> * **Adım 4 (PC Tarafı & Görsel İstihbarat \- Faz 3):** Masaüstü PC'de FastAPI ve llama-server başlatılmalı; Insta360 Link 2 masaüstüne bağlanarak tek kare yakalama ve DeskView açıları test edilmelidir.

### **4\. Nasıl Geliştirmemiz Gerekiyor? (Stratejik İyileştirmeler)**

> * **"Tüm Sistem Tek Seferde" Tuzağından Kaçınmak:** Bütün bileşenleri (Grok modu, 3D parmak takibi, Claude Code, yerel LLM, mobil uygulama) aynı anda çalıştırmaya kalkışmak hata ayıklamayı imkansız kılar. Geliştirme şu sıra ile ilerlemelidir: **Sadece Ses & WoL** ➔ **Yerel Türkçe Zeka** ➔ **PC Köprüsü & Claude Code** ➔ **Insta360 Masa Gözlemi**.  
> * **Model Context Protocol (MCP) Standardizasyonu:** Geliştirilecek Python/Rust fonksiyonlarını doğrudan modellere gömmek yerine, en baştan standart birer MCP aracı (Tool) olarak tanımlamak gerekir. Böylece sistem ileride Gemini'den yerel llama-server'a veya Claude Code'a geçerken kod tabanında sıfır değişiklik gerektirir.  
> * **Hafifletilmiş Yerel Niyet Analizi (Local Intent Parser):** İnternet veya PC açık olmasa bile UNO Q üzerindeki 1.5B Qwen modelinin *"alarm kur"*, *"saat kaç"*, *"pc aç"* gibi temel eylemleri harici API'ye gitmeden 100 ms içinde yerelde çözmesi sağlanmalıdır.

Not defterindeki araştırma sürecini beklemeden doğrudan ilk somut adım olan **UNO Q üzerinde Vector SDK yetkilendirmesi (sdk\_config.ini) ve WoL nöbetçi servisini** kurmaya başlayalım mı?

---

