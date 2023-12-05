import json
import requests
import io
from PIL import Image
API_URL = "https://yma9wwo3hu51qlno.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Authorization": f"Bearer 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",
        "Content-Type": "application/json",}

API_URL2 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers2 = {"Authorization": "Bearer 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"}

#lyrics = '''
#'''

#variables
res = None
data = None
image_bytes = None


# "inputs" must have less than 1024 tokens
def queryLlama2(payload):
    #print("query llama2 call")
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
    #print("query SDXL call")
    response = requests.post(API_URL2, headers=headers2, json=payload)
    return response.content
#image_bytes = querySDXL({
#	"inputs": res,
#})


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

def payload_checker(payload,iterations,header_str,llama):
    token_count = (((len(payload)//4)+1) + iterations*len(header_str))/4
    #print(token_count)
    if token_count > 1024 or (llama and len(payload)>1024):
        return payload[0:2800]
    else:
        return payload
        

def generate(payload, style, iterations):
    #handle if payload is too large
    header_str = None
    if style:
        header_str = "Generate an image in a(n) " + style + " style using the following lyrics: \n"
    else:
        header_str = "Generate an image using the following lyrics: \n"
    payload = payload_checker(payload, iterations, header_str,False)
    
    #generate llama input
    input_set = []
    data = queryLlama2(payload_checker(payload,iterations,header_str,True))
    print(data)
    res = data[0]['generated_text']

    #print(payload)
    #custom slicing     
    input_set = divide_string(payload, iterations)
    input_set.insert(0,res)
    input_set = convert_to_prompt(input_set, header_str)
    #print(input_set[1])
    
    output = []
    for i in range(len(input_set)):
        image_bytes = querySDXL({"inputs": input_set[i]})
        print(image_bytes)
        #print(input_set[i])
        if i == 0:
            #this is the llama image
            #print(input_set[0])
            #image_bytes = querySDXL({"inputs": input_set[i]})
            image = Image.open(io.BytesIO(image_bytes))
            image.save("llama2_out.png", "")
            output.append(("llama2_out.png", input_set[i]))
        else:
            #image_bytes = querySDXL({"inputs": input_set[i]})
            image = Image.open(io.BytesIO(image_bytes))
            title = "image_" + str(i) + ".png"
            image.save(title, "")
            output.append((title, input_set[i]))
    return output
            

#def main():
#    print("main call")
#    input = """"""
#    #print("Token size: ", len(input)/4)
#    #print(lyrics)
#    #print(len(input))
#    out = generate(input, None, 4)
#    print(out)
#    quit()
    
#if __name__ == "__main__":
#    main()



