// Read all the utility files dynamically and export them
const fs = require('fs');
const path = require('path');

// Dynamically read all the utility files
const utilityFiles = fs.readdirSync(path.join(__dirname)).filter(file => file.endsWith('.js'));

const utilities = {};

for (const file of utilityFiles) {
    if (file !== 'index.js') {
        const utility = require(`./${file}`);
        utilities[utility.name] = utility;
    }
}

module.exports = utilities;
