import cloudscraper

# Создание объекта cloudscraper
scraper = cloudscraper.create_scraper()

# Получение HTML-страницы
url = "https://tap.az/elanlar/dasinmaz-emlak/menziller"
response = scraper.get(url)

# Проверка статуса
print(response.text)