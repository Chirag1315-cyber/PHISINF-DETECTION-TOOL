import React, { useState } from "react";

function UrlChecker() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkUrl = async () => {
    if (!url) {
      alert("Please enter a URL");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://localhost:5000/api/check_url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Backend not reachable");
    }

    setLoading(false);
  };

  const getClass = () => {
    if (!result) return "";
    if (result.verdict === "safe") return "safe";
    if (result.verdict === "phishing") return "phishing";
    return "suspicious";
  };

  return (
    <div className="card">
      <div className="title">
        <h1>Phishing Detection Tool</h1>
        <p>AI‑powered URL security scanner</p>
      </div>

      <input
        type="text"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={checkUrl}>
        {loading ? "Analyzing..." : "Scan URL"}
      </button>

      {result && (
        <div className={`result ${getClass()}`}>
          <p><strong>Verdict:</strong> {result.verdict.toUpperCase()}</p>
          <p><strong>Detection Method:</strong> {result.detection_method}</p>

          <div className="progress-bar">
            <div
              className="progress"
              style={{ width: `${result.confidence * 100}%` }}
            ></div>
          </div>

          <p><strong>Confidence:</strong> {Math.round(result.confidence * 100)}%</p>
        </div>
      )}
    </div>
  );
}

export default UrlChecker;
