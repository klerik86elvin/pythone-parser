from abc import ABC, abstractmethod
from core.parser_data_transformer import ParserDataTransformer
from typing import Dict, Any
from enums import AdType
import math
class TapDataTransformer(ParserDataTransformer):
    def __init__(self, parse_data, config) -> None:
        super().__init__(parse_data, config) 

    def adapt(self):
        parse_data = self.parse_data
        data = {}
        information = parse_data['information']
        building_type = [el['id'] for el in self.get_converted_data()['building_type']['data'] if parse_data['building_type'] == el['value']]
        data['building_type'] = building_type[0] if len(building_type) > 0 else 0
            for key, value in self._mapper_data.items():
            if "keys" in value:
                data[key] = [inf['value'] for inf in information if inf['key'] in value['keys']]
                if "Kirayə verilir" in data[key]:
                    _id = [v["id"] for v in value['values'] if v['value'] == data[key][1]]
                    data[key] = _id[0] if len(_id) > 0 else 0
            elif "key" in value:
                _key = value['key']
                arr = [v['value'] for v in information if v['key'] == _key]
                city = self.cities.loc[self.cities['name'] == arr[0], 'id']
                data[key] = city.iloc[0] if len(city) > 0 else 0
        print(data)
        # data['ad_type'] = 