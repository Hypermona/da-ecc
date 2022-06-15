import logo from "./logo.svg";
import "./App.css";
import { useEffect, useState } from "react";
import Home from "./Components/Home";
import Loading from "./Components/Loading";

function App() {
  const [images, SetImages] = useState(null);
  const [enc, setEnc] = useState("");
  const [dec, setDec] = useState("");
  const [sink, setSink] = useState("");
  const [base, setBase] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  // useEffect(() => {
  //   fetch("http://127.0.0.1:8000/", { body: JSON.stringify(formData) })
  //     .then((r) => r.json())
  //     .then((d) => SetImages(d))
  //     .catch((err) => console.log(err));
  // }, []);
  const submitData = (data) => {
    setIsLoading(true);
    console.log(data);
    fetch("http://127.0.0.1:8000/", {
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-cache",
      method: "POST",
      body: JSON.stringify(data),
    })
      .then((r) => r.json())
      .then((d) => {
        console.log(d);
        setIsLoading(false);
        SetImages(d.charts);
        setDec(d.decryption);
        setEnc(d.decryption);
        setSink(d.sink);
        setBase(d.base);
      })
      .catch((err) => {
        setIsLoading(false);
        console.log(err);
      });
  };
  return (
    <div className="App">
      {images ? (
        <div>
          {/* <p>Encrypted Data At Sink Node: {sink} S</p>
          <p>Decrypted Data At Base Node: {base} S</p> */}
          <p>Encryptio Time: {enc} S</p>
          <p>Decryption Time: {dec} S</p>
          {images.map((image, i) => (
            <img src={`data:image/png;base64,${image}`} alt="" key={i} />
          ))}
        </div>
      ) : isLoading ? (
        <Loading />
      ) : (
        <Home submitData={submitData} />
      )}
    </div>
  );
}

export default App;
