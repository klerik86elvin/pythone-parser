import sys
from bs4 import BeautifulSoup
from core.base_parser import BaseParser
from url_generators.tap_az_url_generator import TapAzURLGenerator
import json
import re

class TapAzParser(BaseParser):
  def __init__(self, config):
    super().__init__(config)


  def get_site_specific_filters(self):
    path = self.config.get('filters_path')
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

  def parse_detail_page(self, url):
    with open("output.html", "r") as file:
      html_doc = file.read()
    soup = BeautifulSoup(html_doc)
    data = {}
    data['building_type'] = url.split('/')[5]
    for field, rules in self.config['fields'].items():
      data[field] = self._parse_element(soup, field, rules)
    return data
  def _parse_element(self, element, field, rules):
    pattern = r"^attr:(.+)$"
    if 'css_selector' in rules:
      if rules['method'] == 'text':
        return element.select_one(rules['css_selector']).text.strip()
    elif "css_selector_arr" in rules:
      data = []
      match = re.match(pattern, rules['method'])
      arr = element.select(rules["css_selector_arr"])
      for el in arr:  
        _data = {}
        if match:
          attr = match.group(1)
          data.append(el[match.group(1)])
        if field == "information":
          _data = {"key": el.select_one(".product-properties__i-name").text.strip(), "value": el.select_one(".product-properties__i-value").text.strip()}
        else:
          _data = el.text.strip()
        data.append(_data)
      return data
    return {}
  def parse(self):
    return {}

