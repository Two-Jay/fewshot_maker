import streamlit as st
from classes import Data
import tiktoken
from typing import List, Dict, Any
from random import randint
from classes import IdCounter
from interface import render, display_result_prompt, display_result_generated_fewshot
import os

def session_state_init() -> None:
    if "examples" not in st.session_state:
        st.session_state.examples = []
    if "id_counter" not in st.session_state:
        st.session_state.id_counter = IdCounter()

def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def combine_prompt(data: Data) -> str:
    base_prompt = read_file(f"{os.path.dirname(__file__)}/prompt/generate_fewshots_base.md")
    prompt = base_prompt.replace("{{prompt}}", data.get("prompt"))
    requirements = data.get("requirements")
    constraints = data.get("constraints")
    count_generation = data.get("count_generation")
    prompt = prompt.replace("{{requirements}}", requirements) if requirements else prompt.replace("{{requirements}}", "None")
    prompt = prompt.replace("{{constraints}}", constraints) if constraints else prompt.replace("{{constraints}}", "None")
    prompt = prompt.replace("\n", "<br>")
    format_instructions = read_file(f"{os.path.dirname(__file__)}/prompt/format_instructions.md")
    prompt = prompt.replace("{{format_instructions}}", format_instructions)
    prompt = prompt.replace("{{language}}", data.get("language"))
    prompt = prompt.replace("{{count_generation}}", str(count_generation))
    return prompt

def generate_fewshot(data: Data) -> str:
    pass

input_cost_per_token_gpt4o_mini = 0.00000015
output_cost_per_token_gpt4o_mini = 0.0000006

def calculate_cost(prompt : str, data: Data) -> float:
    if prompt == "":
        return 0
    enc = tiktoken.encoding_for_model("gpt-4o-mini")
    input_token_count = len(enc.encode(prompt))
    max_example_length = max(
        (len(example["user_input"]) + len(example["assistant_output"]) 
         for example in st.session_state.examples),
        default=0
    )
    output_expacted_token_count = max_example_length * data.get("count_generation")
    input_cost = input_token_count * input_cost_per_token_gpt4o_mini
    output_cost = output_expacted_token_count * output_cost_per_token_gpt4o_mini
    return input_cost + output_cost, input_token_count + output_expacted_token_count

def postprocess(data: Data) -> Data:
    prompt = combine_prompt(data)
    token_cost, token_count = calculate_cost(prompt, data)
    data.set("result_prompt", prompt)
    data.set("token_cost", token_cost)
    data.set("token_count", token_count)
    response = generate_fewshot(data)
    data.set("result_generation_fewshot", response)
    return data

not_yet_generated_notice = "아직 생성되지 않았습니다."

def update_interface(data: Data) -> None:
    data.get("count_notice").text(f"생성시 필요 토큰 개수: {data.get('token_count')}")
    cost = data.get("token_cost")
    data.get("cost_notice").text(f"생성 비용: {cost:.5f} 달러")
    if data.get("example_append"):
        if data.get("assistant_output").get():
            st.session_state.examples.append({
                "id": st.session_state.id_counter.get(),
                "user_input": data.get("user_input").get() if data.get("user_input").get() else "",
                "assistant_output": data.get("assistant_output").get(),
            })
            data.get("user_input").clear()
            data.get("assistant_output").clear()
            data.get("example_addition_notice").success("예제 추가 성공")
            st.rerun()
        else:
            data.get("example_addition_notice").error("예제 추가 실패")

    display_result_prompt(data.get("result_prompt"), data.get("asset_combined_prompt"))
    if data.get("result_generation_fewshot"):
        display_result_generated_fewshot(data.get("result_generation_fewshot"), data.get("asset_generation_fewshot"))
    else:
        display_result_generated_fewshot(not_yet_generated_notice, data.get("asset_generation_fewshot"))

def run_impl() -> None:
    st.set_page_config(layout="wide")
    session_state_init()
    data = render()
    postprocessed = postprocess(data)
    update_interface(postprocessed)

class MainController:
    @staticmethod
    def run() -> None:
        run_impl()
