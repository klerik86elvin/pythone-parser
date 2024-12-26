from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime
import json
import pandas as pd
class ParserDataTransformer(ABC):
  def __init__(self, parse_data: Dict[str, Any], config) -> None:
    self.parse_data = parse_data
    self._config = config
    self.__coverted_data = None
    self.query = {"id": int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])}
    self.ad_types = pd.read_csv('csv_tables/ad_types.csv')
    self.cities = pd.read_csv('csv_tables/cities.csv')
    self.building_type = pd.read_csv('csv_tables/building_types.csv')
    self.construction_type = pd.read_csv('csv_tables/construction_type.csv')
    with open(self._config['data_mapper_path'], "r", encoding="utf-8") as file:
        self._mapper_data = json.load(file)
    # print(self.cities )
  @abstractmethod
  def adapt() -> Dict[str, Any]:

    pass

  def get_converted_data(self):
    if self.__coverted_data is None:
      with open(self._config['filters_path'], "r", encoding="utf-8") as file:
        _config = json.load(file)
        self.__coverted_data = _config

    return self.__coverted_data