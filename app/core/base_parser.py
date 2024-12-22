from abc import ABC, abstractmethod
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from helpers.parser_helper import fetch_html
from core.base_url_generator import BaseURLGenerator
import json
import os
import inspect
import re

class BaseParser(ABC):
    """
    Базовый класс для всех парсеров. Определяет основные методы для фильтрации, генерации URL и обработки HTML.
    """
    
    def __init__(self, config):
      self.config = config
   
    @abstractmethod
    def get_site_specific_filters(self):
        """Метод для получения специфичных ключей фильтров для сайта."""
        pass
    @abstractmethod
    def parse(self, method="cloudscraper"):
      """
        Основной метод для выполнения парсинга (заглушка).
        Должен быть переопределен в наследниках.
        :param url: Ссылка на страницу.
        :return: Результаты парсинга.
      """
      pass
        
    def get_base_url(self):
        return self.config.get("url")
    
    
    def _parse_element(self, element, field, rules):
      try:
        text = element.get_text(separator = " ",strip = True)
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
        return value
      except:
        print(f"Ошибка парсинга поля {field}: {e}")
        return None

    def fetch_html(self, url, method = "cloudscraper"):
      html = fetch_html(url, method)
      if not html:
          raise ValueError("HTML content is empty or could not be fetched.")
      self._soup = BeautifulSoup(html, 'html.parser')
      return html
    
   
        


