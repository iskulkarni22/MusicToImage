import json
import requests
import io
from PIL import Image
API_URL = "https://yma9wwo3hu51qlno.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Authorization": f"Bearer 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",
        "Content-Type": "application/json",}

API_URL2 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers2 = {"Authorization": "Bearer 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"}

#lyrics = '''
#'''

#variables
res = None
data = None
image_bytes = None


# "inputs" must have less than 1024 tokens
def queryLlama2(payload):
    print("query llama2 call")
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

#data = queryLlama2(lyrics)

#res = data[0]['generated_text']
# print(res)


def querySDXL(payload):
    print("query SDXL call")
    response = requests.post(API_URL2, headers=headers2, json=payload)
    return response.content
#image_bytes = querySDXL({
#	"inputs": res,
#})

# print(image_bytes)
def divide_string(string, parts):
       # Determine the length of each substring
   part_length = len(string) // parts

   # Divide the string into 'parts' number of substrings
   substrings = [string[i:i + part_length] for i in range(0, len(string), part_length)]

   # If there are any leftover characters, add them to the last substring
   if len(substrings) > parts:
      substrings[-2] += substrings[-1]
      substrings.pop()

   return substrings

def convert_to_prompt(input_set, header_str):
    for i in range(1, len(input_set)):
        input_set[i] = header_str + input_set[i]
    return input_set
        

def generate(payload, style, iterations):
    #llama input
    input_set = []
    #print("calling generate...")
    data = queryLlama2(payload)
    #print(data)
    res = data[0]['generated_text']
    #res is image description
    
    #input_set.append(res)
    
    #custom slicing 
    header_str = "Generate an image in a(n) " + style + " style using the following lyrics: \n"
    token_count = ((len(payload)//4)+1) + iterations*len(header_str)
    input_set = divide_string(payload, iterations)
    input_set.insert(0,res)
    input_set = convert_to_prompt(input_set, header_str)
    #print(input_set[1])
    
    for i in range(len(input_set)):
        image_bytes = querySDXL({"inputs": input_set[i]})
        print(image_bytes)
        if i == 0:
            #this is the llama image
            #print(input_set[0])
            #image_bytes = querySDXL({"inputs": input_set[i]})
            image = Image.open(io.BytesIO(image_bytes))
            image.save("llama2_out.png", "")
        else:
            image_bytes = querySDXL({"inputs": input_set[i]})
            #image = Image.open(io.BytesIO(image_bytes))
            title = "image_" + i + ".png"
            image.save(title, "")
            
            
    #image_bytes = querySDXL({
    #    "inputs": res
    #})
    
    #image = Image.open(io.BytesIO(image_bytes))
    #image.show()
    

def main():
    print("main call")
    input = """Tell me, is you still up? (Up)
It's 5 AM and I'm drunk right now
Tell me, can we still fuck? (Fuck that shit)
One of one, I'm in the zone right now
Tell me, am I still? Mm
Tellin' you just how I feel right now
You say it's just the drugs, and I know
I know, I know, I know, I know, I know, I know
I lied too, way before, before
Before I had you right inside my arms
Then again, I could be drunk (it's lit, yeah)
Baby, I don't wanna sound righteous (yeah)
I got twenty bitches suckin' like bisons
I just eeny, meeny, miney, roll the dices, I pick her (pop it, pop it)
She ain't really even my type, been out here
She been losin' herself to the night shift
She been losin' herself, and I get it, oh, girl, yeah, I get it
Yeah, yeah, you've been fightin' for your shot
And you've been searchin' for your spot
Girl, I feel it, yeah, girl, I feel it, yeah
Oh, you think you got your groove
But you want someone like you
Tell me, is you still up? (Up)
It's 5 AM and I'm drunk right now
Tell me, can we still fuck? (Fuck that shit)
One of one, I'm in the zone right now
Tell me, am I still? Mm
Tellin' you just how I feel right now
You say it's just the drugs, and I know
I know, I know, I know, I know, I know, I know (ooh, it's the kid, know it, damn it)
I lied too, way before, before (how they feelin', how they feelin', ooh)
Before I had you right inside my arms (feelin' like some money, tonight)
Then again, I could be drunk (yeah)
I know, mami, I know (know), it's 2 AM, don't stress
At three, that blue shit kick in', in thirty you'll feel your best
I turned my whole spot to Crucial, it's crucial, the way I left (it's lit)
Upstairs is like a low, my new bitches be the best (let's go)
I'm lookin' at her, when her startin' to turn to you (her)
Now you startin' to fuck up my mind, is it you, is it her?
We brought booby trap to the 'burbs
F29 is my address, in case you ain't heard
It's floodin' upstairs, it's a leak
I don't make it squeak, make it squirt
I make this shit beat, bon appétit when I feast
Slippin' and slide through the streets, it takes a finesse
Especially in this Cabriolet Jeep, engine make chaotic creep
Just leave the gate open, through the side door, I'ma creep (ooh, ooh)
Are you 'bout it? Too real, and are the kids downstairs asleep?
And are you upstairs by yourself? A minute from there
Is there some room for me? Baby, do tell, do tell
Tell me, is you still up? (Up)
It's 5 AM and I'm drunk right now
Tell me, can we still fuck? (Fuck that shit)
One of one, I'm in the zone right now
Tell me, am I still? Mm
Tellin' you just how I feel right now
You say it's just the drugs, and I know
I know, I know, I know, I know, I know, I know
I lied too, way before, before
Before I had you right inside my arms
Then again, I can be drunk
"""
    #print("Token size: ", len(input)/4)
    #print(lyrics)
    generate(input, "anime", 3)
    quit()
    
if __name__ == "__main__":
    main()



