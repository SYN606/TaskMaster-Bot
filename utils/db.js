const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'db.json');


const readDB = () => {
    try {
        const data = fs.readFileSync(dbPath, 'utf8');
        return JSON.parse(data); 
    } catch (err) {
        console.error('Error reading DB:', err);
        return null; 
    }
};


const writeDB = (data) => {
    try {
        fs.writeFileSync(dbPath, JSON.stringify(data, null, 2)); 
    } catch (err) {
        console.error('Error writing to DB:', err);
    }
};

module.exports = { readDB, writeDB };
