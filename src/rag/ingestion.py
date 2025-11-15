from typing import List
from src.core.config import Config

class IngestionService:
    def __init__(self, config: Config):
        self.config = config

    def ingest_data(self, files: List):
        pass