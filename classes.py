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

class IdCounter:
    def __init__(self):
        self.class_id = 0

    def get(self):
        self.class_id += 1
        return self.class_id

    def reset(self):
        self.id = 0

    def get_id(self):
        return self.id
    
    def set_id(self, id: int):
        self.id = id

import streamlit as st

class Clearable_Text_Input:
    def __init__(self, key: str):
        self.key = key
        self.empty = st.empty()
        self.text_input = self.empty.text_input(label=self.key)

    def clear(self):
        self.text_input = ""

    def get(self):
        return self.text_input
    
    def get_asset(self):
        return self

from enum import Enum

class Language(Enum):
    한국어 = "Korean"
    English = "English"
    Arabic = "Arabic"

    def get_languages():
        return [language.value for language in Language]

 