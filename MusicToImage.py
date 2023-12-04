import json
import requests

API_URL = "https://yma9wwo3hu51qlno.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Authorization": "Bearer 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",
        "Content-Type": "application/json",}

lyrics = '''
Look in my eyes, tell me a tale
Do you see the road, the map to my soul?
Look, tell me the signs whenever the smoke clear out of my face
Am I picture-perfect, or do I look fried?
All of that green and yellow, that drip from your eyes is tellin'
Tell you demise, I went to my side
To push back the ceilin' and push back the feelings, I had to decide
I replay them nights, and right by my side, all I see is a sea of people that ride wit' me
If they just knew what Scotty would do to jump off the stage and save him a child
The things I created became the most weighted, I gotta find balance and keep me inspired (hah)
Yeah, yeah
That shit wild, instead I'm a hero
I took it from zero, LaFlame Usain
I run it from miles, this shit wasn't luck
They got me fucked up, I put you on bus and take you around
A couple of guys inside of the school, I gave 'em the tools to get it off ground
They say they the ones when they make the errors
Can't look in the mirror, that shit wild
Stand on the stage, I give 'em the rage
No turnin' it down, can't tame it, can't follow it
We do it for streets, we do it for keeps, we do it for rights, got 52 weeks
This shit ain't for pleasure, I'm comin' to tweak
This shit is forever and infinity
Number eight, yeah, we write it and wrap it around
I take me beat and I turn to a beast
Bought the crib on a hill, made it harder to reach
Bought a couple more whips 'cause I needed more speed
Bought a couple more watches, I needed more time
Didn't buy the condo, it was smarter to lease
And I bought some more ice 'cause I brought in the heat
Made a cast of my dick, so she never gon' cheat
If I gave you a day in my life or a day in my eyes, don't blink
'''

# "inputs" must have less than 1024 tokens
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



API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}

def querySDXL(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = querySDXL({
	"inputs": res,
    "wait_for_model": True
})
import io
from PIL import Image

print(image_bytes)
image = Image.open(io.BytesIO(image_bytes))
image.show()
