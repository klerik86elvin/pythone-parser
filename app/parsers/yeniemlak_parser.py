from bs4 import BeautifulSoup
from core.base_parser import BaseParser
from url_generators.yeniemlak_az_url_generator import YeniemlakAzURLGenerator
import json
import time

class YeniemlakParser(BaseParser):
  def __init__(self, config):
    super().__init__(config)
    
  def get_site_specific_filters(self):
    path = self.config.get('filters_path')
    with open(path, "r") as file:
        data = json.load(file)
    return data

  def fetch_links(self, url):
    """
    Сбор ссылок на страницы подробного описания.
    """
    html = self.fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    if not soup:
        return []
    try:
      elements = soup.select(self.config.get("list_selector", ""))
      links = []

      for element in elements:
        link_tag = element.select_one(self.config.get("detail_link_selector", ""))
        if link_tag and link_tag.get("href"):
            links.append(f"{self.config.get('url')}{link_tag['href']}")
      return links
    except:
        print(soup)


  def parse_detail_page(self, url):
    """
    Парсинг страницы подробного описания.
    """
    try:
      
      soup =  BeautifulSoup(self.fetch_html(url)).select_one(self.config.get("detail_data_selector"), "")
      data = {}
      data['ad_link'] = url
      for field, rules in self.config["fields"].items():
        data[field] = self._parse_element(soup, field, rules)
      locations = self.__get_location_data(soup)
      data = {**data, **locations}
      data['phones'] = self.__get_phones(soup)
      data['property_features'] = self.__get_property_features(soup)
      data['images'] = self.__get_images(soup)
      self.__get_phones(soup)
      return data
    except:
      print(self.fetch_html(url))
    

    

  def parse(self, url):
    """
    Главный метод парсинга: 
    - Сначала собирает ссылки
    - Потом парсит страницы подробного описания
    """
    links = self.fetch_links(url)
    results = []
    for link in links:
      detail_data =  self.parse_detail_page(link)
      if detail_data:
        results.append(detail_data)
      time.sleep(5)
    return results

  def __get_location_data(self, soup):
    locations_soup = soup.find("h1", string="Ünvan").find_next_siblings('div', {"class": "params"})

    location_keys = ["city", "district", "district_settlement", "metro"]
    locations = [el.get_text(strip=True) for el in locations_soup]

    result = {}
    unused_keys = iter(location_keys)  # Создаём итератор по ключам

    for loc in locations:
        if "metro" in loc:
            result["metro"] = loc.replace("metro.", "").strip()
        else:
            result[next(unused_keys)] = loc  # Берём следующий доступный ключ

    return result

  def __get_phones(self, soup):
    phone_soup = soup.find('div', {"class": "tel"}).find_all("img")
    phones_src = [phone['src'].strip() for phone in phone_soup]
    phones = [phone.split('/')[-1] for phone in phones_src]
    return phones

  def __get_property_features(self, soup):
    features = soup.find_all('div', {"class": "check"});
    features = [f.get_text().strip() for f in features]
    return features

  def __get_images(self, soup):
    images = soup.find_all("div", {"class": "img_div"})
    images = [f"{self.config.get('url')}{i.find('img')['src']}" for i in images]
    return images