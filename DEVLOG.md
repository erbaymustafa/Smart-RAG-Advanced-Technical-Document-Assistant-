# Geliştirme Günlüğü (DEVLOG)

## Başlangıç ve Mimari Kararlar
- Proje gereksinimleri analiz edildi. 
- **Karar:** Uygulamanın hızlı prototiplenmesi için `Streamlit`, LLM yönetimi için `LangChain` kullanılmasına karar verildi.
- **Karar:** Vektör veritabanı olarak hafif ve hızlı kurulumu nedeniyle `ChromaDB` seçildi.
- Geliştirme ortamı hazırlandı ve temel kütüphaneler yüklendi.

## Karşılaşılan Sorunlar ve Çözümler
- **Sorun:** Kütüphane kurulumu sırasında "OSError: [Errno 2] No such file or directory" (Windows Long Path) hatası alındı.
- **Neden:** Windows'un 260 karakterlik yol sınırı, derin öğrenme kütüphanelerinin (torch vb.) kurulumuna engel oldu.
- **Çözüm:** Windows Registry üzerinden `LongPathsEnabled` değeri 1 yapılarak sistem genelinde uzun dosya yolları aktif edildi ve kurulum başarıyla tamamlandı.

## OCR ve Metin İşleme Katmanı
- **Karar:** Resimlerden metin okuma (OCR) için açık kaynaklı ve yaygın kullanılan `pytesseract` kütüphanesi tercih edildi.
- **Karar:** PDF işleme için karmaşık yapıdaki (tablo, sütun vb.) belgeleri daha iyi ayrıştıran `UnstructuredPDFLoader` kullanıldı.
- **Teknik Detay:** TUSAŞ'ın gereksinimi olan Türkçe ve İngilizce dil desteği için `lang='tur+eng'` parametresi OCR motoruna eklendi.
- **Sorun:** Windows Path sorunları nedeniyle Streamlit doğrudan çalıştırılamadı, `python -m streamlit` komutu ile workaround uygulandı.

## Teknik Değişiklik ve Optimizasyon
- **Sorun:** `UnstructuredPDFLoader` kullanımında sistemde Poppler bağımlılığı nedeniyle `PDFInfoNotInstalledError` hatası alındı.
- **Analiz:** Poppler'ın Windows sistemlerine manuel kurulumunun deployment süreçlerini (ve son kullanıcı deneyimini) zorlaştıracağı öngörüldü.
- **Karar:** Bağımlılığı azaltmak ve daha hızlı performans elde etmek amacıyla PDF işleme motoru `PyMuPDF (fitz)` ile değiştirildi. 
- **Sonuç:** Ek sistem aracı gerektirmeyen, daha taşınabilir ve hızlı bir çözüm elde edildi. 

## OCR Katmanı Geliştirmesi
- **Sorun:** Tesseract OCR'ın sistem bağımlılıkları (PATH ayarları, harici binary gereksinimi) kurulum ve taşınabilirlik zorlukları yarattı.
- **Karar:** Daha modern, derin öğrenme tabanlı ve kurulumu kolay olan `EasyOCR` kütüphanesine geçiş yapıldı.
- **Gözlem:** EasyOCR'ın Türkçe karakter desteği ve düşük çözünürlüklü metinlerdeki performansı, Tesseract'a göre daha başarılı bulundu.
- **Teknik Detay:** GPU varsa otomatik algılaması sağlandı, yoksa CPU üzerinde stabil çalışacak şekilde konfigüre edildi.

## RAG Stratejisi ve Veri Parçalama (Chunking)
- **Teknik Uygulama:** Belgeler `RecursiveCharacterTextSplitter` ile **500 karakterlik** parçalara bölündü ve 50 karakterlik çakışma (overlap) payı bırakıldı.
- **Mantık:** - **Nokta Atışı Arama:** Sistem tüm dökümanı sırayla okumak yerine, vektör veritabanında (ChromaDB) soruyla en alakalı 500 karakterlik parçaları "mıknatıs gibi" çeker.
- **Performans:** Küçük parçalar sayesinde LLM'e (Llama 3) sadece ilgili veri gönderilerek "bağlam kirliliği" önlendi ve yerel donanım üzerindeki yük azaltıldı.
- **Bütünlük:** 50 karakterlik çakışma ile parçalar arasında anlamsal köprü kurularak bilgi kaybı engellendi.

## Teknik Sorun Giderme: LangChain Sürüm Uyumluluğu
- **Sorun:** `ModuleNotFoundError: No module named 'langchain.prompts'` hatası alındı.
- **Analiz:** LangChain'in v0.2+ sürümlerinde mimari değişikliğe gidildiği ve `prompts` modülünün `langchain-core` paketine taşındığı saptandı.
- **Çözüm:** Import yapıları `langchain_core.prompts` olarak güncellendi ve bağımlılıklar (requirements) bu doğrultuda revize edildi.

## Teknik Güncelleme: LangChain Expression Language (LCEL) Geçişi
- **Sorun:** `langchain.chains` modülünde `RetrievalQA` kullanımı sırasında import hataları yaşandı.
- **Analiz:** LangChain'in v0.2 sürümü ile birlikte klasik "Chain" yapılarının yerini daha esnek ve modüler olan LCEL (LangChain Expression Language) yapısına bıraktığı görüldü.
- **Karar:** Proje mimarisi daha modern, okunabilir ve hata ayıklaması kolay olan LCEL yapısına güncellendi. `RetrievalQA` yerine `RunnablePassthrough` ve `pipe (|)` operatörleri kullanılarak veri akışı (pipeline) yeniden tasarlandı.

