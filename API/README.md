# FastAPI Tabanlı NER ve Sentiment Analizi API'si

Bu proje, BERT modellerini kullanarak adlandırılmış varlık tanıma (NER) ve duygu analizi (Sentiment Analysis) yapan bir FastAPI tabanlı web servisidir. Bu proje, daha büyük bir projenin 4. kod parçasıdır ve tek başına bir proje değildir.

## Gereksinimler

- Python 3.8 veya üstü
- FastAPI
- Uvicorn
- Transformers (Hugging Face)
- Torch

***

## Kurulum

1. Projeyi koymak istediğiniz dosya dizinine gittikten sonra projeyi klonlayın ya da indirin.

```bash
git clone https://github.com/TDDI-Dogal-Dil-Isleme-Senaryosu/TDDIsenaryoBERTeMaL.git
cd TDDIsenaryoBERTeMaL
```

2. Gerekli Python paketlerini yükleyin.

```bash
pip install fastapi uvicorn transformers torch
```

3. BERT modelleri ve tokenizer'ların yolunu `ner_model`, `ner_tokenizer`, `sentiment_model`, ve `sentiment_tokenizer `olarak belirtin.

***

## Kullanım
Aşağıdaki komutla FastAPI uygulamasını başlatabilirsiniz:

```bash
uvicorn api:app --host 0.0.0.0 --port 7777
```

Bu komut, API'yi yerel olarak `http://localhost:7777 `adresinde başlatacaktır.
Not: Port'u ve DNS'i değiştirmek isterseniz değiştirebilirsiniz 
Örneğin: 
`uvicorn api:app --host 1.1.1.1 --port 8888 `
Kodu da çalışacaktır.

***

## API Endpointleri
### /predict - POST
Bu endpoint, gönderilen metin üzerinden NER ve duygu analizi yapar.

***

### **İstek**
+ **Yöntem**: `POST`
+ **Gövde**: JSON formatında bir metin içermelidir.

```json
{
  "text": "Metin buraya gelecek"
} 
```

***

### Yanıt
+ **200 OK** - Başarılı isteklerde, tanınan varlıklar ve ilgili duygu etiketi döndürülür.

```json
{
  "entity_list": ["varlık1", "varlık2"],
  "results": [
    {"entity": "varlık1", "sentiment": "olumlu"},
    {"entity": "varlık2", "sentiment": "nötr"}
  ]
}
```

***

## Örnek İstek
Aşağıdaki gibi bir istekle API'yi test edebilirsiniz:

```bash
curl -X POST "http://localhost:7777/predict" -H "Content-Type: application/json" -d '{"text": "Merhaba dünya"}'
```

***

## Proje Yapısı
+ `main.py`: FastAPI uygulaması ve endpoint tanımları.
+ `ner_model/`: NER modelinin ve tokenizer'ının bulunduğu dizin.
+ `sentiment_model/`: Duygu analizi modelinin ve tokenizer'ının bulunduğu dizin.

## Notlar
+ Bu proje, daha büyük bir projenin parçasıdır ve diğer kodlarla birlikte çalışacak şekilde tasarlanmıştır.
+ BERT modelleri ve tokenizer'lar, daha önce eğitilmiş ve belirli dizinlerde saklanmıştır. Bu dosyaların doğru yollara yerleştirildiğinden emin olun.
+ Duygu etiketleri (olumlu, nötr, olumsuz) örnek olarak tanımlanmıştır. Kendi duygu etiketlerinizi kullanabilirsiniz.
