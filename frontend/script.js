// async function fetchLogs() {
//   const response = await fetch("http://localhost:5000/get_logs");
//   const data = await response.json();
//   const container = document.getElementById("logs");
//   container.innerHTML = "";

//   if (data.status === "success") {
//     data.logs.forEach((log, index) => {
//       const div = document.createElement("div");
//       div.className = "log-entry";
//       div.innerText = `#${index + 1} | Type: ${log.event_type} | Timestamp: ${log.timestamp}`;
//       container.appendChild(div);
//     });
//   } else {
//     container.innerText = "Failed to load logs.";
//   }
// }

document.getElementById("eventForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const event_type = document.getElementById("eventType").value;
  const timestamp = document.getElementById("timestamp").value;

  const res = await fetch("/record_event", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ event_type, timestamp })
  });

  const result = await res.json();
  alert(JSON.stringify(result));
});