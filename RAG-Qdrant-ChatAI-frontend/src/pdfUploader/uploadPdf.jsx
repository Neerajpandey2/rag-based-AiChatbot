// UploadPdfComponent.jsx
import React, { useState } from "react";
import { uploadPdf } from "../Apis/api";
import "./uploadPdf.css";

function UploadPdfComponent() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const DEFAULT_COLLECTION = "CustomAi"; // default collection name

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Select a PDF first");

    try {
      const res = await uploadPdf(file, DEFAULT_COLLECTION); // send collection name
      setMessage(res.message || "Upload complete");
    } catch (err) {
      console.error(err);
      setMessage("Upload failed");
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload PDF</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload PDF</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadPdfComponent;
