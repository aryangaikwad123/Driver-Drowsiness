import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Dashboard.css";

function Dashboard() {

  const [data, setData] = useState({});

  useEffect(() => {

    const fetchData = () => {

      axios
        .get("http://127.0.0.1:5000/dashboard-data")
        .then((res) => {
          setData(res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    fetchData();

    const timer = setInterval(fetchData, 2000);

    return () => clearInterval(timer);

  }, []);

  return (
    <div className="container">

      <h1 className="title">
        🚗 Driver Drowsiness Dashboard
      </h1>

      <div className="status-bar">
        🟢 Real-Time Monitoring Active
      </div>

      <div className="cards">

        <div className="card">
          <h3>Total Alerts</h3>
          <h1>
            {data.drowsy_count + data.yawn_count || 0}
          </h1>
        </div>

        <div className="card">
          <h3>Drowsy Alerts</h3>
          <h1 className="danger">
            {data.drowsy_count}
          </h1>
        </div>

        <div className="card">
          <h3>Yawn Alerts</h3>
          <h1 className="warning">
            {data.yawn_count}
          </h1>
        </div>

      </div>

      <div className="alert-box">

        <h3>
          🚨 Latest Alert :
          {data.status}
        </h3>

        <p>{data.location}</p>

      </div>

      <div className="main-grid">

        <div className="details">

          <span className="badge">
            😴 {data.status}
          </span>

          <p>
            ⏰ {data.last_alert}
          </p>

          <p>
            📍 {data.location}
          </p>
           (
            <p>
  📍 {data.location}
</p>

<a
  href={data.location}
  target="_blank"
  rel="noreferrer"
>
  <button>View Location</button>
</a>

<br /><br />

<iframe
  title="Driver Location"
  src={
    data.location
      ? data.location.replace(
          "https://www.google.com/maps?q=",
          "https://maps.google.com/maps?q="
        ) + "&z=15&output=embed"
      : ""
  }
  width="100%"
  height="300"
  style={{
    border: 0,
    borderRadius: "10px"
  }}
  loading="lazy"
/>
           )
          <a
            href={data.location}
            target="_blank"
            rel="noreferrer"
          >
            <button>
              View Location
            </button>
          </a>

        </div>

        <div className="image-box">

          <img
            src={`http://127.0.0.1:5000/alert-image?${Date.now()}`}
            alt="Driver"
          />

        </div>

      </div>

    </div>
  );
}

export default Dashboard;