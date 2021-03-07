import axios from "axios";
import { useState } from "react";
import ImageUploader from "react-images-upload";

import "./App.css";
import bg from "./assets/bg-img.jpg";

function App() {
  const [server, setServer] = useState("");
  const [client, setClient] = useState("");
  const [images, setImages] = useState([]);

  const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => {
        resolve(fileReader.result);
      };
      fileReader.onerror = (error) => {
        reject(error);
      };
    });
  };

  const histogram = async (event) => {
    event.preventDefault();
    const imageArray = [];
    for (let img of images) {
      const image64 = await convertBase64(img);
      imageArray.push(image64.split(",")[1]);
    }
    console.log({ client, images: imageArray });
    axios.post(server + `ImageServer/Histogram`, {
      client,
      images: imageArray,
    });
  };

  const color = async (event) => {
    event.preventDefault();
    const imageArray = [];
    for (let img of images) {
      const image64 = await convertBase64(img);
      imageArray.push(image64.split(",")[1]);
    }
    console.log({ client, images: imageArray });
    axios.post(server + `ImageServer/ColorClassification`, {
      client,
      images: imageArray,
    });
  };

  const reset = async (event) => {
    event.preventDefault();
    axios.get(server + `ImageServer/Reset`);
  };

  return (
    <div className="App">
      <img className="BgImg" src={bg} alt="bg"></img>
      <div className="Container">
        <h1 className="Title">Image web</h1>
        <form>
          <input
            className="Input"
            value={server}
            onChange={(e) => setServer(e.target.value)}
            type="text"
            placeholder="Server Ip"
          ></input>
          <input
            className="Input"
            value={client}
            onChange={(e) => setClient(e.target.value)}
            type="text"
            placeholder="Cliente"
          ></input>
          <ImageUploader
            withIcon
            withPreview
            label=""
            buttonText="Subir imagen"
            onChange={(imgs) => setImages(imgs)}
            imgExtension={[".jpg", ".jpeg", ".png", ".gif"]}
            maxFileSize={5242880}
          />
          <div className="BtnContainer">
            <button className="Button" onClick={histogram}>
              Histograma
            </button>
            <button className="Button" onClick={color}>
              Colores
            </button>
            <button className="Button" onClick={reset}>
              RESET
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
