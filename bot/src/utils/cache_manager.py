import json
import os
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

class CacheManager:
    @staticmethod
    def get_cache_path(cache_name: str) -> str:
        return os.path.join(CACHE_DIR, f"{cache_name}.json")

    @staticmethod
    def read_cache(cache_name: str) -> Optional[Dict]:
        cache_path = CacheManager.get_cache_path(cache_name)
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                # Check if cache is not expired (24 hours)
                if datetime.fromisoformat(cache_data['timestamp']) + timedelta(hours=24) < datetime.now():
                    return None
                return cache_data['data']
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    @staticmethod
    def write_cache(cache_name: str, data: Any) -> None:
        cache_path = CacheManager.get_cache_path(cache_name)
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
