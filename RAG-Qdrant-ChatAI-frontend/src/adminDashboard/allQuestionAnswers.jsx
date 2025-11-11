import React, { useEffect, useState } from "react";
import {
  getQAPaginated,
  addQAPoint,
  editQAPoint,
  deleteQAPoint,
} from "../Apis/api";

export default function QuestionsAnswersPage() {
  const [qaList, setQaList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [form, setForm] = useState({ question: "", answer: "" });
  const [nextOffset, setNextOffset] = useState(null);
  const [totalPoints, setTotalPoints] = useState(0);

  const collection = "CustomAi";
  const pageSize = 25;

  useEffect(() => {
    fetchQA(true);
  }, []);

  const fetchQA = async (reset = false) => {
    try {
      setLoading(true);

      const data = await getQAPaginated(
        collection,
        pageSize,
        reset ? null : nextOffset
      );

      if (reset) {
        setQaList(data.qa_list || []);
      } else {
        setQaList((prev) => [...prev, ...(data.qa_list || [])]);
      }

      setNextOffset(data.next_page_offset || null);
      setTotalPoints(data.total_points || 0);
    } catch (err) {
      console.error("Error fetching Q&A:", err);
    } finally {
      setLoading(false);
    }
  };

  // Open Add/Edit Modal
  const openModal = (item = null) => {
    setEditingItem(item);
    setForm(
      item ? { question: item.question, answer: item.answer } : { question: "", answer: "" }
    );
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      if (editingItem) {
        await editQAPoint(collection, editingItem.id, form.question, form.answer);
      } else {
        await addQAPoint(collection, form.question, form.answer);
      }
      await fetchQA(true); // reload from start
      setModalOpen(false);
    } catch (err) {
      console.error("Save failed:", err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this Q&A?")) return;
    try {
      await deleteQAPoint(collection, id);
      await fetchQA(true); // reload from start
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  return (
    <div className="container py-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="fw-bold">📖 All Questions & Answers</h2>
        <button className="btn btn-success" onClick={() => openModal()}>
          ➕ Add New Question
        </button>
      </div>

      {/* Loading */}
      {loading && qaList.length === 0 ? (
        <div className="d-flex justify-content-center my-5">
          <div className="spinner-border text-primary" role="status" />
        </div>
      ) : qaList.length > 0 ? (
        <>
          <div className="list-group">
            {qaList.map((item, index) => (
              <div key={item.id || index} className="card mb-3 shadow-sm">
                <div className="card-body">
                  <p className="mb-2">
                    <strong>{index + 1}. Question:</strong> {item.question}
                  </p>
                  <p>
                    <strong>Answer:</strong> {item.answer}
                  </p>
                  <div className="d-flex gap-2 mt-2">
                    <button className="btn btn-primary btn-sm" onClick={() => openModal(item)}>
                      ✏️ Edit
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(item.id)}
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          <div className="d-flex justify-content-center my-3">
            {nextOffset ? (
              <button className="btn btn-outline-primary" onClick={() => fetchQA(false)}>
                ⬇️ Load More
              </button>
            ) : (
              <p className="text-muted">
                ✅ All {totalPoints} Q&A items loaded.
              </p>
            )}
          </div>
        </>
      ) : (
        <p className="text-muted">No data found.</p>
      )}

      {/* Modal */}
      {modalOpen && (
        <div
          className="modal fade show d-block"
          tabIndex="-1"
          style={{ background: "rgba(0,0,0,0.5)" }}
        >
          <div className="modal-dialog">
            <div className="modal-content shadow-lg">
              <div className="modal-header">
                <h5 className="modal-title">{editingItem ? "Edit Q&A" : "Add Q&A"}</h5>
                <button type="button" className="btn-close" onClick={() => setModalOpen(false)} />
              </div>
              <div className="modal-body">
                <input
                  type="text"
                  className="form-control mb-3"
                  placeholder="Enter question"
                  value={form.question}
                  onChange={(e) => setForm({ ...form, question: e.target.value })}
                />
                <textarea
                  className="form-control"
                  rows="3"
                  placeholder="Enter answer"
                  value={form.answer}
                  onChange={(e) => setForm({ ...form, answer: e.target.value })}
                />
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setModalOpen(false)}>
                  ❌ Cancel
                </button>
                <button className="btn btn-success" onClick={handleSave}>
                  💾 Save
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
