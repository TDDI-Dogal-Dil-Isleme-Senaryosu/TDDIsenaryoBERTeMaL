import pandas as pd
import re
import string
import nltk
from nltk.tokenize import word_tokenize
import emoji

file_path = "veri.xlsx"   #veri setininin yolunu belirtme
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
    
# Stop words çıkarma fonksiyonu
def remove_stop_words(tokens, stop_words):
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens
    
# Entity listesi
entities = [
    "kick-turkey","twitch", "nimo tv", "youtube gaming", "facebook gaming", "kickturkey", "kick türkiye", 
    "kick turkey", "twich",  "twtch", "nimo-tv", "nimotv", "youtube-gaming", "youtubegaming", "yt gaming", 
    "ytgaming", "facebookgaming", "facebook-gaming", "fb gaming", "fbgaming", "türk telekom", "turkcell", 
    "vodafone", "türksat", "superonline", "turknet", "bimcell", "pttcell", "ptt cell", "türktelekom", 
    "turk cell", "voda fone", "türk sat", "super online", "turk net", "türk hava yolları", 
    "pegasus hava yolları", "sunexpress", "anadolujet", "ajet", "thyao", "turkish airlines", "turkey airlines", 
    "pegasus airlines", "pgs", "sun Express", "güneş Express", "anadolu havayolları", "a-jet", "a jet", "thy"
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
    
# Stop words çıkarma 
if removeStopWords:
    # Stop words çıkarma işlemini uygulama
    tweets_data['Filtered_Tokens'] = tweets_data['Tokens'].apply(lambda tokens: remove_stop_words(tokens, stop_words))  
     
# Temizlenmiş veriyi kaydetme
tweets_data.to_csv(cleaned_csv_file_path)

# text ve Filtered_Tokens (veya clear_text) sütunlarıyla yeni bir Excel dosyası oluşturma
tweets_data_label = tweets_data[['text', 'cleaned_text', 'Filtered_Tokens']]
tweets_data_label['clear_text_without_stopwords'] = tweets_data_label['Filtered_Tokens'].apply(lambda tokens: ' '.join(tokens))
tweets_data_label.drop(columns=['Filtered_Tokens'], inplace=True)
tweets_data_label.to_csv(filtered_csv_path, index=False)

# JVM'i kapatma
jpype.shutdownJVM()

