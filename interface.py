import streamlit as st
from typing import Dict, Any
from classes import Data, Clearable_Text_Input, Language
from utils import validate_api_key

def slider() -> Dict[str, Any]:
    api_key = st.sidebar.text_input("API Key", type="password", key="api_key")
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, value=0.5, key="temperature")
    top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, step=0.1, value=1.0, key="top_p")
    frequency_penalty = st.sidebar.slider("Frequency Penalty", min_value=0.0, max_value=1.0, step=0.1, value=0.0, key="frequency_penalty")
    presence_penalty = st.sidebar.slider("Presence Penalty", min_value=0.0, max_value=1.0, step=0.1, value=0.0, key="presence_penalty")
    language = st.sidebar.selectbox("Language", Language.get_languages(), key="language")
    is_validate = validate_api_key(api_key, "openai")
    if is_validate:
        st.sidebar.success("API Key 유효성 검사 성공")
    else:
        st.sidebar.error("API Key 유효성 검사 실패")
    st.sidebar.write(f"Fewshot_Maker는 GPT-4o를 사용합니다.")
    return {
        "api_key": api_key,
        "is_validate": is_validate,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "language": language
    }

interface_whole_height = 700

def display_examples() -> None:
    for example in st.session_state.examples:
        temp = st.container(border=True)
        with temp:
            col1, col2 = st.columns([0.8,0.2])
            with col1:
                temp_dict = {
                    "user_input": example["user_input"],
                    "assistant_output": example["assistant_output"]
                }
                st.write(temp_dict)
            with col2:
                if st.button("삭제", key=f"delete_{example['id']}"):
                    st.session_state.examples.remove(example)
                    st.rerun()

def get_sample_list_as_string() -> str:
    lst = []
    for i in st.session_state.examples:
        if i["user_input"] == "" and i["assistant_output"] != "":
            lst.append({
                "assistant_output": i["assistant_output"]
            })
        else:
            lst.append({
                "user_input": i["user_input"],
                "assistant_output": i["assistant_output"]
            })
    return f"```\n{"\n".join([str(i) for i in lst])}\n```"

def display_result_prompt(formatted_result: str, asset: st.empty) -> None:
    if formatted_result and asset:
        if len(st.session_state.examples) > 0:
            formatted_result = formatted_result.replace("{{sample}}", get_sample_list_as_string())
        else:
            formatted_result = formatted_result.replace("{{sample}}", "None")
        asset.markdown(formatted_result, unsafe_allow_html=True)

def display_result_generated_fewshot(generated : str, asset: st.empty) -> None:
    if generated:
        asset.text_area(label="", value=generated, height=int(interface_whole_height * 1.151), label_visibility='collapsed')

def display_result() -> None:
    container = st.container(height=int(interface_whole_height * 1.211))
    with container:
        result_display_asset = st.empty()
    return result_display_asset

def display_result_generation_tab() -> None:
    container = st.container(height=int(interface_whole_height * 1.211))
    with container:
        result_generation_display_asset = st.empty()
    return result_generation_display_asset

def generation_on_click() -> None:
    st.session_state.id_counter.reset()
    st.session_state.examples = []

def main_interface() -> Dict[str, Any]:
    st.header("few-shot 프롬프트 생성기")
    st.write("대상 프롬프트와 생성할 퓨샷의 요구조건 및 제약조건을 입력하면, 출력에 도움이 되는 예제를 생성합니다.")

    col1, col2, col3 = st.columns(3)
    with col1:
        prompt = st.text_area("대상 프롬프트", key="prompt", height=int(interface_whole_height * 0.5))
        count_generation = st.number_input("생성할 예제 개수", min_value=3, max_value=10, step=1, value=5, key="count_generation")
        requirements = st.text_area("정답 제약조건", key="requirements", height=int(interface_whole_height * 0.25))
        constraints = st.text_area("오답 제약조건", key="constraints", height=int(interface_whole_height * 0.25))
        count_notice = st.empty()
        cost_notice = st.empty()

    with col2:
        listup_container = st.container(height=int(interface_whole_height * 0.9))
        input_container = st.container(height=int(interface_whole_height * 0.37))
        with listup_container:
            display_examples()
        with input_container:
            user_input = Clearable_Text_Input("user_input")
            assistant_output = Clearable_Text_Input("assistant_output")
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                example_append = st.button("예제 추가")
            with col2:
                example_addition_notice = st.empty()
        fewshot_generation_button = st.button("few-shot 생성", on_click=lambda: generation_on_click())

    with col3:
        tab1, tab2 = st.tabs(["동작 프롬프트", "결과 확인"])
        with tab1:
            asset_combined_prompt = display_result()
        with tab2:
            asset_generation_result = display_result_generation_tab()
        asset = {
            "combined_prompt": asset_combined_prompt,
            "generation_result": asset_generation_result
        }

    return {
        "prompt": prompt,
        "requirements": requirements,
        "constraints": constraints,
        "count_generation": count_generation,
        "count_notice": count_notice,
        "cost_notice": cost_notice,
        "user_input": user_input.get_asset(),
        "assistant_output": assistant_output.get_asset(),
        "user_input_text_input_key": "user_input",
        "assistant_output_text_input_key": "assistant_output",
        "example_append": example_append,
        "example_addition_notice": example_addition_notice,
        "fewshot_generation_button": fewshot_generation_button,
        "asset_combined_prompt": asset["combined_prompt"],
        "asset_generation_fewshot": asset["generation_result"]
    }

def render() -> Data:
    st.sidebar.title("config")
    config = slider()
    main_page = main_interface()
    return Data({
        **config,
        **main_page
    })