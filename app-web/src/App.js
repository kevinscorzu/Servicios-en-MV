import { useState } from "react";
import ImageUploader from "react-images-upload";

import "./App.css";
import bg from "./assets/bg-img.jpg";

function App() {
  const [server, setServer] = useState("");

  return (
    <div className="App">
      <img className="BgImg" src={bg} alt="bg"></img>
      <div className="Container">
        <h1 className="Title">Image web</h1>
        <form>
          <input
            value={server}
            onChange={(e) => setServer(e.target.value)}
            type="text"
            placeholder="Server Ip"
          ></input>
          <ImageUploader
            withIcon
            withPreview
            label=""
            singleImage
            buttonText="Subir imagen"
            onChange={(e) => console.log(e)}
            imgExtension={[".jpg", ".gif", ".png", ".gif"]}
            maxFileSize={5242880}
          />
          <button className="Button" onClick={(e) => e.preventDefault()}>
            Confirmar
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
