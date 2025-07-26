const fs = require('fs');
const express = require('express');
const app = express();
const port = 3000;

const logDir = '/usr/src/app/logs';
const logFile = `${logDir}/app.log`;

// Garante que o diretório de logs existe
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

app.get('/', (req, res) => {
  const message = `Hello World - ${new Date().toISOString()}\n`;
  fs.appendFileSync(logFile, message);
  res.send('Log registrado!\n');
});

app.listen(port, () => {
  console.log(`App rodando em http://localhost:${port}`);
});
