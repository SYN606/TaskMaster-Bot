const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'db.json');

// Function to read the database from db.json
const readDB = () => {
    try {
        const data = fs.readFileSync(dbPath, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error('Error reading DB:', err);
        return {}; // Return an empty object if DB is not readable
    }
};

// Function to write data to db.json
const writeDB = (data) => {
    try {
        fs.writeFileSync(dbPath, JSON.stringify(data, null, 2), 'utf8');
    } catch (err) {
        console.error('Error writing to DB:', err);
    }
};

// Function to create or add data dynamically based on a key
const createData = (key, subKey, data) => {
    try {
        const db = readDB(); // Read the current data

        if (!db[key]) {
            db[key] = {}; // Create the key if it does not exist
        }

        db[key][subKey] = data; // Add the data under the specific subKey
        writeDB(db); // Write the updated data to the DB
        console.log(`Data added under ${key} -> ${subKey}`);
    } catch (err) {
        console.error(`Error creating data under ${key} -> ${subKey}:`, err);
    }
};

// Function to update existing data dynamically based on a key and subKey
const updateData = (key, subKey, updatedData) => {
    try {
        const db = readDB(); // Read the current data

        if (db[key] && db[key][subKey]) {
            db[key][subKey] = { ...db[key][subKey], ...updatedData }; // Update the existing data
            writeDB(db); // Write the updated data to the DB
            console.log(`Data updated for ${key} -> ${subKey}`);
        } else {
            console.error(`${subKey} not found under ${key}`);
        }
    } catch (err) {
        console.error(`Error updating data for ${key} -> ${subKey}:`, err);
    }
};

// Function to read data dynamically based on a key and subKey
const readData = (key, subKey) => {
    try {
        const db = readDB(); // Read the current data

        if (db[key] && db[key][subKey]) {
            return db[key][subKey]; // Return the requested data
        } else {
            console.error(`${subKey} not found under ${key}`);
            return null;
        }
    } catch (err) {
        console.error(`Error reading data for ${key} -> ${subKey}:`, err);
        return null;
    }
};

// Function to delete data dynamically based on a key and subKey
const deleteData = (key, subKey) => {
    try {
        const db = readDB(); // Read the current data

        if (db[key] && db[key][subKey]) {
            delete db[key][subKey]; // Delete the specific data
            writeDB(db); // Write the updated data to the DB
            console.log(`Data deleted for ${key} -> ${subKey}`);
        } else {
            console.error(`${subKey} not found under ${key}`);
        }
    } catch (err) {
        console.error(`Error deleting data for ${key} -> ${subKey}:`, err);
    }
};

module.exports = { readDB, writeDB, createData, updateData, readData, deleteData };
