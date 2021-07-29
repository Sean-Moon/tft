const mysql      = require('mysql');
const connection = mysql.createConnection({
  host     : '220.90.208.92',
  user     : 'tmax',
  password : 'tmax',
  database : 'testdb'
});

connection.connect();

connection.query('SELECT 1 ', (error, rows, fields) => {
  if (error) throw error;
  console.log('User info is: ', rows);
});

connection.end();
