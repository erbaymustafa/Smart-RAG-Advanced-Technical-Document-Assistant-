# Smart-RAG: Advanced Technical Document Assistant 

Bu proje; teknik dökümanları (PDF) ve infografik görselleri (JPG/PNG) analiz ederek kullanıcı sorularını yanıtlayan, tamamen yerel (local) kaynaklarla çalışan gelişmiş bir RAG (Retrieval-Augmented Generation) sistemidir. 

Proje, özellikle veri gizliliğinin kritik olduğu savunma ve havacılık gibi teknik sektörlerde, dökümanların dışarı çıkmadan analiz edilmesi ihtiyacına yönelik bir çözüm olarak geliştirilmiştir.

## ✨ Öne Çıkan Özellikler
- **Hibrit OCR Teknolojisi:** Derin öğrenme tabanlı `EasyOCR` ile karmaşık mizanpajlı görsellerden metin çıkarma.
- **Vektör Tabanlı Semantik Arama:** `ChromaDB` entegrasyonu ile 10.000+ satır arasından saniyeler içinde "nokta atışı" bilgi tespiti.
- **Strict Prompting:** Modelin döküman dışı bilgi üretmesini (hallucination) engelleyen sıkı talimat seti.
- **Asenkron Geri Bildirim:** Kullanıcı deneyimini iyileştirmek için JSON tabanlı loglama ve oylama sistemi.

---

## 🐳 Docker ile Hızlı Kurulum (Önerilen)

Sistemi herhangi bir bağımlılık yüklemeden saniyeler içinde ayağa kaldırabilirsiniz.

1.  **Ön Koşul:** Bilgisayarınızda [Ollama](https://ollama.com/) kurulu olmalı ve `llama3` modeli çekilmiş olmalıdır (`ollama run llama3`).
2.  **Kurulum:** Proje ana dizininde terminali açın ve şu komutu çalıştırın:
    ```bash
    docker-compose up --build
    ```
3.  **Erişim:** Tarayıcınızda `http://localhost:8000` adresine gidin.

---

## 🛠️ Manuel Kurulum (Alternatif)

1.  **Sanal Ortam:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    ```
2.  **Bağımlılıklar:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Çalıştır:**
    ```bash
    uvicorn src.main:app --reload
    ```

---

## 📁 Proje Mimarisi ve Dokümantasyon
- **`src/`**: Backend servisleri ve RAG boru hattı (Pipeline).
- **`templates/`**: Modern ve kullanıcı dostu arayüz dosyaları.
- **`DEVLOG.md`**: Geliştirme sürecindeki teknik kararlar ve karşılaşılan sorunların çözümü.
- **`TESTING.md`**: Sistemin doğruluğunu kanıtlayan gerçek veri seti test sonuçları.

---

## 🧪 Örnek Test Senaryoları
Sistemi test etmek için aşağıdaki veri setlerini kullanabilirsiniz:
1. **Teknik Şemalar:** Görsellerdeki yabancı terimleri anlık Türkçeye çevirerek analiz eder.
2. **Resmi Dökümanlar:** Çok sayfalı teknik raporlarda anlamsal bütünlüğü koruyarak cevap üretir.
3. **Güvenlik Testi:** Dökümanda yer almayan (Mars'ta hayat vb.) sorulara "bilgi bulunmamaktadır" yanıtını verir.

---
**Geliştirici:** Mustafa ERBAY