# Twitter Verisi Toplama Modülü

Bu modül, Twitter'dan belirli anahtar kelimelere göre tweet verilerini toplamak için kullanılır. Bu kod, Selenium WebDriver kullanarak Twitter'a giriş yapar, belirlenen tarih aralığında ve anahtar kelimelere göre tweet'leri toplar, ve verileri bir Excel dosyasına kaydeder. Bu kod, projenizde yer alan üç farklı kod modülünden sadece biridir.

## Gereksinimler

Bu kodun çalışabilmesi için aşağıdaki araçlara ve Python paketlerine ihtiyaç vardır:

- Python 3.x
- `pandas`
- `selenium`
- ChromeDriver veya GeckoDriver (Firefox için)
- Bir Twitter hesabı (kullanıcı adı ve şifrenizle giriş yapmanız gerekecek)
 
## Kurulum

Gereksinim duyulan Python paketlerini yüklemek için:

```bash
pip install pandas
pip install selenium
```

Ayrıca, tarayıcınız için uygun WebDriver'ı indirip sistem PATH'ine eklemelisiniz:

ChromeDriver
GeckoDriver (Firefox için)

## Kullanım
Bu modül, Twitter'dan belirli anahtar kelimelere göre tweet verilerini toplar ve bir Excel dosyasına kaydeder.

## Örnek Kullanım
Kodun çalıştırılması:

```bash
python twitter_scraper.py
```

## Parametreler
`subject`: Aranacak anahtar kelimeler veya kelime öbekleri (örneğin: "Turkcell" OR "Vodafone").
`start_date`: Aramanın başlangıç tarihi (örneğin: datetime(2024, 3, 24)).
`end_date`: Aramanın bitiş tarihi (örneğin: datetime(2024, 3, 25)).
`max_tweets`: Toplanacak maksimum tweet sayısı.
`kullanıcıAdı`: Twitter kullanıcı adınız.
`sifre`: Twitter şifreniz.
`output_file`: Toplanan verilerin kaydedileceği Excel dosyası (varsayılan: deneme.xlsx).

## Kullanım Adımları
Tarayıcıyı Seçin: Varsayılan olarak Firefox kullanılır. Eğer Chrome kullanmak isterseniz, `driver = webdriver.Chrome() `satırını aktif hale getirin.
Kullanıcı Bilgilerini Girin: `kullanıcıAdı` ve `sifre` değişkenlerine kendi Twitter kullanıcı adı ve şifrenizi girin.
Arama Parametrelerini Ayarlayın: `subject`, `start_date`, `end_date` ve `max_tweets` parametrelerini ihtiyacınıza göre ayarlayın.
Kodun Çalıştırılması: Yukarıdaki örnekte gösterildiği gibi Python scriptini çalıştırın.

## Açıklamalar
Selenium WebDriver: Bu modül, web tarayıcısı üzerinden otomasyon yaparak Twitter'dan veri toplamak için Selenium kullanır.
Tweet Toplama: Belirli anahtar kelimelere göre tweet'leri toplar ve bu tweet'leri Excel dosyasına kaydeder.
Dosya İşlemleri: Toplanan veriler, belirtilen Excel dosyasına eklenir veya yeni bir dosya oluşturulur.
Tarayıcı Desteği: Varsayılan olarak Firefox kullanılır, ancak Chrome için de destek sağlanmıştır.
