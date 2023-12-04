import json
import requests

API_URL = "https://yma9wwo3hu51qlno.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Authorization": f"Bearer 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",
        "Content-Type": "application/json",}

lyrics = '''
Never been in love
But you're dragging my soul away
Feels like woo woo woo woo

Ever since the day
You walked into my life I knew
Complete surrender

Where we go
Where we go
Where you go I follow baby
Where we go
Far away from earth
Where no one can find us

Butterfly
Take me away
Get carried away yeah
Take it off baby

Butterfly
Let's get away
Get carried away yeah
Take it off baby

Butterfly
Take me away
Get carried away yeah
Take it off baby

Butterfly
Let's get away
Get carried away yeah
Losing myself

Where we go
Where we go
Where you go I follow baby
Where we go
Far away from earth
Where no one can find us
'''

def queryLlama2(payload):
    json_body = {
        "inputs": f"[INST] <<SYS>> Generate an image description using these lyrics as inspiration <<SYS>> {payload} [/INST] ",
                "parameters": {"max_new_tokens":256, "top_p":0.9, "temperature":0.7}
        }
    data = json.dumps(json_body)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    try:
        return json.loads(response.content.decode("utf-8"))
    except:
        return response

data = queryLlama2(lyrics)
res = data[0]['generated_text']
# print(res)



API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def querySDXL(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = querySDXL({
	"inputs": res,
})
import io
from PIL import Image

# print(image_bytes)
image = Image.open(io.BytesIO(image_bytes))
image.show()
