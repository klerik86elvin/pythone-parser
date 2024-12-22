from abc import ABC, abstractmethod
from core.parser_data_transformer import ParserDataTransformer
from typing import Dict, Any
class YeniemlakDataTransformer(ParserDataTransformer):
  def __init__(self, parse_data, config) -> None:
    super().__init__(parse_data, config)

  def adapt(self):
    print(self.parse_data)
    self.query['building_type'] = self.parse_data['building_type'].split('/')[0].strip()
    self.query['construction_type'] = self.parse_data['building_type'].split('/')[1].strip()
    self.query['floor'] = int(self.parse_data["floor"].split("/")[1].strip()) if self.parse_data["floor"] is not None else None
    self.query['total_floor'] = int(self.parse_data["floor"].split("/")[0].strip()) if self.parse_data["floor"] is not None else None
    self.query['rooms'] = int(self.parse_data['rooms']) if self.parse_data["rooms"] is not None else None
    self.query['area_m'] = int(self.parse_data['area_m']) if self.parse_data["area_m"] is not None else None
    self.query["area_s"] = int(self.parse_data['area_s']) if self.parse_data["area_s"] is not None else None
    self.query['kupcha'] = True if self.parse_data['kupcha'] == 'Kupça' else False
    self.query['price'] = float(self.parse_data['price'])
    print({**self.parse_data,**self.query })
    # return self._result

  