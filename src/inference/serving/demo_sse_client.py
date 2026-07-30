import requests

response = requests.post(
    "http://127.0.0.1:8000/stream",
    json={
        "prompt": "Explain KV Cache.",
        "max_new_tokens": 32,
    },
    stream=True,
)

for line in response.iter_lines():

    if line:

        print(line.decode())