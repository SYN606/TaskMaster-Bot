const { readDB, writeDB } = require('../utils'); 

module.exports = {
    name: 'changePrefix',
    description: 'Change the command prefix for the bot.',
    async execute(message, args) {
        // Make sure the user has permission to change the prefix
        if (!message.member.permissions.has('ADMINISTRATOR')) {
            return message.reply("You need administrator permissions to change the prefix.");
        }

        // Ensure the new prefix is provided
        if (!args[0]) {
            return message.reply('Please provide a new prefix!');
        }

        const newPrefix = args[0];

        // Check if the new prefix is valid (you can add more validation if needed)
        if (newPrefix.length > 3) {
            return message.reply('Prefix must be 1-3 characters long.');
        }

        // Get current data from the DB
        const data = readDB();
        if (!data) {
            return message.reply('Error reading the database.');
        }

        // Update the prefix in the DB data
        data.prefix = newPrefix;

        // Save the updated data back to the DB
        writeDB(data);

        // Update the bot's prefix in memory
        message.client.prefix = newPrefix;

        message.reply(`Prefix has been changed to: ${newPrefix}`);
    }
};
