from typing import List, Dict, Any

class Data:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def get(self, key: str) -> Any:
        return self.data[key]

    def set(self, key: str, value: Any, overwrite: bool = False):
        if key in self.data and not overwrite:
            raise ValueError(f"Key {key} already exists")
        self.data[key] = value

    def reset_booleans_to_false(self, keys: List[str]):
        for key in keys:
            if isinstance(self.data[key], bool):
                self.data[key] = False