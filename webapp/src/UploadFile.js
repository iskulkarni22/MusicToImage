import { useState, useRef } from "react";
import { FIREBASE_STORAGE } from "./firebase";
import { ref, uploadBytes } from "firebase/storage";

const UploadFile = (props) => {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = function (e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const storageRef = ref(FIREBASE_STORAGE, file.name);
      console.log(storageRef);
      uploadBytes(storageRef, file).then((snapshot) => {
        props.changeFile(file.name);
        const url = `https://us-central1-vipmusictoimage.cloudfunctions.net/transcribe?filename=${file.name}`;
        fetch(url, {
          method: "GET",
        })
          .then((response) => response.text())
          .then((data) => {
            props.changeLyrics(data);
            props.setInputLyrics(data);
          });
      });
    }
  };

  const handleChange = function (e) {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const storageRef = ref(FIREBASE_STORAGE);
      uploadBytes(storageRef, file).then((snapshot) => {
        const url = `https://us-central1-vipmusictoimage.cloudfunctions.net/transcribe?filename=${file.name}`;
        fetch(url, {
          method: "GET",
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
          });
      });
    }
  };

  const inputRef = useRef(null);

  const onButtonClick = () => {
    inputRef.current.click();
  };

  return (
    <form
      id="form-file-upload"
      onDragEnter={handleDrag}
      onSubmit={(e) => e.preventDefault()}
      style={{ margin: "auto" }}
    >
      <p>Upload a sound file:</p>
      <input
        ref={inputRef}
        type="file"
        id="input-file-upload"
        multiple={true}
        onChange={handleChange}
      />
      <label
        id="label-file-upload"
        htmlFor="input-file-upload"
        className={dragActive ? "drag-active" : ""}
      >
        <div>
          <p>Drag and drop</p>
          <p>or</p>
          <button className="upload-button" onClick={onButtonClick}>
            Click to Upload
          </button>
        </div>
      </label>
      {dragActive && (
        <div
          id="drag-file-element"
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        ></div>
      )}
    </form>
  );
};

export default UploadFile;
