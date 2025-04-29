async function loadEvents() {
    const response = await fetch('http://localhost:5000/get_events');
    const events = await response.json();
    const tableBody = document.querySelector('#eventTable tbody');
    tableBody.innerHTML = '';
    events.forEach(event => {
      const row = document.createElement('tr');
      row.innerHTML = `<td>${event.event_type}</td><td>${new Date(event.timestamp * 1000).toLocaleString()}</td>`;
      tableBody.appendChild(row);
    });
  }
  
  loadEvents();
  setInterval(loadEvents, 5000);    // update /5sec
  