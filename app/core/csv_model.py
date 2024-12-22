from abc import ABC
import pandas as pd

class CSVModel(ABC):
  __base_path = ''
  _csv_table = None
  
  @classmethod
  def all(cls):
    return pd.read_csv(f"{cls.__base_path}{cls._csv_table}.csv")


