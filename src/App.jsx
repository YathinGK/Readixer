<<<<<<< HEAD
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FeatureSection from "./components/FeatureSection";
import HandwritingPage from "./pages/HandwritingPage";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Home page with FeatureSection */}
        <Route path="/" element={<FeatureSection />} />

        {/* Handwriting Conversion Page */}
        <Route path="/handwriting" element={<HandwritingPage />} />
      </Routes>
    </Router>
  );
}
=======
function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-purple-200">
      <h1 className="text-4xl font-bold text-slate-800">
        🚀 Tailwind is working!
      </h1>
    </div>
  );
}

export default App;
>>>>>>> 9aaf3d353304132cf53f9e391a6c04823d71bf19
