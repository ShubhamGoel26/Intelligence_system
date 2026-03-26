"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Upload a file first");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setResults(res.data.results);
    } catch (err) {
      console.error(err);
      alert("Error uploading file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 30 }}>
      <h1>Lead Intelligence Dashboard</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button onClick={handleUpload} style={{ marginLeft: 10 }}>
        Upload
      </button>

      {loading && <p>Processing...</p>}

      <table border={1} cellPadding={10} style={{ marginTop: 20 }}>
        <thead>
          <tr>
            <th>Company</th>
            <th>Summary</th>
            <th>Contact</th>
            <th>Outreach</th>
          </tr>
        </thead>

        <tbody>
          {results.map((r, i) => (
            <tr key={i}>
              <td>{r.company}</td>

              <td>
                {r.profile?.description}
                <br />
                <b>Tools:</b> {r.profile?.tools_used}
              </td>

              <td>
                📞 {r.contact?.phone || "N/A"} <br />
                📧 {r.contact?.email || "N/A"} <br />
                🔗 {r.contact?.source || "N/A"}
              </td>

              <td style={{ maxWidth: 300 }}>
                {r.outreach_message}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}