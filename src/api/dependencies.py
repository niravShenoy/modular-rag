from fastapi import Depends
from src.core.config import Config

def get_config() -> Config:
    return Config()