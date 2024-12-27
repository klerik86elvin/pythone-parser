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
        data['apartment_feautures'] = {}
        information = parse_data['information']
        building_type = [el['id'] for el in self.get_converted_data()['building_type']['data'] if parse_data['building_type'] == el['value']]
        data['title'] = parse_data['title']
        data['price'] = float(parse_data['price'].replace(" ", ""))
        data['description'] = parse_data['description']
        data['building_type_id'] = building_type[0] if len(building_type) > 0 else 0
        data['ad_type_id'] = self.__get_ad_type_id()
        data['construction_type_id'] = self.__get_construction_type_id()
        data['city_id'] = self.__get_city_id()
        data['apartment_feautures']['area_m'] = self.__get_area_m()
        data['apartment_feautures']['rooms'] = self.__get_rooms()
        data['address'] = self.__get_address()
        data ['images'] =  self.__get_images()
        print(data)
        return data
    def __get_ad_type_id(self):
        try:
            _parse_data = self.parse_data
            _mapper_data = self._mapper_data
            arr = [inf for inf in _parse_data['information'] if inf['key'] in _mapper_data['ad_type']['keys']]
            is_rent = len([i for i in arr if i['value'] == 'Kirayə verilir']) > 0
            ad_type = arr[1]['value'] if is_rent else arr[0]['value']
            _id = [i['id'] for i in _mapper_data['ad_type']['values'] if i['value'] == ad_type]
            _id = _id[0] if _id else 0
            return _id
        except:
            return None

    def __get_construction_type_id(self):
        construction_type = [i['value'] for i in self.parse_data['information'] if i['key'] == self._mapper_data['construction_type']['key']]
        if construction_type:
            construction_type = construction_type[0]
            _id = [i['id'] for i in self._mapper_data['construction_type']['values'] if i['value'] == construction_type]
            return _id[0]
        else:
            return None

    def __get_city_id(self):
        city  = [i['value'] for i in self.parse_data['information'] if i['key'] == self._mapper_data['city']['key']][0]
        city_id = [i['id'] for i in self._mapper_data['city']['values'] if i['value'] == city][0]
        return city_id

    def __get_area_m(self):
        try:
            _data = [i['value'] for i in self.parse_data['information'] if i['key'].startswith('Sahə, m')][0]
            return int(_data)
        except:
            return None

    def __get_rooms(self):
        _data = [i['value'] for i in self.parse_data['information'] if i['key'].startswith('Otaq sayı')]
        return int(_data[0]) if _data else None

    def __get_address(self):
        _data = [i['value'] for i in self.parse_data['information'] if i['key'].startswith('Yerləş')][0]
        return _data

    def __get_images(self):
        _data = [i for i in self.parse_data['images'] if i]
        return _data