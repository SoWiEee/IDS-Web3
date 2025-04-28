function sendLog() {
    const eventType = document.getElementById('eventType').value;
    const description = document.getElementById('description').value;

    fetch('http://127.0.0.1:5000/log_event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ event_type: eventType, description: description })
    })
    .then(response => response.json())
    .then(data => {
        alert("Log Sent! TxHash: " + data.tx_hash);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error sending log');
    });
}