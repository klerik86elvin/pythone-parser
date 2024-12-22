
import json
from typing import Dict, Any

class FilterManager:
  def __init__(self, site_filters: Dict[str, Any]):
    self.__site_filters: Dict[str, Any] = site_filters
    self.__params: Dict[str, Any] = {}
    with open("static_data/base_filters.json", encoding="utf-8") as file:
      self.base_filters = json.load(file)


  def set_filter(self, key, value):
    """
    Добавляет параметр в запрос с учетом необходимости массивов.
    :param key: Ключ параметра.
    :param value: Значение параметра.
    """
    if key not in self.__params:
      self.__params[key] = value

  def get_readable_filters(self):
    result = {}
    for key, id_value in self.__params.items():
      if key in self.base_filters and "data" in self.base_filters[key]:
        title = self.base_filters[key].get("title", None)
        value_name = next((item.get("name") for item in self.base_filters[key]["data"] if item["id"] == id_value), None)
        if title and value_name:
          result[title] = value_name
    return result
    
  def format_selected_filters(self):
    query = {"path_parts": [], "link_params": []}
    for key, value in self.__params.items():
      data = self.__site_filters[key]
      # Use a default value if no match is found
      _value = next((item['value'] for item in data['data'] if item['id'] == value), None)

      if _value is None:
          raise ValueError(f"Value '{value}' not found in {data['data']} for key '{key}'")

      if data['location'] == 'path':
          query['path_parts'].append(_value)
      elif data['location'] == 'query':
          _key = data['key']
          query['link_params'].append({"key": _key, "value": _value})

    return query


