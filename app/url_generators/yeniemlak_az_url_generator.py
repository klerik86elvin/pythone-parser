from core.base_url_generator import BaseURLGenerator

class YeniemlakAzURLGenerator(BaseURLGenerator):

  def __init__(self, base_url, selected_filters):
    super().__init__(base_url, selected_filters)

  def build_url(self):
    return f"{self.base_url}/elan/axtar"
