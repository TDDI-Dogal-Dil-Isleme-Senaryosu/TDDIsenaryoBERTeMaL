import pandas as pd
import time
from time import sleep
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Selenium WebDriver ile Chrome'u başlat
#driver = webdriver.Chrome()

#Firefox için alttaki satır kullanılabilir
driver = webdriver.Firefox()

# Twitter giriş sayfasına git
driver.get("https://twitter.com/login")

# Arama parametreleri
subject = '"Turkcell" OR "Vodafone" OR "Turknet" OR "TurkTelekom" OR "Türk Telekom" OR "Türksat" OR "SuperOnline" OR "Bimcell" OR "Pttcell" lang:tr'#subject = '"Turkcell" AND "Vodafone"' ikili de yazabiliriz
start_date = datetime(2024, 3, 24)  # Başlangıç tarihi
end_date = datetime(2024, 3, 25)     # Bitiş tarihi
max_tweets = 10000  # Maksimum tweet sayısı

kullanıcıAdı = ""
sifre = ''

# Kullanıcı adı ve şifre ile giriş yap
sleep(3)
username = driver.find_element(By.XPATH, "//input[@name='text']")
username.send_keys(kullanıcıAdı)
username.send_keys(Keys.RETURN)

sleep(3)
password = driver.find_element(By.XPATH, "//input[@name='password']")
password.send_keys(sifre)
password.send_keys(Keys.RETURN)
sleep(3)

# Arama URL'si oluşturma
search_url = f"https://twitter.com/search?q={subject}%20since%3A{start_date.strftime('%Y-%m-%d')}%20until%3A{end_date.strftime('%Y-%m-%d')}&src=typed_query"

# Arama sayfasına git
driver.get(search_url)
sleep(3)

# 'Latest' sekmesini tıklayın
latest_button = driver.find_element(By.XPATH, "//span[contains(text(),'Latest')]")
latest_button.click()
sleep(3)

# Arama sonuçlarının yüklenmesini bekleyin
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']")))

# Tweet verilerini toplama
Tweets = []
TimeStamps = []

# Daha fazla tweet yüklemek için aşağı kaydırma
SCROLL_PAUSE_TIME = 10
last_height = driver.execute_script("return document.body.scrollHeight")

tweet_count = 0
while tweet_count < max_tweets: #tweet_count < max_tweets tweet sayisini belitmek istersen bunu ekle true yerine
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    # Tweet verilerini toplama
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    for article in articles:
        try:
            TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
            tweet_date = datetime.strptime(TimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')  # Tarihi ayrıştırın

            # Tweet tarihi kontrolü
            if start_date <= tweet_date <= end_date:
                # Tweet metnini ve tarihini toplama
                try:
                    Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                    Tweets.append(Tweet)
                    TimeStamps.append(TimeStamp)
                except Exception as e:
                    print(f"Tweet metni alınırken hata oluştu: {str(e)}")
                
                tweet_count += 1
            if tweet_count >= max_tweets:  # Maksimum tweet sayısına ulaşılırsa
                break
            
        except Exception as e:
            print(f"Tweet toplanırken hata oluştu: {str(e)}")

# Yeni veriler için DataFrame oluşturma
new_data = pd.DataFrame({
    'TimeStamps': TimeStamps,
    'Tweets': Tweets
})

# Mevcut Excel dosyasına ekleme
output_file = "deneme.xlsx"

try:
    if os.path.exists(output_file):
        existing_data = pd.read_excel(output_file)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        combined_data = new_data

    # Excel dosyasına yazma
    combined_data.to_excel(output_file, index=False)
    
    # Excel dosyasını işletim sistemine göre açma
    if os.name == 'posix':  # Linux
        os.system(f'libreoffice "{output_file}" &')
    elif os.name == 'nt':  # Windows
        os.system(f'start excel "{output_file}"')

except Exception as e:
    print(f"Excel dosyasına yazarken hata oluştu: {str(e)}")

# Tarayıcıyı kapatma
driver.quit()

