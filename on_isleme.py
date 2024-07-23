import pandas as pd
import re
import string
import nltk
from nltk.tokenize import word_tokenize
import jpype
from jpype import JClass, getDefaultJVMPath, startJVM, JString
import emoji

file_path = "veriSeti.xlsx"   #veri setininin yolunu belirtme
cleaned_csv_file_path = "temizlenmis.csv" #temizlenmiş veriyi kaydetmek için yolu belirtme
stop_words = "stop_words.txt"
filtered_csv_path = 'for_labelling_data.csv' # sadece text ve clear_text içeren yeni excel dosyasının yolu

#yapılması istenen işlemlere "True" yapılmaması için "False" yazılır
removeSpecialChars=False
removeLinks=True
removeHTML=True
removeHashtags=True
removePunctuation=True
removeExtraSpaces=True
removeAtSymbol=True
removeNumbers=False
removeRowMissingValue=True
removeRepeated = True
removeEmoji = True
tokenization = True
lemmatization = True
pos_tagging_enabled =True
removeStopWords = True


data = pd.read_excel(file_path)

# Kendi stop words dosyasını okuma
with open(stop_words, 'r', encoding='utf-8') as f:
    stop_words = set(f.read().splitlines())
    
# Sadece 'tweets' sütununu seçme
tweets_data = data[['Tweets']]
tweets_data.columns = ['text']  # Sütun adını 'text' olarak değiştirdik
 


def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')  # Emojileri boşlukla değiştirir

# Özel karakter listesine ekleme
special_punctuations = "’‘”“"
all_punctuations = string.punctuation + special_punctuations

# Temizlik fonksiyonu
def clean_text(text, removeSpecialChars, removeLinks, removeHTML, removeHashtags, removePunctuation, removeExtraSpaces, removeAtSymbol, removeNumbers, removeEmoji):
    # Küçük harfe çevirme
    text = text.lower()
    
    if removeSpecialChars:
        # Özel karakterleri kaldırma
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    if removeLinks:
        # Linkleri kaldırma
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    if removeHTML:
        # HTML etiketlerini kaldırma
        text = re.sub(r'<.*?>', '', text)
    
    if removeHashtags:
        # Hashtag'lerdeki # işaretini kaldırma
        text = text.replace('#', '')
    
    if removePunctuation:
        # Noktalama işaretlerini kaldırma (önce boşlukla değiştirir, sonra fazladan boşlukları kaldırır)
        text = re.sub(f"[{re.escape(all_punctuations)}]", ' ', text)
    
    if removeExtraSpaces:
        # Fazla boşlukları kaldırma
        text = re.sub(r'\s+', ' ', text).strip()
    
    if removeAtSymbol:
        # Etiketlerde @ işaretini kaldırma ama etiketleri tutma
        text = re.sub(r'@', '', text)
        
    if removeNumbers:
        #Sayıları kaldırmak için
        text = re.sub(r'\d+', '', text)

    if removeEmoji:
        text = remove_emojis(text)
        # Emojileri kaldırma
        
    return text

# Tokenizasyon fonksiyonu 
def tokenize_comment(text):
    return word_tokenize(text)

# Zemberek'i başlatma ve morfolojik analizciyi oluşturma
jpype.startJVM(classpath=['zemberek-full_old.jar'])
TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

# Kök bulma fonksiyonu
def find_roots(tokens):
    roots = []
    for token in tokens:
        analysis = morphology.analyzeAndDisambiguate(JString(token)).bestAnalysis()
        lemma = str(analysis[0].getLemmas()[0])
        if lemma == "UNK":
            lemma = token
        roots.append(lemma)
    return roots

# POS etiketleme fonksiyonu
def pos_tagging(tokens):
    pos_tags = []
    for token in tokens:
        analysis = morphology.analyzeAndDisambiguate(JString(token)).bestAnalysis()
        pos = str(analysis[0].getPos().getStringForm())
        pos_tags.append(pos)
    return pos_tags
    
# Stop words çıkarma fonksiyonu
def remove_stop_words(tokens, stop_words):
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens
    
# Entity listesi
entities = [
    "türk telekom", "turkcell", "vodafone", "türksat",
    "ulak", "superonline", "turknet", "bimcell", "pttcell", "ptt cell", "türktelekom", "turk cell", "voda fone", 
    "türk sat", "super online", "turk net"
]

# Entity'leri içermeyen yorumları kaldırma
def contains_entity(text):
    return any(entity in text for entity in entities)


# Temizleme işlemini uygulama
tweets_data['cleaned_text'] = tweets_data['text'].apply(lambda x: clean_text(x, removeSpecialChars, removeLinks, removeHTML, removeHashtags, removePunctuation, removeExtraSpaces, removeAtSymbol, removeNumbers, removeEmoji))

# Entity'leri içeren yorumları seçme
tweets_data = tweets_data[tweets_data['cleaned_text'].apply(contains_entity)]

if removeRepeated:
     # Tekrarlanan verileri kaldırma
     tweets_data.drop_duplicates(subset="text", keep="first", inplace=True)
     
if removeRowMissingValue:
     # Eksik değerleri kaldırma
     tweets_data.dropna(inplace=True)   
# Tokenizasyon işlemini uygulama
if tokenization:
    tweets_data['Tokens'] = tweets_data['cleaned_text'].apply(tokenize_comment)
    
# Kök bulma işlemini uygulama
if lemmatization:
    tweets_data['Roots'] = tweets_data['Tokens'].apply(find_roots)

# Stop words çıkarma 
if removeStopWords:
    # Stop words çıkarma işlemini uygulama
    tweets_data['Filtered_Tokens'] = tweets_data['Roots'].apply(lambda roots: remove_stop_words(roots, stop_words))  
     
# POS etiketleme işlemini uygulama
if pos_tagging_enabled:
    tweets_data['POS_Tags'] = tweets_data['Filtered_Tokens'].apply(pos_tagging)

# Temizlenmiş veriyi kaydetme
tweets_data.to_csv(cleaned_csv_file_path)

# `text` ve `Filtered_Tokens` (veya `clear_text`) sütunlarıyla yeni bir Excel dosyası oluşturma
tweets_data_label = tweets_data[['text', 'cleaned_text', 'Filtered_Tokens']]
tweets_data_label['clear_text_roots'] = tweets_data_label['Filtered_Tokens'].apply(lambda tokens: ' '.join(tokens))
tweets_data_label.drop(columns=['Filtered_Tokens'], inplace=True)
tweets_data_label.to_csv(filtered_csv_path, index=False)

# JVM'i kapatma
jpype.shutdownJVM()

