import sys
from core.base_parser import BaseParser
from url_generators.tap_az_url_generator import TapAzURLGenerator
import json

class TapAzParser(BaseParser):
  def __init__(self, config):
    super().__init__(config)


  def get_site_specific_filters(self):
    path = self.config.get('filters_path')
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

  def parse(self):
    return {}

