# Test ve Doğrulama Raporu (TESTING.md)

Bu rapor, sistemin gerçek dünya verileri (PDF ve Görsel dökümanlar) üzerindeki performansını ve doğruluğunu kanıtlamak amacıyla hazırlanmıştır.

## 1. Fonksiyonel Test Senaryoları (Gerçek Veri Seti)

### Senaryo 1: Karmaşık Yerleşimli Görsel Analizi (volkan.PNG)
- **Veri Özelliği:** Metinlerin dağınık kutucuklar halinde bulunduğu, infografik yapısında bir görsel.
- **Test Sorusu:** "Dünyanın en büyük aktif yanardağı hangisidir ve nerededir?"
- **Beklenen Sonuç:** Görselin sağ alt ve orta kısımlarındaki parçalı bilgiyi birleştirerek "Mauna Loa - Hawaii" yanıtını vermesi.
- **Sonuç:** BAŞARILI. `EasyOCR` uzamsal gruplama (y_ths=0.5) sayesinde metin bütünlüğü korundu ve LLM doğru ilişkilendirme yaptı.

### Senaryo 2: İngilizce Teknik Terim ve Şema Analizi (renewable_energy.JPG)
- **Veri Özelliği:** "Solar", "Wind", "Hydroelectric" gibi İngilizce başlıklar ve teknik ikonlar içeren bir şema.
- **Test Sorusu:** "Görseldeki yenilenebilir enerji kaynakları nelerdir?"
- **Beklenen Sonuç:** İngilizce terimleri algılayıp kullanıcıya Türkçe olarak listelemesi.
- **Sonuç:** BAŞARILI. Model, "Güneş, Rüzgar, Hidroelektrik, Biyokütle ve Jeotermal" yanıtını vererek diller arası anlamsal eşleşmeyi başarıyla gerçekleştirdi.

### Senaryo 3: Çok Sayfalı Teknik Doküman Analizi (TUSAŞ_Urunleri.pdf)
- **Veri Özelliği:** HÜRKUŞ, KAAN, ANKA gibi ürünlerin teknik detaylarını içeren 3 sayfalık resmi döküman yapısı.
- **Test Sorusu:** "KAAN projesinin savunma sanayisindeki önemi nedir?"
- **Beklenen Sonuç:** PDF'in 3. sayfasındaki "modern hava kuvvetlerinin ihtiyaçlarını karşılama" ve "ileri teknoloji" vurgularını getirmesi.
- **Sonuç:** BAŞARILI. `PyMuPDF` ile sayfa bazlı metin çıkarımı hatasız yapıldı ve RAG yapısı ilgili sayfadaki doğru "chunk"ı (parçayı) bulup getirdi.

## 2. Sistem Dayanıklılık ve Sınır Testleri

**Halüsinasyon Denetimi** | Belgede geçmeyen uydurma bir sistem (Örn: "ANKA-Z projesinin önemi nedir?") soruldu. | "Bu bilgi yüklenen belgede bulunmamaktadır." | **PASSED** |
**Hafıza İzolasyonu** | Volkan görselinden sonra TUSAŞ dökümanı yüklendi. | Volkanlarla ilgili sorulara yanıt verilmedi, sadece yeni belgeye odaklanıldı. | **PASSED** |


## 3. Kullanıcı Deneyimi (UX) Doğrulaması
* **Soru Geçmişi Navigasyonu:** Sidebar üzerindeki geçmiş sorulara tıklandığında, ana paneldeki ilgili cevaba anlık ve pürüzsüz (smooth scroll) geçiş yapıldığı doğrulandı.
* **Geri Bildirim Döngüsü:** Yanıtlara verilen 👍/👎 oylarının `feedback_logs.json` dosyasına; soru, cevap ve zaman damgasıyla (timestamp) birlikte hatasız yazıldığı teyit edildi.
* **Mükerrer İşlem Engelleme:** Yanıt üretim aşamasında "Sor" butonunun kilitlendiği ve kullanıcının işlem bitmeden yeni bir sorgu gönderemediği doğrulandı.

## 4. Teknik Çıkarım
Yapılan testler sonucunda; sistemin **hibrit dilli (TR/EN)** dökümanlarda anlamsal bütünlüğü koruduğu, karmaşık mizanpajlı görsellerde yüksek doğrulukla çalıştığı ve kurumsal veri güvenliği standartlarına uygun olarak **oturum bazlı veri izolasyonu** sağladığı kanıtlanmıştır.