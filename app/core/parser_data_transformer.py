from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime
import json

class ParserDataTransformer(ABC):
  def __init__(self, parse_data: Dict[str, Any], config) -> None:
    self.parse_data = parse_data
    self._config = config
    self.__coverted_data = None
    self.query = {"id": int(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])}

  @abstractmethod
  def adapt() -> Dict[str, Any]:

    pass

  def get_converted_data(self):
    if self.__coverted_data is None:
      with open(self._config['filters_path'], "r", encoding="utf-8") as file:
        _config = json.load(file)
        self.__coverted_data = _config

    return self.__coverted_data