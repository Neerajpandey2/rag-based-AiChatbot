import "./App.css";
import RoutesFile from "./Routes/routes.jsx"; // rename to uppercase
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <>
     <ToastContainer position="top-right" autoClose={3000} />
     <RoutesFile />  // use capital letter here
    </>
  );
}

export default App;
