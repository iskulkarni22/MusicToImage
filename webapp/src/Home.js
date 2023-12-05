import { useState } from "react";
import UploadFile from "./UploadFile";
import GenerateImage from "./GenerateImage";

const Home = () => {
  const [lyrics, setLyrics] = useState("");
  const [filename, setFilename] = useState("");
  const [inputLyrics, setInputLyrics] = useState("");
  return (
    <div style={outer}>
      <h1>Music To Image</h1>
      <div style={inner}>
        <div>
          <UploadFile
            changeLyrics={setLyrics}
            setInputLyrics={setInputLyrics}
            changeFile={setFilename}
          />
          <h3>{"."}</h3>
          <h3>{filename === "" ? "" : `Filename: ${filename}`}</h3>
          <h3>{lyrics === "" ? "" : `Lyrics:`}</h3>
          <p>{lyrics}</p>
        </div>
        <GenerateImage
          inputLyrics={inputLyrics}
          setInputLyrics={setInputLyrics}
        />
      </div>
    </div>
  );
};

const outer = {
  textAlign: "center",
  margin: "auto",
};

const inner = {
  display: "flex",
  justifyContent: "space-around",
  padding: "50px",
};

export default Home;
