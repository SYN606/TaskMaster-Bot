import { Client, GatewayIntentBits } from 'discord.js';
import { readDB } from './db';  
require('dotenv').config();

// Dynamically import commands and utilities
const commands = require('./commands');
const utilities = require('./utils');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Set the bot prefix from the database, default to '!' if not found
const data = readDB();
client.prefix = data?.prefix || '**'; // Use optional chaining for cleaner code

// Attach commands and utilities to the client
client.commands = commands;
client.utils = utilities;

client.once('ready', () => {
    console.log('TaskMaster bot is online!');
});

// Listen for messages
client.on('messageCreate', async (message) => {
    if (message.author.bot) return; // Ignore bot's own messages

    // Ignore messages that don't start with the prefix
    if (!message.content.startsWith(client.prefix)) return;

    // Handle mentions (if bot is mentioned)
    if (message.mentions.has(client.user)) {
        // Use the botInfo utility to send bot information
        await client.utils.botInfo.execute(message, client);
    }

    // Parse arguments from the message content
    const args = message.content.slice(client.prefix.length).trim().split(/ +/); 
    const commandName = args.shift().toLowerCase(); // Get the command name

    // If the command exists, execute it
    const command = client.commands[commandName];
    if (!command) return;

    try {
        // Execute the command
        await command.execute(message, args);
    } catch (error) {
        console.error(error);
        message.reply('There was an error trying to execute that command!');
    }
});

// Log in to Discord with your app's token
client.login(process.env.TOKEN);
