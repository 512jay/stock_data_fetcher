# In base.py
from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def get_historical_data(self):
        pass

    @abstractmethod
    def get_realtime_data(self):
        pass
