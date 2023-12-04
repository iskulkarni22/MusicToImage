from flask import Flask, render_template, request
import json
import requests
import io
from PIL import Image
import base64

app = Flask(__name__)

API_URL_LLAMA2 = "https://yma9wwo3hu51qlno.us-east-1.aws.endpoints.huggingface.cloud"
HEADERS_LLAMA2 = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
}

API_URL_SDXL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS_SDXL = {"Authorization": "Bearer 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"}

def query_llama2(payload):
    json_body = {
        "inputs": f"[INST] <<SYS>> Generate an image description using these lyrics as inspiration <<SYS>> {payload} [/INST] ",
        "parameters": {"max_new_tokens": 256, "top_p": 0.9, "temperature": 0.7},
    }
    data = json.dumps(json_body)
    response = requests.request("POST", API_URL_LLAMA2, headers=HEADERS_LLAMA2, data=data)
    try:
        return json.loads(response.content.decode("utf-8"))
    except:
        return response

def query_sdxl(payload):
    response = requests.post(API_URL_SDXL, headers=HEADERS_SDXL, json=payload)
    return response.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        lyrics = request.form["lyrics"]
        llama2_data = query_llama2(lyrics)
        print(llama2_data)
        generated_text = llama2_data[0]["generated_text"]
        image_bytes = query_sdxl({
            "inputs": generated_text,
            "wait_for_model": True
        })
        print(image_bytes)
        image = Image.open(io.BytesIO(image_bytes))

        # Convert the image to base64 for displaying in HTML
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return render_template("index.html", lyrics=lyrics, generated_text=generated_text, image_data=image_data)
    else:
        return render_template("index.html", lyrics="", generated_text="", image_data="")

if __name__ == "__main__":
    app.run(debug=True)
