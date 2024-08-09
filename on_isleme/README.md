# Tweet Temizleme ve Filtreleme Modülü

Bu modül, tweet verilerini temizlemek, tokenizasyon yapmak, stop words (durak kelimeler) çıkarmak ve belirli entity'leri içermeyen tweet'leri filtrelemek için kullanılır. Bu kod, projenizde yer alan üç farklı kod modülünden sadece biridir.

## Gereksinimler

Bu kodun çalışabilmesi için aşağıdaki Python paketlerine ihtiyaç vardır:

- `pandas`
- `nltk`
- `emoji`

Ek olarak, bu modül `stop_words.txt` dosyasını ve `veri.xlsx` dosyasını gerektirir.

## Kurulum

Gereksinim duyulan Python paketlerini yüklemek için:
```bash
pip install pandas
pip install nltk
pip install emoji
```

Ayrıca, `nltk` paketinde bulunan gerekli veri dosyalarını indirmek için aşağıdaki komutu çalıştırabilirsiniz:

```python
import nltk
nltk.download('punkt')
```

## Kullanım
Bu modül, bir Excel dosyasındaki tweet verilerini temizler ve işlenmiş sonuçları iki farklı CSV dosyasına kaydeder. Temizlik işlemleri isteğe bağlı olarak etkinleştirilebilir veya devre dışı bırakılabilir.

## Örnek Kullanım
Kodun çalıştırılması:

```python
python on_isleme.py
```


## Çıktılar
temizlenmis.csv: Temizlenmiş tweet verileri bu dosyaya kaydedilir.
for_labelling_data.csv: `text`, `cleaned_text`, ve stop words çıkartılmış `clear_text` sütunlarını içeren CSV dosyası.

## Açıklamalar

Tokenizasyon: Her bir tweet'i kelime düzeyinde parçalara ayırır.
Stop Words: Sıklıkla kullanılan ve anlamı zayıf olan kelimeleri metinden çıkartır.
Entity Filtreleme: Kod içinde tanımlı olan belirli entity'leri içermeyen tweet'leri filtreler

