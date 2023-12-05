import React, { useEffect, useState } from "react";

const GenerateImage = ({ inputLyrics, setInputLyrics }) => {
  const [generatedPrompt, setGeneratedPrompt] = useState("");
  const [imageBlob, setImageBlob] = useState(null);

  const API_URL_LLAMA2 =
    "https://yma9wwo3hu51qlno.us-east-1.aws.endpoints.huggingface.cloud";
  const HEADERS_LLAMA2 = {
    Authorization: "Bearer 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",
    "Content-Type": "application/json",
  };

  const API_URL_SDXL =
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1";
  const HEADERS_SDXL = {
    Authorization: "Bearer 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",
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    queryLlama2(inputLyrics);
    console.log(inputLyrics);
  };

  useEffect(() => {
    if (generatedPrompt !== "") {
      querySDXL(generatedPrompt);
    }
  }, [generatedPrompt]);

  const queryLlama2 = (lyrics) => {
    const body = {
      inputs: `[INST] <<SYS>> Generate an image description using these lyrics as inspiration <<SYS>> ${lyrics} [/INST] `,
      parameters: { max_new_tokens: 256, top_p: 0.9, temperature: 0.7 },
    };
    fetch(API_URL_LLAMA2, {
      method: "POST",
      headers: HEADERS_LLAMA2,
      body: JSON.stringify(body),
    })
      .then((response) => response.json())
      .then((data) => {
        setGeneratedPrompt(data[0].generated_text);
        console.log(data);
      });
  };

  const querySDXL = (lyrics) => {
    fetch(API_URL_SDXL, {
      method: "POST",
      headers: HEADERS_SDXL,
      body: JSON.stringify({ inputs: lyrics, wait_for_model: true }),
    })
      .then((data) => data.blob())
      .then((blob) => {
        setImageBlob(blob);
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <p>Input lyrics (2500 characters or less):</p>
        <textarea
          value={inputLyrics}
          onChange={(e) => setInputLyrics(e.target.value)}
          rows="10"
          cols="30"
          maxlength="2500"
        ></textarea>
      </form>
      <button onClick={(e) => handleSubmit(e)}>Generate</button>
      <h3>{generatedPrompt === "" ? "" : `Generated Prompt:`}</h3>
      <p style={text}>{generatedPrompt}</p>
      {imageBlob === null ? (
        ""
      ) : (
        <img
          src={URL.createObjectURL(imageBlob)}
          alt="Generated Image"
          width="50%"
          height="50%"
        />
      )}
    </div>
  );
};

const text = {
  width: "50%",
  margin: "auto",
  padding: "20px",
};

export default GenerateImage;
