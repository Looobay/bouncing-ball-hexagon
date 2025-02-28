# In your terminal, first run:
# pip install openai

import os
from openai import OpenAI

XAI_API_KEY = 'xai-fmDjkyMFoaD0YMiwr3OmWlAnPEXRH2y0VIPWP8E21oFZw8x1YBEPHIqiRR2EqyijlAT2Qh9YYu5AVT1G'
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
    model="grok-beta",
    messages=[
        {
            "role": "user",
            "content": "write a Python program that shows a ball bouncing inside a spinning hexagon. The ball should be affected by gravity and friction, and it must bounce off the rotating walls realistically"
        },
    ],
)

print(completion.choices[0].message.content)