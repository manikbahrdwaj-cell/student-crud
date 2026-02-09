import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key=("csk-tp42hnmnm483dfhncc3wvem49h8npn8yw42kncy62f38p3mw")
)

completion = client.chat.completions.create(
    messages=[{"role":"user","content":"Why is fast inference important?"}],
    model="gpt-oss-120b",
    max_completion_tokens=1024,
    temperature=0.0,
    top_p=1,
    stream=False
)

print(completion.choices[0].message.content)
