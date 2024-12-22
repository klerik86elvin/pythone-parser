from abc import ABC, abstractmethod
from urllib.parse import urlencode

class BaseURLGenerator(ABC):
    def __init__(self, base_url, selected_filters):
        """
        Базовый класс для генерации URL с фильтрами.
        :param base_url: Основной URL сайта.
        :param site_filters: JSON фильтров конкретного сайта.
        """
        self.base_url = base_url
        self.selected_filters = selected_filters
        self.site_filters = selected_filters

    def generate_url(self):
      """
      Генерирует URL на основе установленных фильтров.
      :return: Сгенерированный URL.
      """

      path_parts = self.selected_filters['path_parts']
      link_params = self.selected_filters['link_params']
      params = {item['key']: item['value'] for item in link_params}
      query_string = urlencode(params)
      full_path =  f"{self.build_url()}/{'/'.join(path_parts)}"
      return f"{full_path}?{query_string}" if len(link_params) > 0 else full_path
      
    def build_url(self):
      return self.base_url
