const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const DB_FILE = path.join(__dirname, 'database.json');

// Middleware
app.use(cors());
app.use(express.json()); // Parses JSON bodies

// Ensure database file exists
if (!fs.existsSync(DB_FILE)) {
  fs.writeFileSync(DB_FILE, JSON.stringify([]));
}

// ── ENDPOINTS ──

// Health Check
app.get('/api/health', (req, res) => {
  res.json({ status: 'Online', message: 'Data Infrastructure Intact' });
});

// Join Waitlist Network Endpoint
app.post('/api/waitlist', (req, res) => {
  try {
    const { name, email, company } = req.body;

    // Validation
    if (!name || !email) {
      return res.status(400).json({ success: false, error: 'Name and Email are strictly required for Network Access.' });
    }

    // Read existing database
    const dbData = fs.readFileSync(DB_FILE, 'utf8');
    const records = JSON.parse(dbData || '[]');

    // Prevent duplicate emails
    if (records.some(record => record.email === email)) {
      return res.status(409).json({ success: false, error: 'Terminal alert: Email already registered in the Network.' });
    }

    // Insert new record
    const newEntry = {
      id: Date.now().toString(),
      name,
      email,
      company: company || 'N/A',
      timestamp: new Date().toISOString()
    };
    records.push(newEntry);

    // Write back to database
    fs.writeFileSync(DB_FILE, JSON.stringify(records, null, 2));

    console.log(`[NETWORK LOG] Access Granted for User: ${email}`);
    res.status(201).json({ success: true, message: 'Terminal: Access Granted' });
  } catch (error) {
    console.error('[NETWORK ERROR]', error);
    res.status(500).json({ success: false, error: 'Internal Server Error.' });
  }
});

app.listen(PORT, () => {
  console.log(`===============================================`);
  console.log(`[+] FACTGUARD TERMINAL BACKEND ACTIVE`);
  console.log(`[+] PORT: ${PORT}`);
  console.log(`[+] NETWORK DB: ${DB_FILE}`);
  console.log(`===============================================`);
});