## Teknik Dönüşüm: Streamlit'ten FastAPI'ye Geçiş
- **Neden:** Streamlit'in otomatik yeniden çalışma (re-run) mantığının karmaşık oturum yönetiminde veri tutarsızlıklarına yol açtığı gözlemlendi.
- **Karar:** Daha profesyonel, stabil ve kurumsal kimliğe uygun bir yapı için FastAPI (Backend) ve Bootstrap 5 (Frontend) mimarisine geçildi.
- **Sonuç:** Oturum yönetimi backend tarafında tam kontrol altına alınarak "eski belge verisinin kalması" sorunu kökten çözüldü.

## Teknik Sorun: Web Framework Geçişinde Nesne Uyumluluğu
- **Sorun:** Streamlit'ten FastAPI'ye geçişte `AttributeError: 'UploadFile' object has no attribute 'name'` hatası alındı.
- **Analiz:** Streamlit dosya yükleme nesnesinin meta verilerine `.name` ile erişirken, FastAPI/Starlette altyapısının `.filename` niteliğini kullandığı saptandı. Ayrıca FastAPI'nin dosya içeriğini bir "stream" (akış) olarak yönettiği gözlemlendi.
- **Çözüm:** `processor.py` içindeki dosya erişim mantığı `filename` ve `file.read()` metoduna göre güncellendi. Byte-stream verilerinin `io.BytesIO` ile işlenmesi sağlanarak bellek verimliliği artırıldı.

## Kullanıcı Deneyimi (UX) Optimizasyonları
- **Hata:** Yanıt süresi sırasında kullanıcının butona mükerrer basması sonucunda API kirliliği ve duplicate yanıtlar oluştuğu saptandı.
- **Çözüm:** JavaScript tabanlı "Button Disabling" ve "Loading Overlay" mekanizmaları eklendi. İşlem tamamlanana kadar girdi alanları kilitlenerek sistem kararlılığı sağlandı.
- **Mimari:** Soru geçmişinin takibi için sol sidebar yapısına geçilerek kurumsal dashboard görünümü elde edildi.

## Çok Dilli (Multilingual) Destek İyileştirmesi
- **Sorun:** İngilizce belgelerde Türkçe sorulara verilen yanıt isabet oranının düşük olduğu gözlemlendi.
- **Çözüm:** Prompt Engineering teknikleri kullanılarak LLM'e diller arası çeviri ve anlamsal eşleştirme talimatı verildi. LLM'in dilden bağımsız olarak bağlama odaklanması sağlandı.

## Vektör Veritabanı İzolasyonu ve Çakışma Çözümü
- **Sorun:** Ardışık belge yüklemelerinde ChromaDB'nin eski "collection" verilerini bellekte tuttuğu ve yeni yüklenen belge yerine eski belgeye göre yanıt verdiği (Data Leakage/Persistence issue) saptandı.
- **Analiz:** `Chroma.from_texts` metodunun varsayılan koleksiyon ismini kullanması nedeniyle verilerin üzerine yazılmak yerine append (ekleme) yapıldığı anlaşıldı.
- **Çözüm:** `uuid` kütüphanesi kullanılarak her belge yüklemesi için benzersiz (unique) bir koleksiyon ismi oluşturuldu ve işlem sonunda `delete_collection()` metoduyla bellek temizliği sağlandı.

## OCR Düzen (Layout) Problemlerinin Giderilmesi
- **Sorun:** Çok sütunlu veya kutucuklu görsellerde (örneğin Volkanlar infografiği) standart satır bazlı okumanın metin hiyerarşisini bozduğu gözlemlendi.
- **Çözüm:** 1. Metin kaymasını önlemek için EasyOCR motorunda `paragraph=True` ve `y_ths=0.5` parametreleri ile "Uzamsal Gruplama" uygulandı.
  2. LLM promptuna "OCR hatalarını ve kaymaları anlamsal olarak düzelt" talimatı (Heuristic Repair) eklenerek veri kalitesi artırıldı.

## Geri Bildirim Döngüsü ve Gelecek Projeksiyonu
- **Özellik:** JSON tabanlı, asenkron geri bildirim sistemi entegre edildi. Her yanıt `timestamp` ve kullanıcı değerlendirmesiyle (👍/👎) kaydedilir ve `datetime` entegrasyonu ile her işlem zaman damgalı olarak kaydedilmekte, `question-answer` bazlı kontrol ile mükerrer (duplicate) log oluşumu engellenmektedir.
- **Analiz Değeri:** Toplanan loglar, sistemin zayıf olduğu konuları tespit etmek (Gap Analysis) için kullanılır.
- **Stratejik Amaç:** Düşük puan alan yanıtların ileride yerel LLM (Llama 3) modelinin TUSAŞ teknik terminolojisine adapte edilmesi için yapılacak **Fine-tuning (RLHF)** çalışmalarında veri seti olarak kullanılması planlanmıştır.