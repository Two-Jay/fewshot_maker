
from openai import OpenAI

def validate_api_key(api_key: str, vendor: str) -> bool:
    match vendor:
        case "openai":
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Hello, world!"}
                    ]
                )
                return True
            except Exception as e:
                return False
        case _:
            return False