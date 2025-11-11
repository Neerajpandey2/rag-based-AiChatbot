import React, { useState } from "react";
import "./manageQuestions.css";

export default function ManageQuestions() {
  // Dummy data for now
  const [questions, setQuestions] = useState([
    { id: 1, question: "Hi, Hello, Hlw", answer: "Hello, How can I help you?" },
    { id: 2, question: "What is your aim?", answer: "I am your assistant." },
  ]);

  const deleteQuestion = (id) => {
    setQuestions(questions.filter((q) => q.id !== id));
  };

  return (
    <div className="manage-questions">
      <h1>Manage Questions</h1>
      <button className="add-btn">+ Add New Question</button>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Question</th>
            <th>Answer</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {questions.map((q) => (
            <tr key={q.id}>
              <td>{q.id}</td>
              <td>{q.question}</td>
              <td>{q.answer}</td>
              <td>
                <button className="edit-btn">Edit</button>
                <button className="delete-btn" onClick={() => deleteQuestion(q.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
