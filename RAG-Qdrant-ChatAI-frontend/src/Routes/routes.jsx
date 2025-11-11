import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "../reusableComponents/header";
import Chatbot from "../chatBot/chatBot";
import AdminDashboard from "../adminDashboard/adminDashboard";
import ManageQuestions from "../adminDashboard/manageQuestions";
import GetAllQaList from "../adminDashboard/allQuestionAnswers";
import UploadPage from "../adminDashboard/uploadPdf"; // Dummy Page (replace later)

function App() {
  return (
    <Router>
      {/* Header visible on all pages */}
      <Header />

      <Routes>
        {/* Public Pages */}
        <Route path="/" element={<Chatbot />} />

        {/* Admin Pages with Nested Routes */}
        <Route path="/admin" element={<AdminDashboard />}>
          <Route path="documentUpload" element={<UploadPage />} />
          <Route path="manageQuestionAnswer" element={<ManageQuestions />} />
          <Route path="getAllQa" element={<GetAllQaList />} />
        </Route>

        {/* 404 Fallback */}
        <Route
          path="*"
          element={<h2 className="p-6 text-center">404 Page Not Found</h2>}
        />
      </Routes>
    </Router>
  );
}

export default App;
