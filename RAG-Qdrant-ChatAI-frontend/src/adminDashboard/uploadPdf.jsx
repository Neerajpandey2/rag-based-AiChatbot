import React, { useState } from "react";
import { uploadPdf, saveQaPairs } from "../Apis/api";
import "bootstrap/dist/css/bootstrap.min.css";
import "./uploadPdf.css";


function UploadPdfComponent() {
  const collection_name = "CustomAi"; // default collection name
  const [saving, setSaving] = useState(false);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [qaPairs, setQaPairs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newQA, setNewQA] = useState({ question: "", answer: "" });
  const [stats, setStats] = useState({ total_chunks: 0, total_qa_generated: 0 });
  const [newAddedCount, setNewAddedCount] = useState(0);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Select a PDF first");

    setLoading(true);
    setMessage("Generating questions and answers...");

    try {
      const res = await uploadPdf(file);
      setMessage(res.message || "Upload complete");

      // set stats from backend
      setStats({
        total_chunks: res.total_chunks || 0,
        total_qa_generated: res.total_qa_generated || 0,
      });

      setQaPairs(res.qa_pairs || []);
      setNewAddedCount(0); // reset new added count after upload
    } catch (err) {
      console.error(err);
      setMessage("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (index, field, value) => {
    const updated = [...qaPairs];
    updated[index][field] = value;
    setQaPairs(updated);
  };

  const handleDelete = (index) => {
    const updated = qaPairs.filter((_, i) => i !== index);
    setQaPairs(updated);
  };

  const handleAdd = () => {
    if (!newQA.question.trim() || !newQA.answer.trim()) {
      return alert("Enter both question & answer");
    }
    setQaPairs([...qaPairs, newQA]);
    setNewQA({ question: "", answer: "" });
    setNewAddedCount(newAddedCount + 1);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      console.log("Saving to DB:", qaPairs);
      const res = await saveQaPairs(collection_name , qaPairs);
      setSaving(false);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container mt-4">
      {/* Upload Section */}
      <div className="card p-3 shadow-sm mb-4">
        <h2 className="mb-3">Upload PDF</h2>
        <input
          type="file"
          accept="application/pdf"
          className="form-control mb-2"
          onChange={handleFileChange}
        />
        <button className="btn btn-primary" onClick={handleUpload}>
         Upload PDF
        </button>
        {message && <p className="mt-2">{message}</p>}
      </div>

      {/* Stats Section */}
      {(stats.total_chunks > 0 || stats.total_qa_generated > 0 || newAddedCount > 0) && (
        <div className="row mb-4">
          <div className="col-md-4">
            <div className="card text-center shadow-sm">
              <div className="card-body">
                <h5 className="card-title text-primary">📑 Total Chunks</h5>
                <p className="fs-4 fw-bold">{stats.total_chunks}</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card text-center shadow-sm">
              <div className="card-body">
                <h5 className="card-title text-success">❓ Q&A Generated</h5>
                <p className="fs-4 fw-bold">{stats.total_qa_generated}</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card text-center shadow-sm">
              <div className="card-body">
                <h5 className="card-title text-warning">➕ Newly Added Q&A</h5>
                <p className="fs-4 fw-bold">{newAddedCount}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Q&A Section */}
      <div className="mt-4">
        {loading ? (
          <div className="text-center">
            <div className="spinner-border text-primary" role="status"></div>
            <p className="mt-2">Generating questions & answers...</p>
          </div>
        ) : qaPairs.length > 0 ? (
          <div className="card p-3 shadow-sm">
            {/* Save Button at Top */}
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h3 className="text-primary">📖 Extracted Questions & Answers</h3>
              <button className="btn btn-success" onClick={handleSave}>
              {!saving ? "💾 Save to Database" : "Saving..."}
              </button>
            </div>

            {/* Q&A List */}
            <div className="row">
              {qaPairs.map((qa, index) => (
                <div key={index} className="col-md-6 mb-3">
                  <div className="card shadow-sm h-100">
                    <div className="card-body">
                      <label className="form-label fw-bold">
                        Question {index + 1}
                      </label>
                      <textarea
                        className="form-control mb-2 qa-textarea"
                        value={qa.question}
                        onChange={(e) =>
                          handleEdit(index, "question", e.target.value)
                        }
                      />
                      <label className="form-label fw-bold">Answer</label>
                      <textarea
                        className="form-control mb-3 qa-textarea"
                        value={qa.answer}
                        onChange={(e) =>
                          handleEdit(index, "answer", e.target.value)
                        }
                      />
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(index)}
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Add New Q&A */}
            <div className="card shadow-sm mt-4">
              <div className="card-body">
                <h5 className="card-title text-success">➕ Add New Q&A</h5>
                <label className="form-label fw-bold">Question</label>
                <textarea
                  className="form-control mb-2 qa-textarea"
                  placeholder="Enter question"
                  value={newQA.question}
                  onChange={(e) =>
                    setNewQA({ ...newQA, question: e.target.value })
                  }
                />
                <label className="form-label fw-bold">Answer</label>
                <textarea
                  className="form-control mb-3 qa-textarea"
                  placeholder="Enter answer"
                  value={newQA.answer}
                  onChange={(e) =>
                    setNewQA({ ...newQA, answer: e.target.value })
                  }
                />
                <button className="btn btn-primary" onClick={handleAdd}>
                  Add Q&A
                </button>
              </div>
            </div>
          </div>
        ) : (
          !loading &&
          message && (
            <div className="alert alert-info mt-3">No Q&A generated yet.</div>
          )
        )}
      </div>
    </div>
  );
}

export default UploadPdfComponent;
