
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_html(url, method="requests"):
    try:
        if method == "requests":
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            return response.text
        elif method == "cloudscraper":
            headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
              'Accept-Encoding': 'gzip, deflate',  # Поддержка сжатия
              'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',  # Эмуляция свежего запроса
              'Upgrade-Insecure-Requests': '1',  # Указывает, что клиент поддерживает переход на HTTPS
              'Sec-Fetch-Dest': 'document',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-Site': 'none',
              'Sec-Fetch-User': '?1',
            }
            
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, headers=headers)
            print(f"Status code:{response.status_code}")
            return response.text
        elif method == "selenium":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Без графического интерфейса
            driver = webdriver.Chrome(options=options)

            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'specific-class')))
            html = driver.page_source  # Получаем HTML после полной загрузки
            driver.quit()
            return html
    except Exception as e:
        print(f"Error fetching {url} with {method}: {e}")
        return None

def parse_site(url):
    # 1. Попробовать через requests
    html = fetch_html(url, method="requests")
    if html and "Cloudflare" not in html:
        return BeautifulSoup(html, "lxml")

    # 2. Если requests не сработал, попробовать cloudscraper
    html = fetch_html(url, method="cloudscraper")
    if html and "Cloudflare" not in html:
        return BeautifulSoup(html, "lxml")

    # 3. Если оба не сработали, использовать Selenium
    html = fetch_html(url, method="selenium")
    if html:
        return BeautifulSoup(html, "lxml")

    # 4. Если ничего не помогло
    print(f"Failed to parse {url}")
    return None

def parse_element(element, config):
    data = {}
    text = element.get_text(separator = " ",strip = True)
    for field, rules in config.items():
      if rules is None:
        value = None
      elif 'regex' in rules:
        match = re.search(rules['regex'],text)
        value = match.group(rules["group"]) if match is not None else None
      elif 'css_selector' in rules:
        value = element.select_one(rules['css_selector']).text.strip()
      elif 'selector' in rules:
        if(rules["method"] == 'text'):
          value = element.find(rules['selector']).text.strip()
        elif (rules["method"] == 'combined_text'):
          selected = element.find(rules["selector"])
          value = element.find(rules["selector"]).get_text().strip()
          if selected.next_sibling and isinstance(selected.next_sibling, str):
            value = f"{value} {selected.next_sibling.strip()}"
          else:
            value = None
      elif 'parent_selector' in rules:
        value = element.find(rules["parent_selector"]).find_parent("div")
      else:
        value = None
      data[field] = value

    return data

def save_html_to_file(html_content, file_name="output.html"):
    """
    Сохраняет HTML-текст в файл.

    :param html_content: Текст HTML
    :param file_name: Имя файла, куда будет сохранен HTML
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML успешно сохранен в файл: {file_name}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
