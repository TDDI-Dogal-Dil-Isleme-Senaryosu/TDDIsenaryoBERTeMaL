# Duygu Analizi ve Varlık Tanıma Modeli

Bu projede, Türkçe metinler üzerinde duygu analizi ve varlık tanıma (NER) işlemleri gerçekleştiren bir model geliştirilmiştir.

## Gereksinimler

Projenin çalıştırılması için aşağıdaki Python kütüphanelerine ihtiyaç vardır:

- pandas
- csv
- nltk
- spacy
- simpletransformers
- scikit-learn
- transformers
- jpype1

Gerekli kütüphaneleri kurmak için:

```bash
!pip install nltk spacy pandas simpletransformers scikit-learn transformers jpype1
```

Gerekli kütüphanelerin import edilmesi:

```bash
import nltk
import spacy
import pandas as pd
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from simpletransformers.ner import NERModel, NERArgs
from simpletransformers.classification import ClassificationModel, ClassificationArgs
from transformers import AutoModelForTokenClassification, AutoTokenizer, TrainingArguments, Trainer
import torch
from datasets import Dataset, load_metric
import jpype
from jpype import JClass, getDefaultJVMPath, startJVM
import csv
```

Aşağıdaki kodu çalıştırarak nltk'yı indirin:

```bash
nltk.download('punkt')
```

***

Kodumuzda lazım olan 'hepsi_birlestirilmis3.csv' dosyasına buradan erişebilirsiniz: etiketlenmis_dosya/hepsi_birlestirilmis3.csv

***

Kodumuzun ilk parçasında kaç tane pozitif, negatif ve nötr verimiz olduğu kontrol ediliyor. Bu aşama model eğitimi için gerekli değil. Kod şu şekilde:

```bash
df = pd.read_csv("hepsi_birlestirilmis3.csv", on_bad_lines='skip')
```

***

Kodumuzun ikinci parçasında import ettiğimiz csv dosyasıyla 'output_son.json' oluşturuluyor. Bu json dosyası bir sonraki aşamada lazım. Yine yukardaki ile aynı kod parçasını kullanarak import ediyoruz csv dosyasını.

***

Kodumuzun üçüncü parçasında önceki kodumuzdan elde ettiğimiz 'output_son.json' dosyasını import ediyoruz:

```bash
file_path = r"output_son.json"
```

Kodun sonucunda 'data.xlsx' dosyasını elde ediyoruz. Yine aynı şekilde bu dosyamızda bir sonraki kodumuzda lazım.

***

Kodumuzun dördüncü parçasında 'data.xlsx' dosyasını import ediyoruz:

```bash
df = pd.read_excel('data.xlsx')
```

Bu kodun çıktısı olarak da NER model çıktı sonuçlarını elde ediyoruz ve 'outputs' adlı bir dosya elde ediyoruz.

***

Kodumuzun beşinci parçasında yine 'hepsi_birlestirilmis3.csv' dosyasını import ediyoruz:

```bash
df = pd.read_csv("hepsi_birlestirilmis3.csv")
```

Bu kodun çıktısı olarak da Sentiment modelin çıktı sonuçlarını elde ediyoruz ve 'sentiment_model_output' adlı dosyayı elde ediyoruz.

***

Kodumuzun altıncı parçasında önceki kodlardan elde ettiğimiz 'outputs' ve 'sentiment_model_output' dosyalarını import ediyoruz:

```bash
ner_model = NERModel("bert", "/content/outputs", use_cuda=True)
sentiment_model = ClassificationModel("bert", "/content/sentiment_model_output", use_cuda=True)
```

Bu kodun çıktısında da eğittiğimiz iki modelin sonuçlarını kontrol ediyoruz. Model eğitimi için gerekli bir dosya değildir.






