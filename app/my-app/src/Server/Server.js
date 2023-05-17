const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const cors = require('cors');
const app = express();
app.use(bodyParser.json());
app.use(cors());
// parse JSON request bodies
app.use(express.json());


port = process.env.PORT || 5000;
 

// MySQL configuration
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'cst',
});

// Connect to MySQL
connection.connect(err => {
  if (err) {
    console.error('Error connecting to MySQL: ', err);
    return;
  }
  console.log('Connected to MySQL');
});

// Login endpoint
app.post('/login', (req, res) => {
  const { email, password } = req.body;
  const query = 'SELECT * FROM registration WHERE email = ? AND password = ?';

  connection.query(query, [email, password], (err, results) => {
    if (err) {
      console.error('Error executing MySQL query: ', err);
      res.sendStatus(500);
      return;
    }

    if (results.length > 0) {
      // Valid login credentials
      res.sendStatus(200);
    } else {
      // Invalid credentials
      res.sendStatus(401);
    }
  });
});

// define the API endpoint for handling POST requests
app.post('/api/messages', (req, res) => {
  const message = req.body.message;
  console.log(`Received message: ${message}`);
  res.json({ response: 'Hello from Express!' });
});
// Start the server
app.listen(5000, () => {
  console.log('Server is running on port 5000');
});
