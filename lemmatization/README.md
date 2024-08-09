# Yorum İşleme ve Doğal Dil İşleme (NLP) Modülü

Bu modül, Türkçe metin verilerini işleyerek, lemmatizasyon, olumsuzluk analizi, özel kelime düzeltmeleri ve part of speech (POS) etiketlemesi gibi işlemleri gerçekleştirir. Bu kod, projenizde yer alan kod modüllerinden sadece biridir.

## Gereksinimler

Bu kodun çalışabilmesi için Python paketlerini aşağıdaki şekilde indirmeniz gerekmektedir:

```bash
pip install pandas
pip install jpype1
```

- **Zemberek Kütüphanesi:** Türkçe doğal dil işleme görevleri için kullanılan Zemberek kütüphanesine ihtiyaç vardır. Bu kütüphane, kelime analizi, yazım denetimi, lemmatizasyon ve part of speech (POS) etiketlemesi gibi işlemleri gerçekleştirmek için kullanılır.

[Buraya tıklayarak Zemberek Kütüphanesinin Github sayfasını ziyaret edebilirsiniz.](https://github.com/ahmetaa/zemberek-nlp?tab=readme-ov-file)
[Buraya tıklayarak da zemberek-full-old.jar dosyasının indirme linkine gidebilirsiniz.](https://drive.google.com/drive/folders/1FN80VbqesnqU21us4c4Pvgv2VqUsSf2z)

İndirdiğiniz `zemberek-full_old.jar` dosyasının path'ini unutmadan lemmatization.py kodu içindeki 
`ZEMBEREK_PATH` değişkenine atamayı unutmayın. 

## Kullanım
Bu kod parçası, Excel dosyalarındaki Türkçe metin verilerini işlemek için kullanılır. Metin verileri üzerinde aşağıdaki işlemler gerçekleştirilir:

Tokenization: Metin cümlelerini kelimelere ayırır.
Spell Check: Zemberek kütüphanesi ile yazım denetimi yapar ve özel düzeltmeler uygular.
Lemmatization: Kelimeleri köklerine ayırır ve gerekli düzeltmeleri yapar.
POS Tagging: Kelimelere part of speech (POS) etiketleri ekler.
Negation Handling: Olumsuzluk içeren kelimeleri işaretler ve yeniden yapılandırır.
Kodun sonunda işlenmiş veriler, belirtilen bir CSV dosyasına kaydedilir.

## Kodun Çalıştırılması

```python
python lemmatization.py
```

**Açıklamalar**
* Zemberek Kütüphanesi: Türkçe doğal dil işleme görevleri için kullanılan açık kaynak bir kütüphanedir. Bu projede Zemberek, kelime analizi ve yazım denetimi için kullanılmıştır.
* Özel Düzeltmeler: Kod içerisinde tanımlanan `custom_corrections` sözlüğü, Zemberek kütüphanesinin düzeltmediği kelimeleri manuel olarak düzeltmek için kullanılır.
* Stop Words ve Protected Words: Bu kodda kullanılan `stop_words.txt` ve `kelimeler.txt ` dosyaları, gereksiz kelimeleri çıkarmak ve korunması gereken özel kelimeleri belirlemek için kullanılır.
