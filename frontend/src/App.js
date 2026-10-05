import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState({
    status: "Loading...",
    drowsy_count: 0,
    yawn_count: 0,
    location: "",
    last_alert: ""
  });

  useEffect(() => {
    const fetchData = () => {
      axios
        .get("http://127.0.0.1:5000/dashboard-data")
        .then((res) => {
          setData(res.data);
        })
        .catch((err) => {
          console.error("API Error:", err);
        });
    };

    fetchData();

    const timer = setInterval(fetchData, 2000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🚗 Drowsiness & Yawn Detection Dashboard</h1>

      <hr />

      <h2>Status: {data.status}</h2>

      <h3>😴 Drowsiness Count: {data.drowsy_count}</h3>

      <h3>🥱 Yawn Count: {data.yawn_count}</h3>

      <h3>📍 Location</h3>

      {data.location &&
      data.location.startsWith("http") ? (
        <a href={data.location} target="_blank" rel="noreferrer">
          Open Location
        </a>
      ) : (
        <p>{data.location}</p>
      )}

      <h3>⏰ Last Alert</h3>
      <p>{data.last_alert}</p>

      <h3>📸 Driver Image</h3>

      <img
        src={`http://127.0.0.1:5000/alert-image?${Date.now()}`}
        alt="Driver"
        width="500"
        onError={(e) => {
          e.target.style.display = "none";
        }}
      />
    </div>
  );
}

export default App;