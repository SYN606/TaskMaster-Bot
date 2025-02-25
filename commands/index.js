// Read all the command files dynamically and export them
const fs = require('fs');
const path = require('path');

// Dynamically read all the command files
const commandFiles = fs.readdirSync(path.join(__dirname)).filter(file => file.endsWith('.js'));

const commands = {};

for (const file of commandFiles) {
    if (file !== 'index.js') {
        const command = require(`./${file}`);
        commands[command.name] = command;
    }
}

module.exports = commands;
