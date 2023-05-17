const express = require('express');
const cors = require('cors');

const app = express();
console.log("In")
// parse JSON request bodies
app.use(express.json());
app.use(cors()); // Enable CORS for all routes


let receivedMessage = '';

// For receiving msg
app.post('/api/recmessage', (req, res) => {
  receivedMessage = req.body.message;
  console.log(`Received message: ${receivedMessage}`);
  res.json({ status: 'Message received successfully' });
});

// For sending to frontend
app.get('/api/message', (req, res) => {
    console.log(`In Fronted msg : ${receivedMessage}`)
  res.json({ message: receivedMessage });
  receivedMessage=''
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});