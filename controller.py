import streamlit as st
from classes import Data

def interface() -> Data:
    st.sidebar.title("fewshot-maker")
    api_key = st.sidebar.text_input("API Key", type="password", key="api_key")
    return Data({
        "api_key": api_key
    })

def postprocess(data: Data) -> Data:
    return data

def update_interface(data: Data) -> None:
    st.write(data.get("api_key"))

def run_impl() -> None:
    data = interface()
    postprocessed = postprocess(data)
    update_interface(postprocessed)

class MainController:
    @staticmethod
    def run() -> None:
        run_impl()
